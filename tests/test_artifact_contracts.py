"""Each distribution route must carry its own complete, correctly versioned resources."""

import importlib.util
import io
import json
import tarfile
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "praxis_archives", ROOT / "devtools/check_artifacts.py"
)
archives = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archives)


def write_tar(path, members):
    with tarfile.open(path, "w:bz2" if path.name.endswith(".bz2") else "w:gz") as archive:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


@pytest.fixture
def candidate(tmp_path):
    runtime = {
        "praxis/__init__.py": b'__version__ = "0.1.0"\n',
        "praxis/data/definition.json": b'{"version": "2"}\n',
    }
    for name, data in runtime.items():
        path = tmp_path / "src" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    members = {}
    for name in (
        "tests/conftest.py",
        "examples/local_comparison.py",
        "examples/molsysmt_comparison.py",
        "devtools/check_dependencies.py",
        "devtools/dependency_routes.json",
        ".github/workflows/tests.yml",
        "devguide/FIRST_SLICE.md",
        "pyproject.toml",
    ):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = (
            b'[project]\nname = "praxis"\nversion = "0.1.0"\n'
            if name == "pyproject.toml"
            else b"fixture\n"
        )
        path.write_bytes(data)
        members["praxis-0.1.0/" + name] = data
    members.update({"praxis-0.1.0/src/" + name: data for name, data in runtime.items()})
    sdist = tmp_path / "praxis-0.1.0.tar.gz"
    write_tar(sdist, members)
    wheel = tmp_path / "praxis-0.1.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, data in runtime.items():
            archive.writestr(name, data)
        archive.writestr("praxis-0.1.0.dist-info/METADATA", "Name: praxis\nVersion: 0.1.0\n")
    conda = tmp_path / "praxis-0.1.0-py_0.tar.bz2"
    conda_members = {"site-packages/" + name: data for name, data in runtime.items()}
    conda_members["info/index.json"] = json.dumps(
        {
            "name": "praxis",
            "version": "0.1.0",
            "subdir": "noarch",
        }
    ).encode()
    write_tar(conda, conda_members)
    return tmp_path, wheel, sdist, conda, conda_members


def test_each_archive_matches_the_candidate(candidate):
    root, wheel, sdist, conda, _ = candidate
    result = archives.check(root, wheel, sdist, conda)
    assert result["runtime_files"] == 2 and result["conda_coordinate"]["subdir"] == "noarch"


def test_missing_conda_resource_rejected_even_when_wheel_passes(candidate):
    root, wheel, sdist, conda, members = candidate
    archives.check(root, wheel, sdist)
    del members["site-packages/praxis/data/definition.json"]
    write_tar(conda, members)
    with pytest.raises(ValueError, match="missing Conda"):
        archives.check(root, wheel, sdist, conda)


def test_stale_conda_identity_rejected_even_when_wheel_passes(candidate):
    root, wheel, sdist, conda, members = candidate
    archives.check(root, wheel, sdist)
    members["info/index.json"] = b'{"name":"praxis","version":"0.0.9","subdir":"noarch"}'
    write_tar(conda, members)
    with pytest.raises(ValueError, match="Conda package identity"):
        archives.check(root, wheel, sdist, conda)


def test_missing_wheel_resource_rejected_even_when_conda_is_complete(candidate):
    root, wheel, sdist, conda, _ = candidate
    with zipfile.ZipFile(wheel) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    del members["praxis/data/definition.json"]
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    with pytest.raises((KeyError, ValueError)):
        archives.check(root, wheel, sdist, conda)


def test_stale_embedded_runtime_version_is_rejected(candidate):
    root, wheel, sdist, conda, _ = candidate
    path = root / "src/praxis/__init__.py"
    path.write_bytes(b'__version__ = "0.0.9"\n')
    with zipfile.ZipFile(wheel) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    members["praxis/__init__.py"] = path.read_bytes()
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    with pytest.raises(ValueError, match="runtime version"):
        archives.check(root, wheel, sdist, conda)
