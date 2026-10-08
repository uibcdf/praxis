"""Acceptance exercises for catalog curation, scoped selection and richer local execution."""

from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING

import praxis
from praxis._quantities import duration_record
from praxis._serialization import digest
from praxis.errors import (
    CancelledError,
    ConflictError,
    ContractError,
    DefinitionError,
    NotReadyError,
    WaitingForReview,
)
from praxis.provenance import invocation_digest


def variant(workspace, inputs, *, recipe=None, **changes):
    catalog, context = workspace
    protocol = replace(catalog.get(RMSD), ref=replace(RMSD, version="expanded"), **changes)
    catalog.register(protocol)
    binding = replace(
        context.extensions.bindings[RMSD_BINDING],
        ref=replace(RMSD_BINDING, version="expanded"),
        protocol_ref=protocol.ref,
        recipe=recipe or context.extensions.bindings[RMSD_BINDING].recipe,
    )
    context.extensions.register_binding(binding)
    request = praxis.MethodRequest(
        CAPABILITY, inputs, protocol_ref=protocol.ref, binding_ref=binding.ref
    )
    return protocol, binding, request


def assessment(subject, *, version="1", outcome="supported", scenario=None, supersedes=None):
    return praxis.Assessment(
        praxis.MethodRef("assessment", "scoped", version),
        subject,
        "reviewer",
        "method review",
        "2026-10-08",
        "Declared scope",
        ("contract",),
        ("Evidence inspected",),
        outcome,
        supporting_refs=("retained:provider:result@1",),
        scenario=scenario or {},
        supersedes=supersedes,
    )


def test_scoped_assessments_preserve_conflicts_and_explicit_revisions(workspace):
    catalog, _ = workspace
    scenario = {"system": "protein", "environment": "aqueous"}
    first = assessment(RMSD, scenario=scenario)
    challenged = assessment(RMSD, version="2", outcome="challenged", scenario=scenario)
    catalog.register(first)
    catalog.register(challenged)
    assert catalog.status_for(RMSD, scenario=scenario)["validation"] == "conflicting"
    assert catalog.status_for(RMSD, scenario={"system": "protein"})["validation"] == "unassessed"
    replacement = assessment(RMSD, version="3", scenario=scenario, supersedes=challenged.ref)
    catalog.register(replacement)
    assert len(catalog.assessments_for(RMSD)) == 3
    assert catalog.status_for(RMSD, scenario=scenario)["validation"] == "supported"


def test_admission_and_promotion_require_exact_content_and_assessments(workspace):
    catalog, _ = workspace
    definition = catalog.get(RMSD)
    review = praxis.AdmissionReview(
        praxis.MethodRef("review", "admission", "1"),
        RMSD,
        digest(definition),
        "proposer",
        "maintainer",
        "reviewer",
        "method authority",
        "2026-10-08",
        "admitted_experimental",
        "Procedure is meaningful; scientific benefit remains unassessed",
    )
    catalog.register(review)
    assert catalog.reviews_for(RMSD) == (review,)
    with pytest.raises(DefinitionError):
        catalog.register(
            replace(review, ref=replace(review.ref, version="wrong"), subject_digest="wrong")
        )
    with pytest.raises(DefinitionError):
        replace(review, outcome="promoted")
    supported = assessment(RMSD)
    catalog.register(supported)
    promoted = replace(
        review,
        ref=replace(review.ref, version="2"),
        outcome="promoted",
        evidence=(supported.ref,),
        supersedes=review.ref,
        source_workflow="retained:workflow@1",
    )
    catalog.register(promoted)
    assert catalog.reviews_for(RMSD, active=True) == (promoted,)
    assert catalog.get(RMSD).status == "experimental"  # judgment does not rewrite procedure


def test_withdrawal_preserves_definition_but_blocks_old_preparation(workspace, prepared):
    catalog, context = workspace
    before = catalog.get(RMSD)
    event = praxis.MethodStatus(
        praxis.MethodRef("status", "withdrawal", "1"),
        RMSD,
        "withdrawn",
        "maintainer",
        "catalog authority",
        "2026-10-08",
        "Coverage defect",
    )
    catalog.register(event)
    assert catalog.get(RMSD) == before
    with pytest.raises(NotReadyError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="withdrawn")
    assert context.records.attempt("withdrawn").operational_status == "blocked"


