"""Reproducible procedure, scope and tradeoffs; registration does not imply execution."""

from dataclasses import dataclass

from .._serialization import Model, text, unique
from ..errors import DefinitionError
from .contracts import Parameter, Requirement
from .references import MethodRef
from .reviews import ResourceProfile
from .steps import Step


@dataclass(frozen=True)
class Tradeoff(Model):
    schema = "praxis.tradeoff/0.1"
    kind: str
    conditions: str
    statement: str
    basis: str = "proposed"
    support: tuple[str, ...] = ()
    alternative: MethodRef | None = None

    def __post_init__(self):
        self.validate()
        if self.kind not in {"advantage", "disadvantage", "favorable", "discouraged", "exclusion"}:
            raise DefinitionError("Unknown tradeoff kind")
        if self.basis not in {"proposed", "estimated", "measured", "unknown"}:
            raise DefinitionError("Unknown tradeoff basis")
        text(self.conditions, "tradeoff conditions")
        text(self.statement, "tradeoff statement")
        if self.basis == "measured" and not self.support:
            raise DefinitionError("Measured claims require explicit supporting references")


@dataclass(frozen=True)
class Protocol(Model):
    schema = "praxis.protocol/0.1"
    ref: MethodRef
    title: str
    procedure: str
    capability_ref: MethodRef | None
    steps: tuple[Step, ...]
    scientific_basis: tuple[str, ...] = ()
    parameters: tuple[Parameter, ...] = ()
    requirements: tuple[Requirement, ...] = ()
    provenance_requirements: tuple[str, ...] = ()
    tradeoffs: tuple[Tradeoff, ...] = ()
    limitations: tuple[str, ...] = ()
    pending: tuple[str, ...] = ()
    status: str = "experimental"
    resources: ResourceProfile | None = None
    provenance_checks: tuple[Requirement, ...] = ()

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "protocol":
            raise DefinitionError("Protocol reference kind must be protocol")
        if self.capability_ref is not None and self.capability_ref.kind != "capability":
            raise DefinitionError("Protocol target must be an exact Capability")
        text(self.title, "title")
        text(self.procedure, "procedure")
        if not self.steps:
            raise DefinitionError("A Protocol requires declared steps")
        unique([item.identifier for item in self.steps], "steps")
        unique(
            [item.identifier for item in (*self.requirements, *self.provenance_checks)],
            "requirements",
        )
        unique(self.provenance_requirements, "provenance requirements")
        if set(item.identifier for item in self.provenance_checks) - set(
            self.provenance_requirements
        ):
            raise DefinitionError(
                "Provenance checks must identify declared provenance requirements"
            )
        unique([item.name for item in self.parameters], "parameters")
        if self.status not in {"experimental", "deprecated", "withdrawn"}:
            raise DefinitionError("Scientific validation belongs to explicit assessments")
