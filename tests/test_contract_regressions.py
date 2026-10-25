from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING

import praxis
from praxis.errors import ContractError, NotReadyError, WaitingForReview
from praxis.provenance import invocation_digest


def _prepare_runtime_guard(workspace, inputs, requirement):
    catalog, context = workspace

    def recipe(inputs, configuration, runtime):
        with runtime.step("measure"):
            try:
                runtime.check(requirement.identifier)
            except (ContractError, NotReadyError, WaitingForReview):
                pass
        return {"score": 0, "metric": "fixture"}

    protocol = replace(
        catalog.get(RMSD),
        ref=replace(RMSD, version="runtime-guard"),
        requirements=(requirement,),
    )
    catalog.register(protocol)
    binding = replace(
        context.extensions.bindings[RMSD_BINDING],
        ref=replace(RMSD_BINDING, version="runtime-guard"),
        protocol_ref=protocol.ref,
        recipe=recipe,
    )
    context.extensions.register_binding(binding)
    return praxis.prepare(
        praxis.MethodRequest(
            CAPABILITY, inputs, protocol_ref=protocol.ref, binding_ref=binding.ref
        ),
        catalog=catalog,
        context=context,
    )


@pytest.mark.parametrize("mandatory", [True, False])
@pytest.mark.parametrize("outcome", ["failed", "undetermined", "skipped", "checker_error"])
def test_caught_runtime_check_cannot_establish_mandatory_compliance(
    workspace, inputs, mandatory, outcome
):
    catalog, context = workspace
    checker = praxis.MethodRef("extension", "fixture.runtime_guard", "1")

    def check(*args):
        if outcome == "checker_error":
            raise ValueError("Synthetic checker failure")
        return praxis.CheckResult(outcome, "Synthetic runtime finding")

    context.extensions.register_checker(checker, check)
    prepared = _prepare_runtime_guard(
        workspace,
        inputs,
        praxis.Requirement(
            "guard",
            "Runtime guarantee",
            phase="runtime",
            mandatory=mandatory,
            checker_ref=checker,
        ),
    )
    assert prepared.ready
    if mandatory:
        error = ContractError if outcome == "failed" else NotReadyError
        with pytest.raises(error):
            praxis.execute(prepared, catalog=catalog, context=context, identifier="caught-runtime")
    else:
        praxis.execute(prepared, catalog=catalog, context=context, identifier="caught-runtime")
    attempt = context.records.attempt("caught-runtime")
    runtime_findings = [f for f in attempt.findings if f.phase == "runtime"]
    assert len(runtime_findings) == 1 and runtime_findings[0].outcome == outcome
    assert attempt.outputs == {"score": 0, "metric": "fixture"}
    assert attempt.steps[0]["status"] == "completed"
    assert attempt.contract_status == (
        "violated"
        if mandatory and outcome == "failed"
        else "unassessed"
        if mandatory
        else "supported"
    )
    assert attempt.operational_status == (
        "failed" if mandatory and outcome == "failed" else "blocked" if mandatory else "completed"
    )
    assert praxis.audit_execution(attempt.identifier, records=context.records).outcome != "violated"


@pytest.mark.parametrize("outcome", ["failed", "undetermined"])
def test_caught_human_runtime_gate_preserves_rejection_or_waiting(workspace, inputs, outcome):
    catalog, context = workspace
    prepared = _prepare_runtime_guard(
        workspace,
        inputs,
        praxis.Requirement(
            "review",
            "Scoped human review",
            phase="runtime",
            review_required=True,
            human_authorities=("fixture reviewer",),
        ),
    )
    context.reviews = (
        praxis.EvidenceRecord(
            "fixture:review",
            "human",
            "review",
            invocation_digest(
                CAPABILITY, prepared.selection.protocol_ref, prepared.inputs, prepared.configuration
            ),
            outcome,
            "boundary",
            "fixture actor",
            "fixture reviewer",
            "2026-10-24",
        ),
    )
    with pytest.raises(ContractError if outcome == "failed" else WaitingForReview):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="caught-human")
    attempt = context.records.attempt("caught-human")
    assert attempt.operational_status == ("failed" if outcome == "failed" else "waiting")
    assert attempt.contract_status == ("violated" if outcome == "failed" else "unassessed")
    assert attempt.findings[-1].outcome == outcome


def test_caught_step_failure_cannot_be_relabelled_success(workspace, inputs):
    catalog, context = workspace
    original = context.extensions.bindings[RMSD_BINDING]

    def recipe(inputs, configuration, steps):
        try:
            with steps.step("measure"):
                raise ValueError("provider failed but recipe swallowed it")
        except ValueError:
            pass
        return {"score": 0, "metric": "fictional"}

    reference = replace(RMSD_BINDING, identifier="fixture.caught_failure")
    context.extensions.register_binding(replace(original, ref=reference, recipe=recipe))
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=reference),
        catalog=catalog,
        context=context,
    )
    with pytest.raises(ContractError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="swallowed-failure")
    assert context.records.attempt("swallowed-failure").contract_status == "violated"


def test_defaults_are_frozen_before_later_protocol_revision(workspace, inputs):
    catalog, context = workspace
    original = catalog.get(RMSD)
    reference = replace(RMSD, version="with-default")
    protocol = replace(
        original,
        ref=reference,
        parameters=(praxis.Parameter("fixture_option", "Fictional option", False, {"limit": 3}),),
    )
    catalog.register(protocol)
    binding = replace(
        context.extensions.bindings[RMSD_BINDING],
        ref=replace(RMSD_BINDING, version="with-default"),
        protocol_ref=reference,
    )
    context.extensions.register_binding(binding)
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=reference, binding_ref=binding.ref),
        catalog=catalog,
        context=context,
    )
    catalog.register(
        replace(
            protocol,
            ref=replace(reference, version="next"),
            parameters=(
                praxis.Parameter("fixture_option", "Changed option", False, {"limit": 99}),
            ),
        )
    )
    assert context.records.prepared(prepared.identifier).configuration == {
        "fixture_option": {"limit": 3}
    }
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.operational_status == "completed"
