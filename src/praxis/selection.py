"""Recorded explicit selection or conservative, versioned eligibility policies."""

from dataclasses import dataclass, field

from ._quantities import duration_seconds
from ._serialization import Model, snapshot
from .applicability import assess_applicability
from .definitions import MethodRef
from .errors import DefinitionError
from .execution.reports import SelectionRecord

BUILTIN_POLICY = MethodRef("extension", "praxis.unique_eligible", "1")


@dataclass(frozen=True)
class SelectionPolicy(Model):
    schema = "praxis.selection-policy/0.1"
    ref: MethodRef = BUILTIN_POLICY
    criteria: dict[str, object] = field(default_factory=dict)
    scenario: dict[str, object] = field(default_factory=dict)

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "extension":
            raise DefinitionError("Selection policy requires an exact extension identity")
        if set(self.criteria) - {
            "require_applicable",
            "require_available",
            "require_supported",
            "require_favorable",
            "fidelity",
            "cost_class",
            "max_expected_duration",
        }:
            raise DefinitionError("Unknown selection criterion")
        for key in (
            "require_applicable",
            "require_available",
            "require_supported",
            "require_favorable",
        ):
            if key in self.criteria and type(self.criteria[key]) is not bool:
                raise DefinitionError("Selection requirement must be boolean")
        if (
            self.criteria.get("require_supported") or self.criteria.get("require_favorable")
        ) and not self.scenario:
            raise DefinitionError(
                "Scientific support/suitability selection requires an explicit scenario"
            )
        if "max_expected_duration" in self.criteria:
            if (
                duration_seconds(
                    self.criteria["max_expected_duration"], "selection.max_expected_duration"
                )
                < 0
            ):
                raise DefinitionError("Selection duration budget must be nonnegative")


def _candidate(protocol, request, capability, catalog, extensions, policy, reviews=()):
    status = catalog.status_for(protocol.ref, scenario=policy.scenario)
    reasons = []
    unresolved = []
    criteria = policy.criteria
    if status["maturity"] != "experimental":
        reasons.append("Method is deprecated, withdrawn or has conflicting status")
    configuration = snapshot(request.configuration)
    names = {item.name for item in protocol.parameters}
    if set(configuration) - names:
        reasons.append("Scientific configuration includes undeclared parameters")
    for parameter in protocol.parameters:
        if parameter.name not in configuration:
            if parameter.required:
                unresolved.append("Required parameter is unresolved: " + parameter.name)
            else:
                configuration[parameter.name] = snapshot(parameter.default)
    applicability = assess_applicability(
        capability, protocol, request.inputs, configuration, extensions, reviews=reviews
    )
    if criteria.get("require_applicable"):
        if applicability.outcome == "inapplicable":
            reasons.append("Scientific applicability failed")
        elif applicability.outcome != "applicable":
            unresolved.append("Scientific applicability is undetermined")
    bindings = extensions.bindings_for(protocol.ref)
    if criteria.get("require_available"):
        from depdigest import is_installed

        available = [
            binding
            for binding in bindings
            if all(is_installed(module) for module in binding.dependencies)
        ]
        if not available:
            reasons.append("No implementation with available declared dependencies")
    if criteria.get("require_supported") and status["validation"] != "supported":
        unresolved.append("No uncontradicted supported assessment for this exact scenario")
    if criteria.get("require_favorable"):
        statements = catalog.suitability_for(protocol.ref, scenario=policy.scenario, active=True)
        if status["suitability"] == "exclusion":
            reasons.append("Recorded scenario excludes this method")
        elif (
            status["suitability"] != "favorable"
            or not statements
            or any(item.basis != "measured" for item in statements)
        ):
            unresolved.append("Favorable scenario judgment lacks uncontradicted measured support")
    profile = protocol.resources
    for key in ("fidelity", "cost_class"):
        if key in criteria:
            if profile is None or getattr(profile, key) is None:
                unresolved.append("Unknown resource characteristic: " + key)
            elif getattr(profile, key) != criteria[key]:
                reasons.append("Requested resource characteristic differs: " + key)
    if "max_expected_duration" in criteria:
        if (
            profile is None
            or profile.expected_duration is None
            or profile.basis == "unknown"
            or profile.conditions != policy.scenario
        ):
            unresolved.append("No duration estimate for this exact scenario")
        elif duration_seconds(
            profile.expected_duration, "protocol.expected_duration"
        ) > duration_seconds(criteria["max_expected_duration"], "selection.max_expected_duration"):
            reasons.append("Declared duration exceeds the requested budget")
    return {
        "protocol_ref": protocol.ref.to_dict(),
        "definition": protocol.to_dict(),
        "status": status,
        "applicability": applicability.to_dict(),
        "binding_refs": [item.ref.to_dict() for item in bindings],
        "outcome": "ineligible" if reasons else "undetermined" if unresolved else "eligible",
        "reasons": [*reasons, *unresolved],
    }


