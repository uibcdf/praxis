"""Regressions for the six defects identified in the implementation review."""

import os
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, INPUT_CHECK, RMSD, RMSD_BINDING

import praxis
from praxis.errors import ConflictError, NotReadyError, RecordingError
from praxis.recording import NoRecorder


def request(inputs):
    return praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING)


def specification(inputs, replicates=3):
    return praxis.BenchmarkSpec(
        praxis.MethodRef("benchmark", "review", "1"),
        "Review regression",
        CAPABILITY,
        (praxis.BenchmarkCase("paired", inputs, "synthetic paired coordinates"),),
        (praxis.BenchmarkMethod(RMSD, RMSD_BINDING),),
        praxis.MethodRef("extension", "review.metric", "1"),
        "dimensionless score",
        "One explicit evaluator",
        replicates=replicates,
    )


def test_registered_extensions_cannot_be_overwritten_or_removed(workspace):
    _, context = workspace
    binding = context.extensions.bindings[RMSD_BINDING]
    with pytest.raises(TypeError):
        context.extensions.bindings[RMSD_BINDING] = binding
    with pytest.raises(TypeError):
        del context.extensions.checkers[INPUT_CHECK]
    with pytest.raises(AttributeError):
        context.extensions.bindings = {}
    with pytest.raises(ConflictError):
        context.extensions.register_binding(binding)
    with pytest.raises(ConflictError):
        context.extensions.register_checker(INPUT_CHECK, lambda *args: None)


@pytest.mark.parametrize("changed", ["recipe", "checker"])
def test_replacing_registry_under_same_references_cannot_change_prepared_method(
    workspace, prepared, changed
):
    catalog, context = workspace
    calls = []

    def replacement(*args):
        calls.append(1)
        return {"score": 999, "metric": "fictional"}

    original = (
        context.extensions.bindings[RMSD_BINDING].recipe
        if changed == "recipe"
        else context.extensions.checkers[INPUT_CHECK]
    )
    # Keep the declared Python name too: loaded code must distinguish the functions.
    replacement.__module__ = original.__module__
    replacement.__qualname__ = original.__qualname__
    registry = praxis.Extensions()
    for binding in context.extensions.bindings.values():
        registry.register_binding(
            replace(binding, recipe=replacement)
            if changed == "recipe" and binding.ref == RMSD_BINDING
            else binding
        )
    for ref, checker in context.extensions.checkers.items():
        registry.register_checker(
            ref, replacement if changed == "checker" and ref == INPUT_CHECK else checker
        )
    context.extensions = registry
    with pytest.raises(NotReadyError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="changed-code")
    assert calls == []
    assert context.records.attempt("changed-code").operational_status == "blocked"


def test_mutating_loaded_code_is_detected_without_registry_replacement(
    workspace, prepared, monkeypatch
):
    catalog, context = workspace

    def replacement(inputs, configuration, context):
        return {"score": 999, "metric": "fictional"}

    recipe = context.extensions.bindings[RMSD_BINDING].recipe
    monkeypatch.setattr(recipe, "__code__", replacement.__code__)
    with pytest.raises(NotReadyError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="mutated-code")
    assert not context.records.attempt("mutated-code").steps


def minimal_method(
    workspace,
    *,
    input_validator="finite_number",
    output_validator="finite_number",
    output=1,
    unit=None,
    field_checker=None,
):
    catalog, context = workspace
    cap_ref = praxis.MethodRef("capability", "review.scalar", "1")
    prot_ref = praxis.MethodRef("protocol", "review.scalar", "1")
    binding_ref = praxis.MethodRef("extension", "review.scalar", "1")
    capability = praxis.Capability(
        cap_ref,
        "Scalar fixture",
        "Return a declared scalar",
        (
            praxis.Field(
                "number",
                "Input",
                "finite number",
                unit,
                validator=input_validator,
                checker_ref=field_checker,
            ),
        ),
        (praxis.Field("score", "Output", "finite number", validator=output_validator),),
    )
    protocol = praxis.Protocol(
        prot_ref,
        "Scalar fixture",
        "Copy a scalar",
        cap_ref,
        (praxis.Step("copy", "Copy", "fixture", "copy"),),
        ("Synthetic fixture",),
    )

    def recipe(inputs, configuration, recipe_context):
        with recipe_context.step("copy"):
            return {"score": output}

    catalog.register(capability)
    catalog.register(protocol)
    context.extensions.register_binding(
        praxis.ImplementationBinding(binding_ref, prot_ref, recipe, "Synthetic scalar fixture")
    )
    return capability, protocol, binding_ref


