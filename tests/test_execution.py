from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, INPUT_CHECK, OUTPUT_CHECK, RMSD, RMSD_BINDING

import praxis
from praxis.errors import ContractError, IntegrityError, NotReadyError


def test_success_reopens_and_inputs_remain_unchanged(workspace, prepared, inputs, tmp_path):
    catalog, context = workspace
    outputs, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert outputs["score"] == pytest.approx(2**-0.5)
    assert inputs["left"] == [[0, 0, 0], [1, 0, 0]]
    assert attempt.operational_status == "completed"
    assert attempt.contract_status == "supported"
    assert attempt.recording_status == "not_requested"
    reopened = praxis.MethodRecords(tmp_path / "records")
    assert reopened.attempt(attempt.identifier) == attempt
    assert reopened.prepared(prepared.identifier) == prepared
    assert [item.requirement for item in attempt.findings if item.outcome != "passed"] == []
    assert catalog.assessments_for(RMSD) == ()


def test_multiple_protocols_or_bindings_do_not_select_by_registration_order(workspace, inputs):
    catalog, context = workspace
    ambiguous = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs), catalog=catalog, context=context
    )
    assert not ambiguous.ready and ambiguous.selection.protocol_ref is None
    binding = context.extensions.bindings[RMSD_BINDING]
    context.extensions.register_binding(replace(binding, ref=replace(RMSD_BINDING, version="2")))
    ambiguous = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD),
        catalog=catalog,
        context=context,
    )
    assert not ambiguous.ready and ambiguous.selection.binding_ref is None


@pytest.mark.parametrize(
    "outcome,expected",
    [
        ("passed", "applicable"),
        ("failed", "inapplicable"),
        ("undetermined", "undetermined"),
        ("skipped", "undetermined"),
    ],
)
def test_applicability_outcomes_are_distinct(
    workspace, inputs, outcome, expected, configure_extensions
):
    catalog, context = workspace
    configure_extensions(
        {INPUT_CHECK: lambda *args: praxis.CheckResult(outcome, "fixture finding")}
    )
    report = praxis.assess_applicability(
        catalog.get(CAPABILITY), catalog.get(RMSD), inputs, {}, context.extensions
    )
    assert report.outcome == expected


def test_missing_checker_blocks_engine_but_not_registration(
    workspace, inputs, configure_extensions
):
    catalog, context = workspace
    configure_extensions(omitted=(INPUT_CHECK,))
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready
    with pytest.raises(NotReadyError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="missing-checker")
    attempt = context.records.attempt("missing-checker")
    assert attempt.operational_status == "blocked" and not attempt.steps


def test_actual_consumption_rechecks_preconditions(workspace, inputs, configure_extensions):
    catalog, context = workspace
    environment = {"outcome": "passed"}

    def check(*args):
        return praxis.CheckResult(environment["outcome"], "Current conditions")

    configure_extensions({INPUT_CHECK: check})
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready
    environment["outcome"] = "failed"
    with pytest.raises(NotReadyError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="changed-conditions")
    assert any(
        check.outcome == "failed"
        for check in context.records.attempt("changed-conditions").findings
    )


def test_mutated_prepared_inputs_are_rejected(workspace, prepared):
    catalog, context = workspace
    prepared.inputs["left"][0][0] = 100
    with pytest.raises(IntegrityError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="tampered")
    assert context.records.attempt("tampered").operational_status == "failed"


def test_native_failure_partial_steps_and_retry_are_retained(workspace, inputs):
    catalog, context = workspace
    native = ValueError("fictional provider details should not be persisted")
    working = context.extensions.bindings[RMSD_BINDING]

    def fails(inputs, configuration, recipe_context):
        with recipe_context.step("measure"):
            raise native

    # Use a distinct implementation identity for the failing recipe.
    failing_ref = replace(RMSD_BINDING, identifier="fixture.failing_recipe")
    context.extensions.register_binding(replace(working, ref=failing_ref, recipe=fails))
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=failing_ref),
        catalog=catalog,
        context=context,
    )
    with pytest.raises(ValueError) as caught:
        praxis.execute(prepared, catalog=catalog, context=context, identifier="failed-provider")
    assert caught.value is native
    attempt = context.records.attempt("failed-provider")
    assert attempt.failure_type == "ValueError" and attempt.steps[0]["status"] == "failed"
    assert "fictional provider details" not in str(attempt.to_dict())
    with pytest.raises(ValueError):
        praxis.execute(
            prepared,
            catalog=catalog,
            context=context,
            retry_of=attempt.identifier,
            identifier="retry",
        )
    assert context.records.attempt("retry").retry_of == attempt.identifier