def select(request, catalog, extensions, *, reviews=()):
    protocols = catalog.protocols_for(request.capability_ref)
    candidates = tuple(item.ref for item in protocols)
    reasons = []
    policy_spec = request.selection_policy
    candidate_findings = ()
    policy_description = None
    if policy_spec is None:
        eligible = tuple(
            item.ref
            for item in protocols
            if catalog.status_for(item.ref)["maturity"] == "experimental"
        )
        policy = "explicit choice" if request.protocol_ref else "unique candidate/0.1"
    else:
        capability = catalog.get(request.capability_ref)
        candidate_findings = tuple(
            _candidate(item, request, capability, catalog, extensions, policy_spec, reviews)
            for item in protocols
        )
        eligible = tuple(
            MethodRef.from_dict(item["protocol_ref"])
            for item in candidate_findings
            if item["outcome"] == "eligible"
        )
        policy = str(policy_spec.ref)
        policy_description = (
            extensions.describe_policy(policy_spec.ref)
            if policy_spec.ref != BUILTIN_POLICY
            else {"ref": BUILTIN_POLICY.to_dict(), "implementation": "praxis.unique_eligible/1"}
        )
    if (
        policy_spec is not None
        and policy_spec.ref != BUILTIN_POLICY
        and policy_spec.ref not in extensions.policies
    ):
        reasons.append("Exact selection policy is unavailable")
    protocol_ref = request.protocol_ref
    if protocol_ref is not None:
        if protocol_ref not in eligible:
            reasons.append("Explicit Protocol does not fulfill the declared selection requirements")
            protocol_ref = None
    elif policy_spec is not None and policy_spec.ref != BUILTIN_POLICY:
        chooser = extensions.policies.get(policy_spec.ref)
        if chooser is None:
            reasons.append("Exact selection policy is unavailable")
        else:
            choice = chooser(snapshot(candidate_findings), snapshot(policy_spec.to_dict()))
            if choice is not None and choice not in eligible:
                raise DefinitionError(
                    "Policy selected a candidate that failed declared eligibility"
                )
            protocol_ref = choice
            if choice is None:
                reasons.append("Registered policy abstained")
    elif len(eligible) == 1:
        protocol_ref = eligible[0]
    else:
        reasons.append("Protocol choice is ambiguous or no eligible candidate is registered")
    binding_ref = None
    if protocol_ref is not None:
        bindings = extensions.bindings_for(protocol_ref)
        if request.binding_ref is not None:
            if any(item.ref == request.binding_ref for item in bindings):
                binding_ref = request.binding_ref
            else:
                reasons.append("Explicit binding is not registered for this Protocol")
        elif len(bindings) == 1:
            binding_ref = bindings[0].ref
        else:
            reasons.append("Binding choice is ambiguous or no implementation is registered")
    return SelectionRecord(
        candidates,
        protocol_ref,
        binding_ref,
        policy,
        tuple(reasons),
        candidate_findings=candidate_findings,
        criteria=policy_spec.to_dict() if policy_spec else {},
        policy_implementation=policy_description,
    )
