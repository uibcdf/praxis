"""Provisional local method records, not shared MOLI Runs or ExecutionPlans."""

from dataclasses import dataclass, field

from .._serialization import Model
from ..definitions import CheckFinding, MethodRef


@dataclass(frozen=True)
class SelectionRecord(Model):
    schema = "praxis.selection/0.1"
    candidates: tuple[MethodRef, ...]
    protocol_ref: MethodRef | None
    binding_ref: MethodRef | None
    policy: str
    reasons: tuple[str, ...]
    candidate_findings: tuple[dict[str, object], ...] = ()
    criteria: dict[str, object] = field(default_factory=dict)
    policy_implementation: dict[str, object] | None = None


@dataclass(frozen=True)
class PreparedInvocation(Model):
    schema = "praxis.prepared/0.1"
    identifier: str
    created: str
    capability_ref: MethodRef
    selection: SelectionRecord
    inputs: dict[str, object]
    configuration: dict[str, object]
    definitions: tuple[dict[str, object], ...]
    binding: dict[str, object] | None
    findings: tuple[CheckFinding, ...]
    ready: bool
    reasons: tuple[str, ...]
    checkers: tuple[dict[str, object], ...] = ()
    environment_requirements: dict[str, object] = field(default_factory=dict)
    environment_observed: dict[str, object] = field(default_factory=dict)
    actor: str | None = None
    authority: str | None = None
    catalog_snapshot: tuple[dict[str, object], ...] = ()
    child_implementations: tuple[dict[str, object], ...] = ()


@dataclass(frozen=True)
class AttemptRecord(Model):
    schema = "praxis.attempt/0.1"
    identifier: str
    prepared_id: str
    started: str
    finished: str | None
    operational_status: str
    contract_status: str
    recording_status: str
    findings: tuple[CheckFinding, ...]
    steps: tuple[dict[str, object], ...]
    outputs: dict[str, object] | None
    environment: dict[str, object]
    failure_type: str | None = None
    recording_refs: tuple[dict[str, object], ...] = ()
    attribution: dict[str, object] | None = None
    retry_of: str | None = None
    limitations: tuple[str, ...] = (
        "Observed declared boundaries; provider internals not inspected",
    )
    implementations: tuple[dict[str, object], ...] = ()
    actor: str | None = None
    authority: str | None = None
    parent_id: str | None = None
    child_ids: tuple[str, ...] = ()
    replay_of: str | None = None
    branches: tuple[dict[str, object], ...] = ()


@dataclass
class MethodRequest:
    capability_ref: MethodRef | None = None
    inputs: dict[str, object] = field(default_factory=dict)
    configuration: dict[str, object] = field(default_factory=dict)
    protocol_ref: MethodRef | None = None
    binding_ref: MethodRef | None = None
    selection_policy: object | None = None

    def __post_init__(self):
        from .._arguments import request_values
        from ..selection import SelectionPolicy

        if self.selection_policy is not None:
            if not isinstance(self.selection_policy, SelectionPolicy):
                raise ValueError("Expected a SelectionPolicy")
            self.selection_policy = SelectionPolicy.from_dict(self.selection_policy.to_dict())

        self.inputs, self.configuration = request_values(self.inputs, self.configuration)
