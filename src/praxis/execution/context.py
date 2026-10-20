"""Standalone method context, with optional borrowed application recording."""

from dataclasses import dataclass, field
from getpass import getuser

from ..definitions import EvidenceRecord
from ..extensions import Extensions
from ..recording import MethodRecords


@dataclass
class ExecutionContext:
    extensions: Extensions
    records: MethodRecords
    recorder: object | None = None
    attribution: bool = False
    actor: str = field(default_factory=lambda: "local:" + getuser())
    authority: str = "application-supplied local execution; identity not authenticated"
    environment_requirements: dict[str, object] = field(default_factory=dict)
    environment_metadata: dict[str, object] = field(default_factory=dict)
    cancelled: bool = False
    reviews: tuple[EvidenceRecord, ...] = ()
    max_depth: int = 16