@pytest.mark.parametrize("inputs", [{}, {"number": None}, {"number": True}, {"number": "3"}])
def test_field_contract_applies_even_without_authored_requirements(workspace, inputs):
    catalog, context = workspace
    capability, protocol, binding = minimal_method(workspace)
    applicability = praxis.assess_applicability(
        capability, protocol, inputs, {}, context.extensions
    )
    assert applicability.outcome == "inapplicable"
    prepared = praxis.prepare(
        praxis.MethodRequest(
            capability.ref, inputs, protocol_ref=protocol.ref, binding_ref=binding
        ),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready


@pytest.mark.parametrize("output", [None, True, "3", [], {}])
def test_present_but_invalid_output_cannot_support_contract(workspace, output):
    catalog, context = workspace
    capability, protocol, binding = minimal_method(workspace, output=output)
    prepared = praxis.prepare(
        praxis.MethodRequest(
            capability.ref, {"number": 1}, protocol_ref=protocol.ref, binding_ref=binding
        ),
        catalog=catalog,
        context=context,
    )
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.operational_status == "completed"
    assert attempt.contract_status == "unsupported"
    assert attempt.findings[-1].outcome == "failed"
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


@pytest.mark.parametrize("options", [{"input_validator": None}, {"unit": "nanometer"}])
def test_descriptions_and_unit_labels_do_not_invent_validation(workspace, options):
    _, context = workspace
    capability, protocol, _ = minimal_method(workspace, **options)
    report = praxis.assess_applicability(
        capability, protocol, {"number": 1}, {}, context.extensions
    )
    assert report.outcome == "undetermined"


def test_missing_output_validator_cannot_support_contract(workspace):
    catalog, context = workspace
    capability, protocol, binding = minimal_method(workspace, output_validator=None)
    prepared = praxis.prepare(
        praxis.MethodRequest(
            capability.ref, {"number": 1}, protocol_ref=protocol.ref, binding_ref=binding
        ),
        catalog=catalog,
        context=context,
    )
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.contract_status == "unsupported"
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "unverified"
    )