def test_catalog_bundle_reopens_all_history_and_rejects_conflicts_before_writing(
    workspace, tmp_path
):
    catalog, _ = workspace
    catalog.register(assessment(RMSD))
    bundle = catalog.export_bundle()
    reopened = praxis.Catalog.open(tmp_path / "portable")
    reopened.import_bundle(bundle)
    assert reopened.export_bundle() == bundle
    conflicting = replace(catalog.get(RMSD), title="Conflicting scientific definition")
    bad = {**bundle, "documents": [*bundle["documents"], conflicting.to_dict()]}
    bad["digest"] = digest(bad["documents"])
    empty = praxis.Catalog.open(tmp_path / "empty")
    with pytest.raises(ConflictError):
        empty.import_bundle(bad)
    assert tuple(empty.definitions()) == ()


def test_schema_migration_is_explicit_and_preserves_scientific_identity(workspace, tmp_path):
    catalog, _ = workspace
    bundle = catalog.export_bundle()
    legacy = {**bundle["documents"][0], "schema": "legacy.capability/0"}
    bundle["documents"][0] = legacy
    bundle["digest"] = digest(bundle["documents"])
    restored = praxis.Catalog.open(tmp_path / "migration")
    with pytest.raises(DefinitionError):
        restored.import_bundle(bundle)

    def upgrade(document):
        return {**document, "schema": "praxis.capability/0.1"}

    restored.import_bundle(bundle, migrations={"legacy.capability/0": upgrade})
    assert restored.get(CAPABILITY) == catalog.get(CAPABILITY)
    assert legacy["schema"] == "legacy.capability/0"


def test_discovery_filters_do_not_claim_input_applicability(workspace):
    catalog, _ = workspace
    result = catalog.query(kind="capability", inputs=("left", "right"), text="paired")
    assert len(result) == 1
    assert result[0]["definition"]["ref"] == CAPABILITY.to_dict()
    assert "not checked" in result[0]["basis"]


def test_protocol_only_request_resolves_capability(workspace, inputs):
    catalog, context = workspace
    prepared = praxis.prepare(
        praxis.MethodRequest(inputs=inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready and prepared.capability_ref == CAPABILITY


def test_resource_policy_preserves_units_scenario_and_abstention(workspace, inputs):
    catalog, context = workspace
    profile = praxis.ResourceProfile(
        fidelity="full paired RMSD",
        cost_class="small",
        expected_duration=duration_record(1, "protocol.expected_duration"),
        basis="estimated",
        conditions={"scope": "small paired coordinates"},
    )
    protocol, _, _ = variant(workspace, inputs, resources=profile)
    policy = praxis.SelectionPolicy(
        criteria={
            "fidelity": profile.fidelity,
            "max_expected_duration": duration_record(2, "selection.max_expected_duration"),
        },
        scenario=profile.conditions,
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, selection_policy=policy),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready and prepared.selection.protocol_ref == protocol.ref
    assert any(item["outcome"] == "undetermined" for item in prepared.selection.candidate_findings)
    strict = replace(
        policy,
        criteria={
            **policy.criteria,
            "max_expected_duration": duration_record(0.1, "selection.max_expected_duration"),
        },
    )
    rejected = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, selection_policy=strict),
        catalog=catalog,
        context=context,
    )
    assert not rejected.ready and rejected.selection.protocol_ref is None


def test_suitability_revision_does_not_rewrite_protocol_and_comparison_keeps_basis(workspace):
    catalog, _ = workspace
    old = catalog.get(RMSD)
    statement = praxis.SuitabilityStatement(
        praxis.MethodRef("suitability", "rmsd", "1"),
        RMSD,
        {"purpose": "paired displacement"},
        "favorable",
        ("retain all pairs",),
        "reviewer",
        "method review",
        "2026-10-08",
        "Suitable for the declared all-pair statistic",
        basis="measured",
        supporting_refs=("retained:benchmark@1",),
    )
    catalog.register(statement)
    revised = replace(
        statement,
        ref=replace(statement.ref, version="2"),
        outcome="discouraged",
        rationale="Prefer another statistic for this purpose",
        supersedes=statement.ref,
    )
    catalog.register(revised)
    assert catalog.get(RMSD) == old
    assert len(catalog.suitability_for(RMSD)) == 2
    document = praxis.comparison_document((RMSD,), catalog=catalog, scenario=statement.scenario)
    assert "discouraged" in praxis.render(document) and str(statement.ref) in praxis.render(
        document
    )


