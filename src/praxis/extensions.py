"""Explicit in-process extensions. Catalog reads never discover or import plugins."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable

from ._implementation import callable_identity
from ._serialization import Model, text
from .definitions import EvidenceRecord, MethodRef
from .errors import ConflictError, DefinitionError


@dataclass(frozen=True)
class CheckResult(Model):
    schema = "praxis.check-result/0.1"
    outcome: str
    reason: str
    evidence: tuple[str, ...] = ()
    coverage: str = "declared check only"
    evidence_records: tuple[EvidenceRecord, ...] = ()

    def __post_init__(self):
        self.validate()
        if self.outcome not in {"passed", "failed", "undetermined", "skipped"}:
            raise DefinitionError("Checkers must return an explicit supported outcome")
        text(self.reason, "check reason")


@dataclass(frozen=True)
class ImplementationBinding:
    ref: MethodRef
    protocol_ref: MethodRef
    recipe: Callable
    compatibility: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self):
        if self.ref.kind != "extension" or self.protocol_ref.kind != "protocol":
            raise DefinitionError("A binding connects an exact extension to an exact Protocol")
        if not callable(self.recipe):
            raise DefinitionError("A binding requires a callable recipe")
        text(self.compatibility, "binding compatibility declaration")
        for dependency in self.dependencies:
            text(dependency, "dependency module name")

    def description(self):
        return {
            "ref": self.ref.to_dict(),
            "protocol_ref": self.protocol_ref.to_dict(),
            "compatibility": self.compatibility,
            "dependencies": list(self.dependencies),
            "implementation": callable_identity(self.recipe),
            "evidence_scope": "provider declaration; not independently verified",
        }


class Extensions:
    """Exact-version registrations; conflicting or ambiguous bindings never win by order."""

    def __init__(self):
        self._bindings = {}
        self._checkers = {}
        self._policies = {}

    @property
    def bindings(self):
        return MappingProxyType(self._bindings)

    @property
    def checkers(self):
        return MappingProxyType(self._checkers)

    def register_binding(self, binding):
        if not isinstance(binding, ImplementationBinding):
            raise DefinitionError("Expected an ImplementationBinding")
        if (
            binding.ref in self.bindings
            or binding.ref in self.checkers
            or binding.ref in self.policies
        ):
            raise ConflictError("Extension reference is already registered")
        binding.description()
        self._bindings[binding.ref] = binding

    def register_checker(self, reference, checker):
        if reference.kind != "extension" or not callable(checker):
            raise DefinitionError("A checker needs an exact extension reference and callable")
        if reference in self.checkers or reference in self.bindings or reference in self.policies:
            raise ConflictError("Extension reference is already registered")
        callable_identity(checker)
        self._checkers[reference] = checker

    def describe_checkers(self, references):
        descriptions = []
        for reference in dict.fromkeys(ref for ref in references if ref is not None):
            checker = self.checkers.get(reference)
            descriptions.append(
                {
                    "ref": reference.to_dict(),
                    "implementation": callable_identity(checker) if checker is not None else None,
                }
            )
        return tuple(descriptions)

    def bindings_for(self, protocol_ref):
        return tuple(
            binding for binding in self.bindings.values() if binding.protocol_ref == protocol_ref
        )

    @property
    def policies(self):
        return MappingProxyType(self._policies)

    def register_policy(self, reference, policy):
        if reference.kind != "extension" or not callable(policy):
            raise DefinitionError("Policy requires an exact extension reference and callable")
        if reference in self.checkers or reference in self.bindings or reference in self.policies:
            raise ConflictError("Extension reference is already registered")
        callable_identity(policy)
        self._policies[reference] = policy

    def describe_policy(self, reference):
        policy = self.policies.get(reference)
        return {
            "ref": reference.to_dict(),
            "implementation": callable_identity(policy) if policy is not None else None,
        }
