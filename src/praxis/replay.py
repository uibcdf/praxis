"""Local trace inspection and explicit fresh execution; Recorda is not a replay engine."""

from dataclasses import dataclass

from ._implementation import callable_identity
from ._serialization import Model, digest, snapshot
from .applicability import assess_applicability, checker_references
from .definitions import Capability, MethodRef, Protocol
from .errors import IntegrityError, NotReadyError
from .execution.runner import _verify_child_pins, _verify_policy_pin, execute
from .provenance import environment_findings, environment_manifest


@dataclass(frozen=True)
class ReplayPreflight(Model):
    schema = "praxis.replay-preflight/0.1"
    attempt_id: str
    prepared_id: str
    ready: bool
    reasons: tuple[str, ...]
    findings: tuple[dict[str, object], ...]
    environment: dict[str, object]
    limitations: tuple[str, ...] = (
        "Checks observed local identities and declared reference/provenance checkers; no provider computation",
        "Cannot prove equivalence of opaque engines, closure state, remote permissions or physical events",
    )


def trace_execution(identifier, *, records):
    """Return preserved method relationships and intent, without importing providers."""

    def visit(current, ancestors):
        if current in ancestors:
            raise IntegrityError("Cyclic recorded child attempt graph")
        attempt = records.attempt(current)
        prepared = records.prepared(attempt.prepared_id)
        children = []
        for child_id in attempt.child_ids:
            try:
                children.append(visit(child_id, (*ancestors, current)))
            except FileNotFoundError:
                children.append({"attempt_id": child_id, "availability": "missing"})
        return {"attempt": attempt.to_dict(), "prepared": prepared.to_dict(), "children": children}

    return visit(identifier, ())


def replay_preflight(identifier, *, catalog, context):
    """Inspect a supported attempt and reevaluate declared availability/precondition checks."""
    attempt = context.records.attempt(identifier)
    prepared = context.records.prepared(attempt.prepared_id)
    reasons = []
    findings = ()
    binding = context.extensions.bindings.get(prepared.selection.binding_ref)
    dependencies = binding.dependencies if binding is not None else ()
    observed = environment_manifest(
        (*dependencies, *prepared.environment_requirements.get("packages", {})),
        supplied=context.environment_metadata,
    )
    if attempt.operational_status != "completed" or attempt.contract_status != "supported":
        reasons.append("Original attempt does not establish a supported completed result")
    if not prepared.ready or len(prepared.definitions) != 2:
        reasons.append("Original preparation is unresolved")
    else:
        capability = Capability.from_dict(prepared.definitions[0])
        protocol = Protocol.from_dict(prepared.definitions[1])
        for definition in (capability, protocol):
            try:
                if digest(catalog.get(definition.ref)) != digest(definition):
                    reasons.append("Historical definition differs: " + str(definition.ref))
                if catalog.status_for(definition.ref)["maturity"] != "experimental":
                    reasons.append("Method is currently withdrawn/deprecated or conflicting")
            except FileNotFoundError:
                reasons.append("Historical definition is unavailable: " + str(definition.ref))
        try:
            _verify_child_pins(prepared, context.extensions)
            _verify_policy_pin(prepared, context.extensions)
        except NotReadyError as error:
            reasons.append(str(error))
        if binding is None or binding.description() != prepared.binding:
            reasons.append("Exact historical binding is unavailable or changed")
        if (
            context.extensions.describe_checkers(checker_references(capability, protocol))
            != prepared.checkers
        ):
            reasons.append("Exact historical checkers are unavailable or changed")
        else:
            applicability = assess_applicability(
                capability,
                protocol,
                prepared.inputs,
                prepared.configuration,
                context.extensions,
                reviews=context.reviews,
            )
            findings = tuple(item.to_dict() for item in applicability.findings)
            if applicability.outcome != "applicable":
                reasons.append("Current declared applicability/reference checks do not pass")
    reasons.extend(environment_findings(prepared.environment_requirements, observed))
    # Strict local replay does not silently accept a changed observed environment.
    for key in ("python", "python_implementation", "system", "machine", "packages", "application"):
        if observed.get(key) != attempt.environment.get(key):
            reasons.append("Historical observed environment differs: " + key)
    return ReplayPreflight(
        identifier, prepared.identifier, not reasons, tuple(reasons), findings, observed
    )


def replay_execution(identifier, *, catalog, context, comparator=None, comparator_ref=None):
    """Execute exact retained intent as a new linked attempt; compare only when explicitly supplied."""
    if (comparator is None) != (comparator_ref is None):
        raise ValueError("An equivalence comparator requires an exact versioned identity")
    if comparator_ref is not None and (
        not isinstance(comparator_ref, MethodRef) or comparator_ref.kind != "extension"
    ):
        raise ValueError("Comparator must identify an extension")
    preflight = replay_preflight(identifier, catalog=catalog, context=context)
    if not preflight.ready:
        raise NotReadyError("Replay preflight rejected: " + "; ".join(preflight.reasons))
    original = context.records.attempt(identifier)
    prepared = context.records.prepared(original.prepared_id)
    outputs, attempt = execute(prepared, catalog=catalog, context=context, replay_of=identifier)
    comparison = None
    if comparator is not None:
        comparison = {
            "original_id": identifier,
            "replay_id": attempt.identifier,
            "comparator_ref": comparator_ref.to_dict(),
            "implementation": callable_identity(comparator),
            "outcome": "unverified",
            "reason": "Replay did not support its contract",
        }
        if attempt.contract_status == "supported":
            try:
                finding = comparator(snapshot(original.outputs), snapshot(outputs))
                if finding.outcome not in {"passed", "failed", "undetermined"}:
                    raise ValueError(
                        "Comparator must return a CheckResult with a comparison outcome"
                    )
                comparison.update(
                    outcome=finding.outcome, reason=finding.reason, evidence=list(finding.evidence)
                )
            except Exception as error:
                comparison.update(outcome="checker_error", failure_type=type(error).__name__)
        context.records.store.put(
            {"kind": "replay-comparison", "id": attempt.identifier}, comparison
        )
    return outputs, attempt, comparison