@pytest.mark.parametrize("value,ready", [(2, True), (0, False), (True, False), ("2", False)])
def test_parameter_contracts_gate_configuration(workspace, inputs, value, ready):
    catalog, context = workspace
    _, _, request = variant(
        workspace,
        inputs,
        parameters=(praxis.Parameter("count", "Positive count", validator="number", minimum=1),),
    )
    request.configuration = {"count": value}
    prepared = praxis.prepare(request, catalog=catalog, context=context)
    assert prepared.ready == ready
    if ready:
        _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
        assert (
            praxis.audit_execution(attempt.identifier, records=context.records).outcome
            == "consistent"
        )


def test_quantity_parameter_uses_shared_codec_field_units_and_bounds(workspace, inputs):
    import pyunitwizard as puw

    catalog, context = workspace
    parameter = praxis.Parameter(
        "radius", "Declared radius", validator="quantity", unit="nanometer", minimum=0.1, maximum=1
    )
    _, _, request = variant(workspace, inputs, parameters=(parameter,))
    request.configuration = {
        "radius": puw.QuantityRecord.from_quantity(
            puw.quantity(5, "angstrom", form="pint"),
            field="protocol.parameter/radius",
            unit="angstrom",
        ).to_dict()
    }
    prepared = praxis.prepare(request, catalog=catalog, context=context)
    assert prepared.ready
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )
    request.configuration["radius"] = duration_record(1, "protocol.parameter/radius")
    assert not praxis.prepare(request, catalog=catalog, context=context).ready


def test_environment_constraints_rechecked_and_actor_retained(workspace, prepared):
    catalog, context = workspace
    context.actor = "application:scientist"
    context.authority = "controlled local workflow"
    context.environment_requirements = {"packages": {"numpy": "impossible-version"}}
    request = praxis.MethodRequest(
        CAPABILITY, prepared.inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING
    )
    rejected = praxis.prepare(request, catalog=catalog, context=context)
    assert not rejected.ready
    assert rejected.actor == context.actor
    context.environment_requirements = {}
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.actor == context.actor and attempt.environment["machine"]


def test_bounded_repetition_and_recorded_branch(workspace, inputs):
    catalog, context = workspace
    condition = praxis.MethodRef("extension", "false.branch", "1")
    context.extensions.register_checker(
        condition, lambda *args: praxis.CheckResult("failed", "Declared optional stage not needed")
    )
    steps = (
        praxis.Step(
            "optional", "Optional measurement", "fixture", "optional", condition_ref=condition
        ),
        praxis.Step("measure", "Repeated measurement", "fixture", "measure", repeat=2),
    )

    def recipe(inputs, configuration, runtime):
        assert not runtime.branch("optional")
        for _ in range(2):
            with runtime.step("measure"):
                pass
        return {"score": 0, "metric": "fixture"}

    _, _, request = variant(workspace, inputs, recipe=recipe, steps=steps)
    prepared = praxis.prepare(request, catalog=catalog, context=context)
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert [step["status"] for step in attempt.steps] == ["skipped", "completed", "completed"]
    assert [step["iteration"] for step in attempt.steps] == [0, 0, 1]
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


def test_cancellation_blocks_next_declared_boundary_and_preserves_record(workspace, prepared):
    catalog, context = workspace
    context.cancelled = True
    with pytest.raises(CancelledError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="cancelled")
    assert context.records.attempt("cancelled").operational_status == "cancelled"
    assert not context.records.attempt("cancelled").steps


def test_runtime_human_review_waits_then_explicit_retry_consumes_scoped_evidence(workspace, inputs):
    catalog, context = workspace
    requirement = praxis.Requirement(
        "approval",
        "Review this invocation",
        "runtime",
        review_required=True,
        human_authorities=("scientific reviewer",),
    )

    def recipe(inputs, configuration, runtime):
        with runtime.step("review"):
            runtime.check("approval")
        with runtime.step("measure"):
            pass
        return {"score": 0, "metric": "fixture"}

    _, _, request = variant(
        workspace,
        inputs,
        recipe=recipe,
        requirements=(requirement,),
        steps=(
            praxis.Step("review", "Scoped review", "human", "approve", kind="human"),
            praxis.Step("measure", "Measure", "fixture", "measure"),
        ),
    )
    prepared = praxis.prepare(request, catalog=catalog, context=context)
    assert prepared.ready
    with pytest.raises(WaitingForReview):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="waiting")
    first = context.records.attempt("waiting")
    assert first.operational_status == "waiting" and len(first.steps) == 1
    context.reviews = (
        praxis.EvidenceRecord(
            "retained:review@1",
            "human",
            "approval",
            invocation_digest(
                CAPABILITY, prepared.selection.protocol_ref, prepared.inputs, prepared.configuration
            ),
            "passed",
            "boundary",
            "reviewer",
            "scientific reviewer",
            "2026-10-08",
        ),
    )
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context, retry_of="waiting")
    assert attempt.contract_status == "supported"
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


