"""Verify private wheel and source archives against the current reviewable checkout."""

import argparse
import hashlib
import json
import subprocess
import tarfile
import tomllib
import zipfile
from pathlib import Path


def check(root, wheel, sdist, conda=None):
    root = Path(root)
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    files = sorted(
        path
        for path in (root / "src/praxis").rglob("*")
        if path.is_file() and path.suffix in {".py", ".json"}
    )
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        for path in files:
            name = path.relative_to(root / "src").as_posix()
            if archive.read(name) != path.read_bytes():
                raise ValueError("Wheel differs from checkout: " + name)
        actual = {
            name for name in names if name.startswith("praxis/") and name.endswith((".py", ".json"))
        }
        if actual != {path.relative_to(root / "src").as_posix() for path in files}:
            raise ValueError("Unexpected or missing wheel runtime resource")
        metadata = archive.read(
            next(name for name in names if name.endswith(".dist-info/METADATA"))
        ).decode()
        if "Version: " + project["version"] + "\n" not in metadata:
            raise ValueError("Wheel metadata version differs")
        if (
            f'__version__ = "{project["version"]}"'
            not in archive.read("praxis/__init__.py").decode()
        ):
            raise ValueError("Wheel runtime version differs")
    with tarfile.open(sdist) as archive:
        prefix = next(iter(archive.getnames())).split("/")[0]
        for relative in (
            "tests/conftest.py",
            "examples/local_comparison.py",
            "examples/molsysmt_comparison.py",
            "devtools/check_dependencies.py",
            "devtools/dependency_routes.json",
            ".github/workflows/tests.yml",
            "devguide/FIRST_SLICE.md",
            "pyproject.toml",
        ):
            member = archive.extractfile(prefix + "/" + relative)
            if member is None or member.read() != (root / relative).read_bytes():
                raise ValueError("Source archive cannot reproduce checkout: " + relative)
        source_files = set()
        for directory in ("tests", "examples", "devtools", "devguide", ".github"):
            source_files.update(
                path
                for path in (root / directory).rglob("*")
                if path.is_file()
                and path.suffix in {".py", ".json", ".yaml", ".yml", ".md", ".toml"}
            )
        for name in (
            "README.md",
            "CHANGELOG.md",
            "AGENTS.md",
            "MOLI_GUIDE.md",
            "NEXT_STEPS.md",
            "MANIFEST.in",
            "LICENSE",
        ):
            if (root / name).is_file():
                source_files.add(root / name)
        for path in sorted(source_files):
            relative = path.relative_to(root).as_posix()
            member = archive.extractfile(prefix + "/" + relative)
            if member is None or member.read() != path.read_bytes():
                raise ValueError("Source archive cannot reproduce checkout: " + relative)
        for path in files:
            member = archive.extractfile(prefix + "/" + path.relative_to(root).as_posix())
            if member is None or member.read() != path.read_bytes():
                raise ValueError("Source runtime differs: " + str(path))
    result = {
        "version": project["version"],
        "runtime_files": len(files),
        "runtime_hashes": {
            path.relative_to(root / "src").as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files
        },
        "wheel_sha256": hashlib.sha256(Path(wheel).read_bytes()).hexdigest(),
        "sdist_sha256": hashlib.sha256(Path(sdist).read_bytes()).hexdigest(),
        "scope": "Archive/source consistency; installed dependency/platform gates are separate",
    }
    if conda is not None:
        with tarfile.open(conda) as archive:
            index = json.load(archive.extractfile("info/index.json"))
            if index["name"] != project["name"] or index["version"] != project["version"]:
                raise ValueError("Conda package identity differs")
            expected = {"site-packages/" + name for name in result["runtime_hashes"]}
            actual = {
                name
                for name in archive.getnames()
                if name.startswith("site-packages/praxis/") and name.endswith((".py", ".json"))
            }
            if actual != expected:
                raise ValueError("Unexpected or missing Conda runtime resource")
            for path in files:
                name = "site-packages/" + path.relative_to(root / "src").as_posix()
                if archive.extractfile(name).read() != path.read_bytes():
                    raise ValueError("Conda differs from checkout: " + name)
        result["conda_sha256"] = hashlib.sha256(Path(conda).read_bytes()).hexdigest()
        result["conda_coordinate"] = {
            "owner": "uibcdf",
            "package": index["name"],
            "version": index["version"],
            "subdir": index["subdir"],
            "filename": Path(conda).name,
        }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("sdist", type=Path)
    parser.add_argument("--conda", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = check(Path(__file__).resolve().parents[1], args.wheel, args.sdist, args.conda)
    if subprocess.check_output(["git", "status", "--porcelain"], text=True).strip():
        raise ValueError("Archive receipt requires a clean committed candidate")
    result["source_commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
