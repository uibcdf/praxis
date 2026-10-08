"""Declared sequential boundaries; numerical algorithms belong to providers."""

from dataclasses import dataclass

from .._serialization import Model, text
from ..errors import DefinitionError
from .references import MethodRef


@dataclass(frozen=True)
class Step(Model):
    schema = "praxis.step/0.1"
    identifier: str
    description: str
    provider: str
    operation: str
    pending: tuple[str, ...] = ()
    kind: str = "provider"
    repeat: int = 1
    condition_ref: MethodRef | None = None
    child_capability_ref: MethodRef | None = None
    child_protocol_ref: MethodRef | None = None
    child_binding_ref: MethodRef | None = None

    def __post_init__(self):
        self.validate()
        if self.kind not in {"provider", "capability", "human", "check"} or self.repeat < 1:
            raise DefinitionError("Unknown step kind or invalid bounded repetition")
        if self.kind == "capability" and (
            self.child_capability_ref is None or self.child_capability_ref.kind != "capability"
        ):
            raise DefinitionError("Child step must declare its Capability")
        for ref, kind in (
            (self.condition_ref, "extension"),
            (self.child_protocol_ref, "protocol"),
            (self.child_binding_ref, "extension"),
        ):
            if ref is not None and ref.kind != kind:
                raise DefinitionError("Step reference has the wrong kind")
        for field in ("identifier", "description", "provider", "operation"):
            text(getattr(self, field), field)