@pytest.mark.parametrize("coverage,expected", [("boundary", False), ("throughout", True)])
def test_endpoint_equality_does_not_prove_throughout_invariant(
    workspace, inputs, coverage, expected
):
    catalog, context = workspace
    checker_ref = praxis.MethodRef("extension", "enforcement", "1")
    requirement = praxis.Requirement(
        "frozen",
        "Frozen throughout",
        "runtime",
        checker_ref=checker_ref,
        coverage_required="throughout",
        accepted_evidence=("instrumented",),
    )

    def checker(inputs, configuration, outputs):
        evidence = praxis.EvidenceRecord(
            "retained:instrumentation@1",
            "instrumented",
            "frozen",
            outputs["subject"],
            "passed",
            coverage,
            "provider",
            "provider instrumentation",
            "2026-10-08",
            steps=("measure",),
            attempt_id=outputs["attempt"],
        )
        return praxis.CheckResult(
            "passed", "Retained provider evidence", evidence_records=(evidence,)
        )

    context.extensions.register_checker(checker_ref, checker)

    def recipe(inputs, configuration, runtime):
        with runtime.step("measure"):
            pass
        runtime.check(
            "frozen",
            outputs={
                "subject": invocation_digest(
                    CAPABILITY, runtime.protocol.ref, inputs, configuration
                ),
                "attempt": runtime.identifier,
            },
        )
        return {"score": 0, "metric": "fixture"}

    _, _, request = variant(workspace, inputs, recipe=recipe, requirements=(requirement,))
    prepared = praxis.prepare(request, catalog=catalog, context=context)
    if expected:
        _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
        assert (
            praxis.audit_execution(attempt.identifier, records=context.records).outcome
            == "consistent"
        )
    else:
        with pytest.raises(NotReadyError):
            praxis.execute(prepared, catalog=catalog, context=context, identifier="unverified")
        assert context.records.attempt("unverified").findings[-1].outcome == "undetermined"


def parent(workspace, inputs, *, recursive=False):
    catalog, context = workspace
    ref = replace(CAPABILITY, identifier="composed.fixture")
    capability = replace(catalog.get(CAPABILITY), ref=ref)
    catalog.register(capability)
    proto_ref = replace(RMSD, identifier="composed.fixture")
    binding_ref = replace(RMSD_BINDING, identifier="composed.fixture")
    step = praxis.Step(
        "child",
        "Invoke child comparison",
        "praxis",
        "invoke",
        kind="capability",
        child_capability_ref=ref if recursive else CAPABILITY,
        child_protocol_ref=proto_ref if recursive else RMSD,
        child_binding_ref=binding_ref if recursive else RMSD_BINDING,
    )
    protocol = replace(catalog.get(RMSD), ref=proto_ref, capability_ref=ref, steps=(step,))
    catalog.register(protocol)

    def recipe(inputs, configuration, runtime):
        result, _ = runtime.invoke("child", inputs)
        return result

    binding = praxis.ImplementationBinding(
        binding_ref, proto_ref, recipe, "Composed synthetic fixture"
    )
    context.extensions.register_binding(binding)
    return praxis.prepare(
        praxis.MethodRequest(ref, inputs, protocol_ref=proto_ref, binding_ref=binding_ref),
        catalog=catalog,
        context=context,
    )


def test_child_attempts_pin_candidates_and_correlate_parent(workspace, inputs):
    catalog, context = workspace
    prepared = parent(workspace, inputs)
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert len(attempt.child_ids) == 1
    child = context.records.attempt(attempt.child_ids[0])
    assert child.parent_id == attempt.identifier
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


def test_recursive_capability_composition_is_prohibited(workspace, inputs):
    catalog, context = workspace
    prepared = parent(workspace, inputs, recursive=True)
    with pytest.raises(ContractError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="recursive")
    assert not context.records.attempt("recursive").child_ids


def test_hydrogen_v2_retains_v1_and_requires_throughout_evidence(tmp_path):
    catalog = praxis.Catalog.open(tmp_path)
    catalog.load_bundled()
    original = catalog.export_bundle()
    catalog.load_bundled(version="2")
    capabilities = [item for item in catalog.definitions() if isinstance(item, praxis.Capability)]
    current = next(item for item in capabilities if item.ref.version == "2")
    old = next(item for item in capabilities if item.ref.version == "1")
    assert old.to_dict() in original["documents"]
    guarantee = next(
        item for item in current.requirements if item.identifier == "frozen_enforcement"
    )
    assert guarantee.phase == "runtime" and guarantee.coverage_required == "throughout"
    assert guarantee.accepted_evidence == ("instrumented", "independent")
    assert {"correspondence", "report"} <= {item.name for item in current.outputs}
    assert len(catalog.protocols_for(old.ref)) == len(catalog.protocols_for(current.ref)) == 2
    assert all(item.pending for item in catalog.protocols_for(current.ref))