def test_custom_field_checker_is_pinned_and_can_establish_a_representation(workspace):
    catalog, context = workspace
    ref = praxis.MethodRef("extension", "review.field", "1")
    context.extensions.register_checker(
        ref,
        lambda inputs, config, outputs: praxis.CheckResult(
            "passed", "Provider representation inspected"
        ),
    )
    capability, protocol, binding = minimal_method(
        workspace, input_validator=None, field_checker=ref
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(
            capability.ref, {"number": 1}, protocol_ref=protocol.ref, binding_ref=binding
        ),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready and prepared.checkers[0]["ref"] == ref.to_dict()
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


def test_protocol_association_is_part_of_direct_applicability(workspace, inputs):
    catalog, context = workspace
    protocol = replace(catalog.get(RMSD), capability_ref=replace(CAPABILITY, version="other"))
    report = praxis.assess_applicability(
        catalog.get(CAPABILITY), protocol, inputs, {}, context.extensions
    )
    assert report.outcome == "inapplicable"


def test_interrupted_benchmark_retains_previous_metric_and_full_schedule(workspace, inputs):
    catalog, context = workspace
    spec = specification(inputs)
    calls = []
    native = KeyboardInterrupt()

    def evaluator(inputs, outputs):
        calls.append(1)
        if len(calls) == 2:
            raise native
        return 0.75

    with pytest.raises(KeyboardInterrupt) as caught:
        praxis.run_benchmark(
            spec,
            catalog=catalog,
            context=context,
            evaluators={spec.evaluator_ref: evaluator},
            identifier="interrupt",
        )
    assert caught.value is native
    assert "Praxis benchmark: interrupt" in caught.value.__notes__
    partial = praxis.load_benchmark("interrupt", records=context.records)
    assert partial.status == "interrupted" and len(partial.rows) == 3
    assert partial.rows[0]["metric_value"] == 0.75
    assert partial.rows[1]["method_status"] == "completed"
    assert partial.rows[1]["metric_status"] == "interrupted"
    assert partial.rows[2]["method_status"] == "not_started"
    assert "1/3" in praxis.render(praxis.benchmark_document(partial))
    assert len(calls) == 2


def test_abrupt_process_exit_keeps_benchmark_checkpoints_readable(workspace, inputs, tmp_path):
    code = """import os, sys, praxis
from local_comparison import build_fixture, CAPABILITY, RMSD, RMSD_BINDING
catalog, context = build_fixture(sys.argv[1])
spec = praxis.BenchmarkSpec(praxis.MethodRef("benchmark", "abrupt", "1"), "Abrupt exit fixture",
    CAPABILITY, (praxis.BenchmarkCase("case", {"left": [[0,0,0]], "right": [[1,0,0]]}, "paired"),),
    (praxis.BenchmarkMethod(RMSD, RMSD_BINDING),), praxis.MethodRef("extension", "metric", "1"),
    "dimensionless", "fixture", replicates=3)
calls = []
def evaluate(inputs, outputs):
    calls.append(1)
    if len(calls) == 2:
        os._exit(23)
    return 0.5
praxis.run_benchmark(spec, catalog=catalog, context=context,
    evaluators={spec.evaluator_ref: evaluate}, identifier="abrupt")
"""
    root = tmp_path / "child"
    completed = subprocess.run(
        [sys.executable, "-B", "-c", code, str(root)],
        check=False,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
    )
    assert completed.returncode == 23
    partial = praxis.load_benchmark("abrupt", records=praxis.MethodRecords(root / "records"))
    assert partial.status == "incomplete" and partial.finished is None
    assert partial.rows[0]["metric_value"] == 0.5
    assert partial.rows[1]["method_status"] == "completed"
    assert partial.rows[1]["metric_status"] == "incomplete"
    assert partial.rows[2]["metric_value"] is None
    assert "1/3" in praxis.render(praxis.benchmark_document(partial))


@pytest.mark.parametrize(
    "alteration,code",
    [
        ({"findings": ()}, "check_coverage"),
        ({"steps": ()}, "step_coverage"),
        ({"outputs": {"score": None, "metric": "paired_rmsd"}}, "field_evidence"),
        ({"implementations": ()}, "implementation_evidence"),
    ],
)
def test_audit_detects_claims_without_matching_evidence(workspace, prepared, alteration, code):
    catalog, context = workspace
    _, actual = praxis.execute(prepared, catalog=catalog, context=context)
    assert (
        praxis.audit_execution(actual.identifier, records=context.records).outcome == "consistent"
    )
    forged = replace(actual, identifier="forged", **alteration)
    context.records.save_attempt(forged)
    audit = praxis.audit_execution("forged", records=context.records)
    assert audit.outcome == "violated"
    assert code in {issue.code for issue in audit.issues}


def test_audit_rejects_duplicate_or_differently_scoped_check_evidence(workspace, prepared):
    catalog, context = workspace
    _, actual = praxis.execute(prepared, catalog=catalog, context=context)
    first = replace(actual.findings[0], mandatory=False)
    forged = replace(actual, identifier="duplicate", findings=(first, *actual.findings))
    context.records.save_attempt(forged)
    codes = {
        issue.code for issue in praxis.audit_execution("duplicate", records=context.records).issues
    }
    assert {"duplicate_check", "check_identity"} <= codes


class FaultyEvaluationRecorder(NoRecorder):
    def __init__(self, stage, operation_name="praxis.evaluate"):
        self.stage = stage
        self.operation_name = operation_name
        self.sequence = 0

    def reference(self, path, identifier):
        return {"id": identifier}

    def coverage(self, correlations):
        return "complete_declared_boundaries" if correlations else "omitted_by_policy"

    @contextmanager
    def operation(self, name, **kwargs):
        evaluation = name == self.operation_name
        if evaluation and self.stage == "enter":
            raise RecordingError("Evaluation recording start failed")
        self.sequence += 1
        sequence = self.sequence
        stage = self.stage

        class Operation:
            def correlation(self):
                return {"operation_id": str(sequence)}

            def output(self, name, value):
                if evaluation and stage == "output":
                    raise RecordingError("Evaluation output recording failed")

        yield Operation()
        if evaluation and self.stage == "exit":
            raise RecordingError("Evaluation terminal recording failed")


@pytest.mark.parametrize("stage", ["enter", "output", "exit"])
def test_metric_and_recording_failures_remain_separate(workspace, inputs, stage):
    catalog, context = workspace
    context.recorder = FaultyEvaluationRecorder(stage)
    spec = specification(inputs, replicates=1)
    calls = []

    def evaluator(inputs, outputs):
        calls.append(1)
        return 0.25

    result = praxis.run_benchmark(
        spec, catalog=catalog, context=context, evaluators={spec.evaluator_ref: evaluator}
    )
    row = result.rows[0]
    assert row["method_status"] == "completed"
    assert row["evaluation_recording_status"] == "gap"
    assert row["evaluation_failure_type"] is None
    assert row["recording_failure_type"] == "RecordingError"
    assert row["metric_status"] == ("not_started" if stage == "enter" else "available")
    assert row["metric_value"] == (None if stage == "enter" else 0.25)
    assert len(calls) == (0 if stage == "enter" else 1)
    assert praxis.load_benchmark(result.identifier, records=context.records) == result


@pytest.mark.parametrize("stage", ["started", "finished"])
@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("error_type", [OSError, KeyboardInterrupt])
def test_persistence_failure_exposes_attempt_identifier(
    workspace, prepared, monkeypatch, stage, explicit, error_type
):
    catalog, context = workspace
    native = error_type("Snapshot fault")
    save = context.records.save_attempt
    seen = []

    def fault(attempt):
        seen.append(attempt.identifier)
        if (attempt.finished is None) == (stage == "started"):
            raise native
        return save(attempt)

    monkeypatch.setattr(context.records, "save_attempt", fault)
    kwargs = {"identifier": "known-attempt"} if explicit else {}
    with pytest.raises(error_type) as caught:
        praxis.execute(prepared, catalog=catalog, context=context, **kwargs)
    assert caught.value is native
    assert "Praxis method attempt: " + seen[0] in native.__notes__
    if stage == "finished":
        assert context.records.attempt(seen[0]).operational_status == "incomplete"


def test_audit_checks_the_saved_conclusion_in_both_directions(workspace, prepared):
    catalog, context = workspace
    _, actual = praxis.execute(prepared, catalog=catalog, context=context)
    context.records.save_attempt(
        replace(actual, identifier="wrong-conclusion", contract_status="unsupported")
    )
    audit = praxis.audit_execution("wrong-conclusion", records=context.records)
    assert audit.outcome == "violated"
    assert "conclusion_mismatch" in {issue.code for issue in audit.issues}


def test_native_evaluator_error_is_classified_by_its_boundary(workspace, inputs):
    catalog, context = workspace
    spec = specification(inputs, replicates=1)

    def evaluator(inputs, outputs):
        raise RecordingError("Native evaluator error, not the recording adapter")

    result = praxis.run_benchmark(
        spec, catalog=catalog, context=context, evaluators={spec.evaluator_ref: evaluator}
    )
    row = result.rows[0]
    assert row["metric_status"] == "evaluator_failed"
    assert row["evaluation_failure_type"] == "RecordingError"
    assert row["evaluation_recording_status"] == "not_requested"
    assert row["recording_failure_type"] is None


@pytest.mark.parametrize("stage", ["output", "exit"])
def test_recording_failure_after_method_checks_does_not_invalidate_their_evidence(
    workspace, prepared, stage
):
    catalog, context = workspace
    context.recorder = FaultyEvaluationRecorder(stage, operation_name="praxis.execute")
    with pytest.raises(RecordingError):
        praxis.execute(
            prepared, catalog=catalog, context=context, identifier="method-recording-gap"
        )
    attempt = context.records.attempt("method-recording-gap")
    assert attempt.operational_status == "failed"
    assert attempt.contract_status == "supported"
    assert attempt.recording_status == "gap"
    audit = praxis.audit_execution(attempt.identifier, records=context.records)
    assert audit.outcome == "unverified"
    assert {issue.code for issue in audit.issues} == {"recording_gap"}


def test_checkpoint_fault_preserves_native_error_and_exposes_benchmark_id(
    workspace, inputs, monkeypatch
):
    catalog, context = workspace
    spec = specification(inputs, replicates=1)
    put = context.records.store.put
    native = OSError("Checkpoint fault")

    def fault(identity, document):
        if identity.get("kind") == "benchmark-row" and identity["stage"] == "metric_computed":
            raise native
        return put(identity, document)

    monkeypatch.setattr(context.records.store, "put", fault)
    with pytest.raises(OSError) as caught:
        praxis.run_benchmark(
            spec,
            catalog=catalog,
            context=context,
            evaluators={spec.evaluator_ref: lambda inputs, outputs: 0.25},
            identifier="checkpoint-fault",
        )
    assert caught.value is native and "Praxis benchmark: checkpoint-fault" in native.__notes__
    partial = praxis.load_benchmark("checkpoint-fault", records=context.records)
    assert partial.status == "failed"
    assert partial.rows[0]["metric_value"] == 0.25
    assert partial.rows[0]["evaluation_failure_type"] is None


def test_terminal_benchmark_persistence_fault_keeps_checkpoints_readable(
    workspace, inputs, monkeypatch
):
    catalog, context = workspace
    spec = specification(inputs, replicates=1)
    put = context.records.store.put
    native = OSError("Terminal benchmark snapshot fault")

    def fault(identity, document):
        if identity.get("kind") == "benchmark-result":
            raise native
        return put(identity, document)

    monkeypatch.setattr(context.records.store, "put", fault)
    with pytest.raises(OSError) as caught:
        praxis.run_benchmark(
            spec,
            catalog=catalog,
            context=context,
            evaluators={spec.evaluator_ref: lambda inputs, outputs: 0.25},
        )
    assert caught.value is native
    identifier = next(
        note.removeprefix("Praxis benchmark: ")
        for note in native.__notes__
        if note.startswith("Praxis benchmark: ")
    )
    partial = praxis.load_benchmark(identifier, records=context.records)
    assert partial.status == "incomplete"
    assert partial.rows[0]["metric_status"] == "available"
    assert partial.rows[0]["metric_value"] == 0.25


def test_reusing_benchmark_id_cannot_replace_prior_partial_progress(workspace, inputs, monkeypatch):
    catalog, context = workspace
    spec = specification(inputs, replicates=1)
    put = context.records.store.put

    def fault(identity, document):
        if identity.get("kind") == "benchmark-result":
            raise OSError("Terminal snapshot fault")
        return put(identity, document)

    monkeypatch.setattr(context.records.store, "put", fault)
    with pytest.raises(OSError):
        praxis.run_benchmark(
            spec,
            catalog=catalog,
            context=context,
            evaluators={spec.evaluator_ref: lambda inputs, outputs: 0.25},
            identifier="retained-progress",
        )
    previous = praxis.load_benchmark("retained-progress", records=context.records)
    monkeypatch.setattr(context.records.store, "put", put)
    with pytest.raises(ConflictError):
        praxis.run_benchmark(
            spec,
            catalog=catalog,
            context=context,
            evaluators={spec.evaluator_ref: lambda inputs, outputs: 999},
            identifier="retained-progress",
        )
    assert praxis.load_benchmark("retained-progress", records=context.records) == previous
    assert previous.rows[0]["metric_value"] == 0.25
