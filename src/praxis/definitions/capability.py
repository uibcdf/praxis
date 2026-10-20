"""Scientific intent independent of recipes and provider availability."""

from dataclasses import dataclass

from .._serialization import Model, text, unique
from ..errors import DefinitionError
from .contracts import Field, Requirement
from .references import MethodRef


@dataclass(frozen=True)
class Capability(Model):
    schema = "praxis.capability/0.1"
    ref: MethodRef
    title: str
    intent: str
    inputs: tuple[Field, ...]
    outputs: tuple[Field, ...]
    requirements: tuple[Requirement, ...] = ()
    authorized_changes: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    status: str = "experimental"

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "capability":
            raise DefinitionError("Capability reference kind must be capability")
        text(self.title, "title")
        text(self.intent, "scientific intent")
        if not self.inputs or not self.outputs:
            raise DefinitionError("A Capability requires semantic inputs and outputs")
        for group in (self.inputs, self.outputs):
            unique([item.name for item in group], "semantic fields")
        unique([item.identifier for item in self.requirements], "requirements")
        if self.status not in {"experimental", "deprecated", "withdrawn"}:
            raise DefinitionError("Scientific validation belongs to explicit assessments")