def test_nested_composition_rejects_changed_grandchild_before_provider_calls(workspace, inputs):
    catalog, context = workspace
    child = parent(workspace, inputs)
    capability = replace(
        catalog.get(child.capability_ref),
        ref=replace(child.capability_ref, identifier="nested.outer"),
    )
    catalog.register(capability)
    protocol_ref = replace(child.selection.protocol_ref, identifier="nested.outer")
    binding_ref = replace(child.selection.binding_ref, identifier="nested.outer")
    protocol = replace(
        catalog.get(child.selection.protocol_ref),
        ref=protocol_ref,
        capability_ref=capability.ref,
        steps=(
            replace(
                catalog.get(child.selection.protocol_ref).steps[0],
                child_capability_ref=child.capability_ref,
                child_protocol_ref=child.selection.protocol_ref,
                child_binding_ref=child.selection.binding_ref,
            ),
        ),
    )
    catalog.register(protocol)
    context.extensions.register_binding(
        replace(
            context.extensions.bindings[child.selection.binding_ref],
            ref=binding_ref,
            protocol_ref=protocol_ref,
        )
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(
            capability.ref, inputs, protocol_ref=protocol_ref, binding_ref=binding_ref
        ),
        catalog=catalog,
        context=context,
    )
    assert any(
        item["binding"]["ref"] == RMSD_BINDING.to_dict() for item in prepared.child_implementations
    )
    registry = praxis.Extensions()
    for ref, checker in context.extensions.checkers.items():
        registry.register_checker(ref, checker)
    for binding in context.extensions.bindings.values():
        registry.register_binding(
            replace(
                binding,
                recipe=lambda i, c, r: (_ for _ in ()).throw(
                    AssertionError("Should never execute changed provider")
                ),
            )
            if binding.ref == RMSD_BINDING
            else binding
        )
    context.extensions = registry
    with pytest.raises(NotReadyError, match="nested child"):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="changed-grandchild")
    assert not context.records.attempt("changed-grandchild").steps


def test_scientific_selection_cannot_infer_an_unspecified_scenario():
    with pytest.raises(DefinitionError, match="explicit scenario"):
        praxis.SelectionPolicy(criteria={"require_supported": True})


def test_unknown_policy_does_not_pass_with_an_explicit_protocol(workspace, inputs):
    catalog, context = workspace
    policy = praxis.SelectionPolicy(praxis.MethodRef("extension", "unregistered.policy", "1"))
    prepared = praxis.prepare(
        praxis.MethodRequest(
            CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING, selection_policy=policy
        ),
        catalog=catalog,
        context=context,
    )
    assert not prepared.ready and "Exact selection policy is unavailable" in prepared.reasons


def test_changed_policy_is_rejected_by_replay_preflight(workspace, inputs):
    catalog, context = workspace
    reference = praxis.MethodRef("extension", "fixture.select.rmsd", "1")
    context.extensions.register_policy(reference, lambda candidates, policy: RMSD)
    prepared = praxis.prepare(
        praxis.MethodRequest(
            CAPABILITY,
            inputs,
            binding_ref=RMSD_BINDING,
            selection_policy=praxis.SelectionPolicy(reference),
        ),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready and prepared.selection.protocol_ref == RMSD
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    registry = praxis.Extensions()
    for binding in context.extensions.bindings.values():
        registry.register_binding(binding)
    for ref, checker in context.extensions.checkers.items():
        registry.register_checker(ref, checker)
    registry.register_policy(reference, lambda candidates, policy: None)
    context.extensions = registry
    preflight = praxis.replay_preflight(attempt.identifier, catalog=catalog, context=context)
    assert not preflight.ready and any("policy" in reason for reason in preflight.reasons)


def test_human_and_executable_guarantees_cannot_share_a_misleading_checker_identity():
    with pytest.raises(DefinitionError, match="separate guarantee identities"):
        praxis.Requirement(
            "human",
            "Explicit human review",
            checker_ref=praxis.MethodRef("extension", "automatic", "1"),
            review_required=True,
            human_authorities=("reviewer",),
        )
