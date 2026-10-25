from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD

import praxis


@pytest.mark.parametrize("subject", [CAPABILITY, RMSD])
@pytest.mark.parametrize("human", [True, False])
def test_definition_audit_distinguishes_declared_human_review_from_missing_checker(
    workspace, subject, human
):
    catalog, _ = workspace
    requirement = praxis.Requirement(
        "review_or_check",
        "Declared requirement",
        review_required=human,
        human_authorities=("fixture reviewer",) if human else (),
    )
    definition = replace(
        catalog.get(subject),
        ref=replace(subject, version="audit-requirement"),
        requirements=(requirement,),
    )
    catalog.register(definition)
    audit = praxis.audit_definition(definition.ref, catalog=catalog)
    codes = {issue.code for issue in audit.issues}
    assert ("checker_unresolved" in codes) is not human
    assert {"admission_unreviewed", "validation_unresolved"} <= codes
    assert audit.outcome == "unverified"
