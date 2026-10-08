"""Explicit local admission and scenario judgments; neither execution nor metrics promote methods."""

from dataclasses import dataclass, field

from .._serialization import Model, text
from ..errors import DefinitionError
from .references import MethodRef


@dataclass(frozen=True)
class AdmissionReview(Model):
    schema = "praxis.admission-review/0.1"
    ref: MethodRef
    subject: MethodRef
    subject_digest: str
    proposer: str
    maintainer: str
    reviewer: str
    authority: str
    date: str
    outcome: str
    rationale: str
    evidence: tuple[MethodRef, ...] = ()
    conditions: tuple[str, ...] = ()
    source_workflow: str | None = None
    supersedes: MethodRef | None = None

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "review" or self.subject.kind not in {"capability", "protocol"}:
            raise DefinitionError("Admission reviews identify an exact scientific definition")
        for name in (
            "subject_digest",
            "proposer",
            "maintainer",
            "reviewer",
            "authority",
            "date",
            "rationale",
        ):
            text(getattr(self, name), name)
        if self.outcome not in {
            "clarification_requested",
            "rejected",
            "admitted_experimental",
            "promoted",
        }:
            raise DefinitionError("Unknown admission review outcome")
        if self.outcome == "promoted" and not self.evidence:
            raise DefinitionError("Promotion requires explicit assessment evidence")


@dataclass(frozen=True)
class SuitabilityStatement(Model):
    schema = "praxis.suitability/0.1"
    ref: MethodRef
    subject: MethodRef
    scenario: dict[str, object]
    outcome: str
    criteria: tuple[str, ...]
    actor: str
    authority: str
    date: str
    rationale: str
    basis: str = "proposed"
    supporting_refs: tuple[str, ...] = ()
    alternative: MethodRef | None = None
    supersedes: MethodRef | None = None
    withdrawn: bool = False

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "suitability" or self.subject.kind not in {"capability", "protocol"}:
            raise DefinitionError("Suitability targets an exact method")
        if not self.scenario or not self.criteria:
            raise DefinitionError("Suitability needs explicit scenario properties and criteria")
        for name in ("actor", "authority", "date", "rationale"):
            text(getattr(self, name), name)
        if self.outcome not in {"favorable", "discouraged", "exclusion", "unknown"}:
            raise DefinitionError("Unknown suitability outcome")
        if self.basis not in {"proposed", "estimated", "measured", "unknown"}:
            raise DefinitionError("Unknown suitability basis")
        if self.basis == "measured" and not self.supporting_refs:
            raise DefinitionError("Measured suitability requires retained supporting references")


@dataclass(frozen=True)
class MethodStatus(Model):
    schema = "praxis.method-status/0.1"
    ref: MethodRef
    subject: MethodRef
    action: str
    actor: str
    authority: str
    date: str
    reason: str
    replacement: MethodRef | None = None
    supersedes: MethodRef | None = None

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "status" or self.subject.kind not in {"capability", "protocol"}:
            raise DefinitionError("Method status targets an exact method")
        if self.action not in {"deprecated", "withdrawn", "experimental"}:
            raise DefinitionError("Unknown method status action")
        for name in ("actor", "authority", "date", "reason"):
            text(getattr(self, name), name)
        if self.replacement is not None and self.replacement.kind != self.subject.kind:
            raise DefinitionError("Replacement must identify the same kind of method")


@dataclass(frozen=True)
class ResourceProfile(Model):
    schema = "praxis.resource-profile/0.1"
    fidelity: str | None = None
    cost_class: str | None = None
    hardware: tuple[str, ...] = ()
    expected_duration: dict[str, object] | None = None
    basis: str = "unknown"
    conditions: dict[str, object] = field(default_factory=dict)
    support: tuple[str, ...] = ()

    def __post_init__(self):
        self.validate()
        if self.basis not in {"proposed", "estimated", "measured", "unknown"}:
            raise DefinitionError("Unknown resource-profile basis")
        if self.basis == "measured" and not self.support:
            raise DefinitionError("Measured profiles require supporting records")
        if self.expected_duration is not None:
            from .._quantities import duration_seconds

            if duration_seconds(self.expected_duration, "protocol.expected_duration") < 0:
                raise DefinitionError("Expected duration cannot be negative")
