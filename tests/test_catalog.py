import json
import subprocess
import sys
from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD

import praxis
from praxis.errors import ConflictError, DefinitionError, IntegrityError


def test_history_reopens_and_assessment_never_rewrites_method(workspace, tmp_path):
    catalog, _ = workspace
    original = catalog.get(RMSD)
    revised = replace(
        original, ref=replace(RMSD, version="2"), procedure="Revised fixture procedure"
    )
    catalog.register(revised)
    assessment = praxis.Assessment(
        praxis.MethodRef("assessment", "fixture.review", "1"),
        RMSD,
        "fixture reviewer",
        "fixture review only",
        "2026-10-08",
        "two synthetic coordinate cases",
        ("paired displacement is finite",),
        ("supported for these fictional cases",),
        "supported",
        supporting_refs=("fixture:retained-example@1",),
        limitations=("Not protein validation",),
    )
    catalog.register(assessment)
    reopened = praxis.Catalog.open(tmp_path / "catalog")
    assert reopened.get(RMSD) == original
    assert reopened.get(revised.ref) == revised
    assert reopened.get(RMSD).status == "experimental"
    assert reopened.assessments_for(RMSD) == (assessment,)
    assert reopened.assessments_for(revised.ref) == ()


def test_same_reference_is_idempotent_but_different_content_conflicts(workspace):
    catalog, _ = workspace
    protocol = catalog.get(RMSD)
    catalog.register(protocol)
    with pytest.raises(ConflictError):
        catalog.register(
            replace(protocol, procedure="Different meaning under the same exact version")
        )
    assert catalog.get(RMSD) == protocol


def test_scientific_identity_cannot_escape_storage(workspace, tmp_path):
    catalog, _ = workspace
    original = catalog.get(CAPABILITY)
    reference = replace(CAPABILITY, identifier="../../outside/../method")
    catalog.register(replace(original, ref=reference))
    assert catalog.get(reference).ref == reference
    assert all(
        path.parent == tmp_path / "catalog" for path in catalog.store.directory.glob("*.json")
    )


def test_tampered_catalog_is_rejected(workspace):
    catalog, _ = workspace
    path = catalog.store.path(RMSD)
    envelope = json.loads(path.read_text())
    envelope["document"]["procedure"] = "Silent alteration"
    path.write_text(json.dumps(envelope))
    with pytest.raises(IntegrityError):
        catalog.get(RMSD)


def test_unknown_fields_and_wrong_schema_are_rejected(workspace):
    catalog, _ = workspace
    document = catalog.get(RMSD).to_dict()
    document["unrecognized"] = "must not disappear silently"
    with pytest.raises(DefinitionError):
        praxis.Protocol.from_dict(document)
    document.pop("unrecognized")
    document["schema"] = "praxis.protocol/999"
    with pytest.raises(DefinitionError):
        praxis.Protocol.from_dict(document)


def test_protocol_cannot_override_common_requirement(workspace):
    catalog, _ = workspace
    protocol = catalog.get(RMSD)
    with pytest.raises(DefinitionError):
        catalog.register(
            replace(
                protocol,
                ref=replace(RMSD, version="2"),
                requirements=(praxis.Requirement("paired_coordinates", "Weaker substitute"),),
            )
        )


def test_unassociated_candidate_can_be_registered_but_not_discovered_for_capability(workspace):
    catalog, _ = workspace
    candidate = replace(
        catalog.get(RMSD), ref=replace(RMSD, identifier="candidate"), capability_ref=None
    )
    catalog.register(candidate)
    assert catalog.get(candidate.ref).capability_ref is None
    assert candidate not in catalog.protocols_for(CAPABILITY)


def test_conflicting_assessments_are_both_retained(workspace):
    catalog, _ = workspace
    first = praxis.Assessment(
        praxis.MethodRef("assessment", "review", "1"),
        RMSD,
        "reviewer",
        "fixture review",
        "2026-10-08",
        "synthetic case",
        ("criterion",),
        ("unknown",),
        "inconclusive",
    )
    second = replace(
        first,
        ref=replace(first.ref, version="2"),
        outcome="challenged",
        findings=("counterexample",),
    )
    catalog.register(first)
    catalog.register(second)
    assert set(catalog.assessments_for(RMSD)) == {first, second}


def test_bundled_hydrogen_methods_expose_pending_tools(tmp_path):
    catalog = praxis.Catalog.open(tmp_path)
    catalog.load_bundled()
    catalog.load_bundled()  # same bytes are idempotent
    definitions = tuple(catalog.definitions())
    capability = next(item for item in definitions if isinstance(item, praxis.Capability))
    protocols = catalog.protocols_for(capability.ref)
    assert len(protocols) == 2
    assert all(item.pending and item.status == "experimental" for item in protocols)
    assert all(requirement.checker_ref is None for requirement in capability.requirements)
    assert "throughout" in next(
        item.description
        for item in capability.requirements
        if item.identifier == "frozen_enforcement"
    )


def test_import_and_catalog_read_do_not_load_optional_providers(tmp_path):
    code = """import sys, praxis
c = praxis.Catalog.open(sys.argv[1]); c.load_bundled(); list(c.definitions())
assert not {"ackredit", "recorda", "nextia", "hydride", "openmm", "argdigest", "depdigest", "smonitor"}.intersection(sys.modules)
"""
    subprocess.run([sys.executable, "-B", "-c", code, str(tmp_path)], check=True)
