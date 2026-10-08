"""Explicit scoped review history; successful execution never creates an assessment."""

from dataclasses import dataclass, field

from .._serialization import Model, text
from ..errors import DefinitionError
from .references import MethodRef


@dataclass(frozen=True)
class Assessment(Model):
    schema = "praxis.assessment/0.1"
    ref: MethodRef
    subject: MethodRef
    actor: str
    authority: str
    date: str
    scope: str
    criteria: tuple[str, ...]
    findings: tuple[str, ...]
    outcome: str
    supporting_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    scenario: dict[str, object] = field(default_factory=dict, hash=False)
    supersedes: MethodRef | None = None
    withdrawn: bool = False

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "assessment" or self.subject.kind not in {"capability", "protocol"}:
            raise DefinitionError("Assessment references must identify an assessment and method")
        for name in ("actor", "authority", "date", "scope", "outcome"):
            text(getattr(self, name), name)
        if not self.criteria or not self.findings:
            raise DefinitionError("An assessment must state criteria and findings")
        if self.outcome not in {"supported", "challenged", "inconclusive"}:
            raise DefinitionError("Unknown assessment outcome")
        if self.outcome == "supported" and not self.supporting_refs:
            raise DefinitionError("Supported assessments require explicit supporting references")
