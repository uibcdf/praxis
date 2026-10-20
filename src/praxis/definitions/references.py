"""Exact owner-issued local references; paths and current aliases are not identities."""

from dataclasses import dataclass

from .._serialization import Model, text
from ..errors import DefinitionError


@dataclass(frozen=True)
class MethodRef(Model):
    schema = "praxis.method-ref/0.1"
    kind: str
    identifier: str
    version: str
    owner: str = "praxis"

    def __post_init__(self):
        for field in ("kind", "identifier", "version", "owner"):
            text(getattr(self, field), field)
        if self.kind not in {
            "capability",
            "protocol",
            "assessment",
            "benchmark",
            "extension",
            "review",
            "suitability",
            "status",
        }:
            raise DefinitionError("Unknown reference kind")

    def __str__(self):
        return f"{self.owner}:{self.kind}:{self.identifier}@{self.version}"
