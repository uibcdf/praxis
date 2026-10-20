"""Optional provider qualification, separate from the dependency-free core fixtures."""

from pathlib import Path

import pytest

import praxis
from praxis._quantities import quantity_value


def test_real_molsysmt_workflow_keeps_units_conventions_and_failures(tmp_path):
    msm = pytest.importorskip("molsysmt")
    from molsysmt_comparison import DIRECT, FITTED, run

    path = Path(msm.__file__).parent / "data" / "pdb" / "1vii.pdb"
    if not path.is_file():
        pytest.skip("This provider distribution does not include the local PDB qualification case")
    result = run(tmp_path, path)
    assert len(result.rows) == 6
    assert sum(row["method_status"] == "blocked" for row in result.rows) == 2
    records = praxis.MethodRecords(tmp_path / "records")
    for row in result.rows[:4]:
        attempt = records.attempt(row["attempt_id"])
        assert attempt.contract_status == "supported"
        assert attempt.outputs["provider_version"] == msm.__version__
        value = float(
            quantity_value(attempt.outputs["rmsd"], field="comparison.rmsd", unit="nanometer")
        )
        expected = (
            1 if row["case"] == "translated" and row["protocol_ref"] == DIRECT.to_dict() else 0
        )
        assert value == pytest.approx(expected, abs=1e-6)
        if row["protocol_ref"] == FITTED.to_dict():
            assert attempt.outputs["convention"] == "optimal_superposition"
        else:
            assert attempt.outputs["convention"] == "fixed_frame"
        assert praxis.replay_preflight(
            attempt.identifier,
            catalog=praxis.Catalog.open(tmp_path / "catalog"),
            context=__import__("molsysmt_comparison").build(tmp_path, path)[1],
        ).ready
    assert praxis.audit_benchmark(result.identifier, records=records).outcome == "consistent"
    assert "comparison.rmsd" in (tmp_path / "benchmark.md").read_text()
