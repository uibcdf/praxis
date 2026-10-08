import hashlib
import importlib.util
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "praxis_coverage", ROOT / "devtools/normalize_coverage.py"
)
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


@pytest.fixture
def report(tmp_path):
    source = tmp_path / "src/praxis/module.py"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"value = 1\nunused = 2\n")
    installed = tmp_path / "installed/praxis"
    xml = tmp_path / "coverage.xml"
    xml.write_text(f'''<coverage lines-valid="2" lines-covered="1" line-rate="0.5">
      <sources><source></source></sources><packages><package name="installed.praxis">
      <classes><class name="module.py" filename="{installed / "module.py"}">
      <lines><line number="1" hits="1"/><line number="2" hits="0"/></lines>
      </class></classes></package></packages></coverage>''')
    observation = {
        "source_commit": "a" * 40,
        "artifact_sha256": "b" * 64,
        "import_path": str(installed),
    }
    manifest = {
        "source_commit": "a" * 40,
        "conda_sha256": "b" * 64,
        "runtime_hashes": {"praxis/module.py": hashlib.sha256(source.read_bytes()).hexdigest()},
    }
    return tmp_path, xml, observation, manifest


def test_mapping_preserves_all_line_hits_and_totals(report):
    root, xml, observation, manifest = report
    before = ET.parse(xml)
    output = root / "normalized.xml"
    coverage.normalize(root, xml, observation, manifest, output)
    after = ET.parse(output)
    assert after.getroot().attrib == before.getroot().attrib
    assert [v.attrib for v in after.findall(".//line")] == [
        v.attrib for v in before.findall(".//line")
    ]
    assert after.find(".//class").attrib["filename"] == "src/praxis/module.py"


def test_changed_source_cannot_receive_installed_coverage(report):
    root, xml, observation, manifest = report
    (root / "src/praxis/module.py").write_text("value = 100\n")
    with pytest.raises(ValueError, match="differs"):
        coverage.normalize(root, xml, observation, manifest, root / "normalized.xml")


def test_unrelated_package_cannot_be_mapped_as_praxis(report):
    root, xml, observation, manifest = report
    observation["import_path"] = str(root / "other")
    with pytest.raises(ValueError, match="unexpected"):
        coverage.normalize(root, xml, observation, manifest, root / "normalized.xml")


def test_another_artifact_cannot_supply_coverage(report):
    root, xml, observation, manifest = report
    observation["artifact_sha256"] = "c" * 64
    with pytest.raises(ValueError, match="another artifact"):
        coverage.normalize(root, xml, observation, manifest, root / "normalized.xml")
