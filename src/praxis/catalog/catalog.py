"""Exact local catalog, explicit reviews and conservative scenario queries."""

import json
from importlib.resources import files

from .._serialization import digest, snapshot
from ..benchmarks.definitions import BenchmarkSpec
from ..definitions import (
    AdmissionReview,
    Assessment,
    Capability,
    MethodRef,
    MethodStatus,
    Protocol,
    SuitabilityStatement,
)
from ..errors import DefinitionError
from .storage import FileStore

_TYPES = {
    item.schema: item
    for item in (
        Capability,
        Protocol,
        Assessment,
        AdmissionReview,
        SuitabilityStatement,
        MethodStatus,
        BenchmarkSpec,
    )
}


def _sort_key(item):
    return (item.ref.owner, item.ref.kind, item.ref.identifier, item.ref.version)


def _active(records):
    superseded = {item.supersedes for item in records if getattr(item, "supersedes", None)}
    return tuple(
        item
        for item in records
        if item.ref not in superseded and not getattr(item, "withdrawn", False)
    )


class Catalog:
    def __init__(self, directory):
        self.store = FileStore(directory)

    @classmethod
    def open(cls, directory):
        return cls(directory)

    def _validate_links(self, definition, get):
        if isinstance(definition, Protocol) and definition.capability_ref is not None:
            capability = get(definition.capability_ref)
            if not isinstance(capability, Capability):
                raise DefinitionError("Protocol target must resolve to a Capability")
            common = {item.identifier for item in capability.requirements}
            if common.intersection(
                item.identifier
                for item in (*definition.requirements, *definition.provenance_checks)
            ):
                raise DefinitionError("Protocol must not redefine a Capability requirement")
        if isinstance(definition, BenchmarkSpec):
            if not isinstance(get(definition.capability_ref), Capability):
                raise DefinitionError("Benchmark must reference a Capability")
            for method in definition.methods:
                protocol = get(method.protocol_ref)
                if (
                    not isinstance(protocol, Protocol)
                    or protocol.capability_ref != definition.capability_ref
                ):
                    raise DefinitionError("Benchmark methods must target its Capability")
        if hasattr(definition, "subject"):
            subject = get(definition.subject)
            if not isinstance(subject, (Capability, Protocol)):
                raise DefinitionError("Review must target a scientific definition")
            if isinstance(definition, AdmissionReview):
                if definition.subject_digest != digest(subject):
                    raise DefinitionError(
                        "Admission review does not identify the preserved definition"
                    )
                for ref in definition.evidence:
                    assessment = get(ref)
                    if (
                        not isinstance(assessment, Assessment)
                        or assessment.subject != definition.subject
                    ):
                        raise DefinitionError(
                            "Admission evidence must assess this exact definition"
                        )
                    if definition.outcome == "promoted" and (
                        assessment.outcome != "supported" or assessment.withdrawn
                    ):
                        raise DefinitionError(
                            "Promotion needs supported, active assessment evidence"
                        )
            if getattr(definition, "supersedes", None) is not None:
                previous = get(definition.supersedes)
                if type(previous) is not type(definition) or previous.subject != definition.subject:
                    raise DefinitionError(
                        "Revision must preserve record kind and scientific subject"
                    )
                if getattr(previous, "scenario", None) != getattr(definition, "scenario", None):
                    raise DefinitionError("Revised judgment must preserve its declared scenario")
        if isinstance(definition, MethodStatus) and definition.replacement is not None:
            get(definition.replacement)

    def register(self, definition):
        if type(definition) not in _TYPES.values():
            raise DefinitionError("Unsupported catalog definition or methodological record")
        definition = type(definition).from_dict(definition.to_dict())
        self._validate_links(definition, self.get)
        self.store.put(definition.ref, definition)
        return definition.ref

    def get(self, reference):
        document = self.store.get(reference)
        cls = _TYPES.get(document.get("schema"))
        if cls is None:
            raise DefinitionError("Unknown catalog schema")
        definition = cls.from_dict(document)
        if definition.ref != reference:
            raise DefinitionError("Definition reference differs from storage identity")
        return definition

    def definitions(self):
        for document in self.store.documents():
            cls = _TYPES.get(document.get("schema"))
            if cls is None:
                raise DefinitionError("Unknown catalog schema")
            definition = cls.from_dict(document)
            self.store.get(definition.ref)
            yield definition

    def protocols_for(self, capability_ref):
        self.get(capability_ref)
        return tuple(
            sorted(
                (
                    item
                    for item in self.definitions()
                    if isinstance(item, Protocol) and item.capability_ref == capability_ref
                ),
                key=_sort_key,
            )
        )

    def records_for(self, reference, record_type, *, scenario=None, active=False):
        self.get(reference)
        matches = tuple(
            sorted(
                (
                    item
                    for item in self.definitions()
                    if isinstance(item, record_type)
                    and item.subject == reference
                    and (scenario is None or getattr(item, "scenario", None) == snapshot(scenario))
                ),
                key=_sort_key,
            )
        )
        return _active(matches) if active else matches

    def assessments_for(self, reference, *, scenario=None, active=False):
        return self.records_for(reference, Assessment, scenario=scenario, active=active)

    def suitability_for(self, reference, *, scenario=None, active=False):
        return self.records_for(reference, SuitabilityStatement, scenario=scenario, active=active)

    def reviews_for(self, reference, *, active=False):
        return self.records_for(reference, AdmissionReview, active=active)

    def status_for(self, reference, *, scenario=None):
        definition = self.get(reference)
        if not isinstance(definition, (Capability, Protocol)):
            raise DefinitionError("Status queries require a Capability or Protocol")
        states = self.records_for(reference, MethodStatus, active=True)
        actions = {item.action for item in states}
        maturity = (
            next(iter(actions))
            if len(actions) == 1
            else ("conflicting" if actions else definition.status)
        )
        assessments = self.assessments_for(reference, scenario=scenario, active=True)
        conclusions = {item.outcome for item in assessments}
        validation = (
            next(iter(conclusions))
            if len(conclusions) == 1
            else ("conflicting" if conclusions else "unassessed")
        )
        suitability = self.suitability_for(reference, scenario=scenario, active=True)
        outcomes = {item.outcome for item in suitability}
        return {
            "ref": reference.to_dict(),
            "maturity": maturity,
            "validation": validation,
            "scenario": snapshot(scenario),
            "assessments": [item.ref.to_dict() for item in assessments],
            "suitability": next(iter(outcomes))
            if len(outcomes) == 1
            else ("conflicting" if outcomes else "unknown"),
            "suitability_refs": [item.ref.to_dict() for item in suitability],
            "status_refs": [item.ref.to_dict() for item in states],
            "reviews": [item.ref.to_dict() for item in self.reviews_for(reference, active=True)],
            "disclosure": "Judgments apply only to the recorded scope; no universal certification",
        }

    def query(self, *, kind=None, text=None, inputs=(), outputs=(), scenario=None):
        """Discovery filters describe definitions, never establish applicability."""
        matches = []
        for item in sorted(self.definitions(), key=_sort_key):
            if (
                not isinstance(item, (Capability, Protocol))
                or kind is not None
                and item.ref.kind != kind
            ):
                continue
            semantic = (
                item
                if isinstance(item, Capability)
                else (self.get(item.capability_ref) if item.capability_ref is not None else None)
            )
            if inputs and (
                semantic is None or not set(inputs) <= {f.name for f in semantic.inputs}
            ):
                continue
            if outputs and (
                semantic is None or not set(outputs) <= {f.name for f in semantic.outputs}
            ):
                continue
            content = (
                item.title + " " + (item.intent if isinstance(item, Capability) else item.procedure)
            )
            if text is not None and text.casefold() not in content.casefold():
                continue
            matches.append(
                {
                    "definition": item.to_dict(),
                    "status": self.status_for(item.ref, scenario=scenario),
                    "basis": "Explicit discovery filters; input suitability not checked",
                }
            )
        return tuple(matches)

    def benchmarks_for(self, capability_ref):
        self.get(capability_ref)
        return tuple(
            sorted(
                (
                    item
                    for item in self.definitions()
                    if isinstance(item, BenchmarkSpec) and item.capability_ref == capability_ref
                ),
                key=_sort_key,
            )
        )

    def export_bundle(self):
        documents = [item.to_dict() for item in sorted(self.definitions(), key=_sort_key)]
        return {
            "schema": "praxis.catalog-bundle/0.1",
            "documents": documents,
            "digest": digest(documents),
        }

    def import_bundle(self, bundle, *, migrations=None):
        """Validate all schemas/links/conflicts before admission; retain exact scientific refs.

        Explicit schema adapters apply to incoming documents only. Existing local
        snapshots remain immutable. IO failure may leave admitted objects; repeated
        admission with identical content is safe and never rewrites history.
        """
        from ..errors import ConflictError, IntegrityError

        if (
            type(bundle) is not dict
            or set(bundle) != {"schema", "documents", "digest"}
            or bundle["schema"] != "praxis.catalog-bundle/0.1"
            or bundle["digest"] != digest(bundle["documents"])
        ):
            raise IntegrityError("Invalid catalog bundle or content digest")
        definitions = {}
        for raw in bundle["documents"]:
            document = snapshot(raw)
            if document.get("schema") not in _TYPES:
                adapter = (migrations or {}).get(document.get("schema"))
                if adapter is None:
                    raise DefinitionError("Bundle schema needs an explicit migration adapter")
                document = snapshot(adapter(document))
                if document.get("ref") != raw.get("ref"):
                    raise DefinitionError(
                        "Schema migration must not silently change scientific identity"
                    )
            cls = _TYPES.get(document.get("schema"))
            if cls is None:
                raise DefinitionError("Migration did not produce a supported schema")
            definition = cls.from_dict(document)
            if definition.ref in definitions and digest(definitions[definition.ref]) != digest(
                definition
            ):
                raise ConflictError("Bundle contains conflicting scientific identities")
            definitions[definition.ref] = definition
            try:
                existing = self.get(definition.ref)
            except FileNotFoundError:
                pass
            else:
                if digest(existing) != digest(definition):
                    raise ConflictError("Bundle conflicts with preserved local history")

        def get(ref):
            return definitions[ref] if ref in definitions else self.get(ref)

        for definition in definitions.values():
            self._validate_links(definition, get)
            seen = {definition.ref}
            previous = getattr(definition, "supersedes", None)
            while previous is not None:
                if previous in seen:
                    raise DefinitionError("Cyclic review revision history")
                seen.add(previous)
                previous = getattr(get(previous), "supersedes", None)
        for definition in definitions.values():
            self.store.put(definition.ref, definition)
        return tuple(definitions)

    def load_bundled(self, name="hydrogen_refinement", *, version="1"):
        if name != "hydrogen_refinement":
            raise DefinitionError("Unknown bundled collection")
        if version not in {"1", "2"}:
            raise DefinitionError("Unknown bundled scientific definition version")
        suffix = "" if version == "1" else "_v2"
        root = files("praxis").joinpath("data", name)
        for filename in tuple(
            stem + suffix + ".json"
            for stem in ("capability", "hydride_protocol", "openmm_protocol")
        ):
            document = json.loads(root.joinpath(filename).read_text(encoding="utf-8"))
            self.register(_TYPES[document["schema"]].from_dict(document))


class _SnapshotStore:
    def __init__(self, documents):
        self._documents = {
            digest(MethodRef.from_dict(item["ref"])): snapshot(item) for item in documents
        }

    def get(self, identity):
        try:
            return snapshot(self._documents[digest(identity)])
        except KeyError:
            raise FileNotFoundError("Definition is absent from the frozen catalog") from None

    def documents(self):
        return iter(snapshot(list(self._documents.values())))

    def put(self, *args):
        raise DefinitionError("A preserved catalog snapshot is read-only")


def snapshot_catalog(documents):
    catalog = Catalog.__new__(Catalog)
    catalog.store = _SnapshotStore(documents)
    tuple(catalog.definitions())
    return catalog
