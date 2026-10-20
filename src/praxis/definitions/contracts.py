"""Semantic contracts and versioned executable check references."""

from dataclasses import dataclass

from .._serialization import Model, encode, text
from ..errors import DefinitionError
from .references import MethodRef


@dataclass(frozen=True)
class Field(Model):
    schema = "praxis.field/0.1"
    name: str
    meaning: str
    representation: str
    unit: str | None = None
    required: bool = True
    validator: str | None = None
    checker_ref: MethodRef | None = None
    quantity_field: str | None = None

    def __post_init__(self):
        self.validate()
        for field in ("name", "meaning", "representation"):
            text(getattr(self, field), field)
        if self.validator not in {
            None,
            "json",
            "number",
            "finite_number",
            "string",
            "boolean",
            "array",
            "object",
            "quantity",
        }:
            raise DefinitionError("Unknown structural field validator")
        if self.validator == "quantity" and (self.unit is None or self.quantity_field is None):
            raise DefinitionError("Quantity fields require explicit semantic field and unit")
        if self.checker_ref is not None and self.checker_ref.kind != "extension":
            raise DefinitionError("A field checker must reference an exact extension")


@dataclass(frozen=True)
class EvidenceRecord(Model):
    schema = "praxis.check-evidence/0.1"
    reference: str
    kind: str
    requirement: str
    subject_digest: str
    outcome: str
    coverage: str
    actor: str
    authority: str
    date: str
    steps: tuple[str, ...] = ()
    attempt_id: str | None = None
    limitations: tuple[str, ...] = ()

    def __post_init__(self):
        self.validate()
        for name in ("reference", "requirement", "subject_digest", "actor", "authority", "date"):
            text(getattr(self, name), name)
        if self.kind not in {"provider_declaration", "instrumented", "independent", "human"}:
            raise DefinitionError("Unknown evidence basis")
        if self.outcome not in {"passed", "failed", "undetermined"}:
            raise DefinitionError("Unknown evidence outcome")
        if self.coverage not in {"pre", "post", "boundary", "throughout"}:
            raise DefinitionError("Unknown evidence coverage")


@dataclass(frozen=True)
class Requirement(Model):
    schema = "praxis.requirement/0.1"
    identifier: str
    description: str
    phase: str = "pre"
    mandatory: bool = True
    checker_ref: MethodRef | None = None
    coverage_required: str = "boundary"
    accepted_evidence: tuple[str, ...] = (
        "provider_declaration",
        "instrumented",
        "independent",
        "human",
    )
    review_required: bool = False
    human_authorities: tuple[str, ...] = ()

    def __post_init__(self):
        self.validate()
        if self.coverage_required not in {"boundary", "throughout"}:
            raise DefinitionError("Unknown required evidence coverage")
        if set(self.accepted_evidence) - {
            "provider_declaration",
            "instrumented",
            "independent",
            "human",
        }:
            raise DefinitionError("Unknown permitted evidence basis")
        if self.review_required and self.checker_ref is not None:
            raise DefinitionError(
                "Human review and executable checks require separate guarantee identities"
            )
        if self.review_required and not self.human_authorities:
            raise DefinitionError("Human requirements must declare permitted authority")
        text(self.identifier, "requirement identifier")
        if self.identifier.startswith(("praxis.field/", "praxis.parameter/")):
            raise DefinitionError("The praxis.field/ namespace is reserved for field guarantees")
        text(self.description, "requirement description")
        if self.phase not in {"pre", "runtime", "post"}:
            raise DefinitionError("Check phases are pre, runtime and post")
        if self.checker_ref is not None and self.checker_ref.kind != "extension":
            raise DefinitionError("A checker must reference an exact extension")


@dataclass(frozen=True)
class Parameter(Model):
    schema = "praxis.parameter/0.1"
    name: str
    description: str
    required: bool = True
    default: object = None
    validator: str = "json"
    unit: str | None = None
    quantity_field: str | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None
    choices: tuple[object, ...] = ()
    checker_ref: MethodRef | None = None

    def __post_init__(self):
        self.validate()
        text(self.name, "parameter name")
        text(self.description, "parameter description")
        encode(self.default)
        Field(
            self.name,
            self.description,
            "Parameter value",
            self.unit,
            self.required,
            self.validator,
            self.checker_ref,
            self.quantity_field or "protocol.parameter/" + self.name,
        )
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise DefinitionError("Parameter minimum exceeds maximum")


@dataclass(frozen=True)
class CheckFinding(Model):
    schema = "praxis.check-finding/0.1"
    requirement: str
    phase: str
    outcome: str
    mandatory: bool
    checker_ref: MethodRef | None
    reason: str
    evidence: tuple[str, ...] = ()
    coverage: str = "declared check only"
    evidence_records: tuple[EvidenceRecord, ...] = ()

    def __post_init__(self):
        self.validate()
        if self.outcome not in {"passed", "failed", "undetermined", "checker_error", "skipped"}:
            raise DefinitionError("Unknown check outcome")
        text(self.reason, "check reason")
