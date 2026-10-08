import pytest
from local_comparison import RMSD_BINDING

import praxis
from praxis.errors import RecordingError


def test_recorda_and_ackredit_borrow_sessions_and_keep_reused_credits(
    workspace, prepared, tmp_path, prepare_recipe
):
    recorda = pytest.importorskip("recorda")
    ackredit = pytest.importorskip("ackredit")
    catalog, context = workspace
    original = context.extensions.bindings[RMSD_BINDING]
    item = "software:praxis-test:fictional-fixture:1"
    ackredit.register_item(
        id=item, type="software", title="Fictional Praxis test fixture", version="1"
    )

    def credited(inputs, configuration, recipe_context):
        result = original.recipe(inputs, configuration, recipe_context)
        ackredit.track_item(item, roles=["executed_software"], context={"fixture": True})
        return result

    prepared = prepare_recipe(credited)
    attempts = []
    with ackredit.session("application") as credits:
        with recorda.session("application", path=tmp_path / "operations.jsonl") as recording:
            context.recorder = praxis.RecordaRecorder(recording)
            context.attribution = True
            for _ in range(2):
                _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
                attempts.append(attempt)
                assert attempt.recording_status == "complete_declared_boundaries"
                assert attempt.attribution["items"][0]["id"] == item
            assert ackredit.current_session() is credits
            with recording.operation("application.still_active"):
                pass
    record = recorda.inspect(tmp_path / "operations.jsonl")
    assert len(record.operations) == 5
    assert record.operations[0]["inputs"]["attempt_id"] == attempts[0].identifier
    assert record.operations[1]["parent_id"] == record.operations[0]["id"]
    assert (
        attempts[0].recording_refs[0]["operation_id"]
        != attempts[1].recording_refs[0]["operation_id"]
    )
    # Preserved attribution can be loaded offline, without crediting new work.
    before = ackredit.get_used_items()
    restored = ackredit.Attribution.from_dict(attempts[0].attribution)
    assert restored.to_dict() == attempts[0].attribution
    assert before == ackredit.get_used_items()


def test_recorda_policy_exclusion_is_not_complete_recording(workspace, prepared, tmp_path):
    recorda = pytest.importorskip("recorda")
    catalog, context = workspace
    with recorda.session(
        "excluded",
        path=tmp_path / "excluded.jsonl",
        capture_policy=recorda.CapturePolicy(profiles=("other",)),
    ) as session:
        context.recorder = praxis.RecordaRecorder(session)
        _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.operational_status == "completed"
    assert attempt.recording_status == "omitted_by_policy"
    assert not attempt.recording_refs


def test_recorda_failure_prevents_provider_call(
    workspace, prepared, tmp_path, monkeypatch, prepare_recipe
):
    recorda = pytest.importorskip("recorda")
    catalog, context = workspace
    called = []
    original = context.extensions.bindings[RMSD_BINDING]

    def recipe(*args):
        called.append(1)
        return original.recipe(*args)

    prepared = prepare_recipe(recipe)
    with recorda.session("fault", path=tmp_path / "fault.jsonl") as session:
        context.recorder = praxis.RecordaRecorder(session)
        append = session._append

        def fails(event, **data):
            if event == "operation_started":
                raise OSError("test recording fault")
            return append(event, **data)

        monkeypatch.setattr(session, "_append", fails)
        with pytest.raises(RecordingError):
            praxis.execute(prepared, catalog=catalog, context=context, identifier="recording-fault")
    attempt = context.records.attempt("recording-fault")
    assert not called and attempt.recording_status == "gap"


def test_native_exception_survives_terminal_snapshot_failure(
    workspace, prepared, monkeypatch, prepare_recipe
):
    catalog, context = workspace
    native = ValueError("fixture native failure")

    def fails(*args):
        raise native

    prepared = prepare_recipe(fails)
    persist = context.records.save_attempt

    def failed_persistence(attempt):
        if attempt.finished is not None:
            raise OSError("terminal snapshot failure")
        return persist(attempt)

    monkeypatch.setattr(context.records, "save_attempt", failed_persistence)
    with pytest.raises(ValueError) as caught:
        praxis.execute(prepared, catalog=catalog, context=context, identifier="partial-persistence")
    assert caught.value is native
    assert "Praxis method attempt: partial-persistence" in native.__notes__
    assert any("could not persist the terminal" in note for note in native.__notes__)
    assert context.records.attempt("partial-persistence").operational_status == "incomplete"