def test_postcondition_failure_is_not_an_engine_failure(workspace, inputs, configure_extensions):
    catalog, context = workspace
    configure_extensions(
        {OUTPUT_CHECK: lambda *args: praxis.CheckResult("failed", "Output guarantee violated")}
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    outputs, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert outputs is not None
    assert attempt.operational_status == "completed"
    assert attempt.contract_status == "unsupported"
    assert attempt.findings[-1].outcome == "failed"


@pytest.mark.parametrize("presentation_failure", [False, True])
def test_checker_error_is_unresolved_and_its_private_message_is_not_stored(
    workspace, inputs, configure_extensions, monkeypatch, presentation_failure
):
    import smonitor

    catalog, context = workspace
    warnings_before = smonitor.report()["warnings_total"]
    if presentation_failure:

        def broken_transport(*args, **kwargs):
            raise OSError("diagnostic transport unavailable")

        monkeypatch.setattr(smonitor, "emit", broken_transport)

    def fails(*args):
        raise RuntimeError("private checker content")

    configure_extensions({INPUT_CHECK: fails})
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready
    assert any(check.outcome == "checker_error" for check in prepared.findings)
    assert "private checker content" not in str(prepared.to_dict())
    if not presentation_failure:
        assert smonitor.report()["warnings_total"] > warnings_before


def test_advisory_findings_do_not_override_required_gate(workspace, inputs):
    catalog, context = workspace
    protocol = catalog.get(RMSD)
    advisory = replace(
        protocol,
        ref=replace(RMSD, version="advisory"),
        requirements=(
            praxis.Requirement("advisory", "Unimplemented advisory check", mandatory=False),
        ),
    )
    catalog.register(advisory)
    binding = replace(
        context.extensions.bindings[RMSD_BINDING],
        ref=replace(RMSD_BINDING, version="advisory"),
        protocol_ref=advisory.ref,
    )
    context.extensions.register_binding(binding)
    prepared = praxis.prepare(
        praxis.MethodRequest(
            CAPABILITY, inputs, protocol_ref=advisory.ref, binding_ref=binding.ref
        ),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready and prepared.findings[-1].outcome == "undetermined"


def test_undeclared_parameters_block_preparation(workspace, inputs):
    catalog, context = workspace
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, {"surprise": True}, RMSD, RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready and any("Undeclared" in item for item in prepared.reasons)


def test_recipe_cannot_skip_declared_step(workspace, inputs):
    catalog, context = workspace
    binding = context.extensions.bindings[RMSD_BINDING]
    ref = replace(RMSD_BINDING, identifier="fixture.hidden_recipe")
    context.extensions.register_binding(
        replace(
            binding,
            ref=ref,
            recipe=lambda inputs, config, recipe_context: {"score": 0, "metric": "fictional"},
        )
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=ref),
        catalog=catalog,
        context=context,
    )
    with pytest.raises(ContractError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="missing-step")
    attempt = context.records.attempt("missing-step")
    assert attempt.contract_status == "violated"
    assert attempt.outputs["score"] == 0  # partial outputs retained without a success claim


def test_only_started_record_is_reported_as_incomplete(workspace, prepared):
    catalog, context = workspace
    attempt = praxis.AttemptRecord(
        "interrupted",
        prepared.identifier,
        "2026-10-08",
        None,
        "running",
        "unassessed",
        "pending",
        (),
        (),
        None,
        {},
    )
    context.records.save_attempt(attempt)
    assert context.records.attempt("interrupted").operational_status == "incomplete"
    audit = praxis.audit_execution("interrupted", records=context.records)
    assert any("No retained terminal" in item for item in audit.findings)


def test_unavailable_dependency_is_separate_from_scientific_applicability(workspace, inputs):
    catalog, context = workspace
    binding = context.extensions.bindings[RMSD_BINDING]
    reference = replace(RMSD_BINDING, identifier="fixture.unavailable_engine")
    context.extensions.register_binding(
        replace(binding, ref=reference, dependencies=("_praxis_nonexistent_scientific_engine",))
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=reference),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready and all(item.outcome == "passed" for item in prepared.findings)
    assert any("dependency" in item for item in prepared.reasons)
