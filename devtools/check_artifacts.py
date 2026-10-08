"""Verify private wheel and source archives against the current reviewable checkout."""

import argparse
import hashlib
import tarfile
import tomllib
import zipfile
from pathlib import Path


def check(root, wheel, sdist):
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
        for path in files:
            member = archive.extractfile(prefix + "/" + path.relative_to(root).as_posix())
            if member is None or member.read() != path.read_bytes():
                raise ValueError("Source runtime differs: " + str(path))
    return {
        "runtime_files": len(files),
        "wheel_sha256": hashlib.sha256(Path(wheel).read_bytes()).hexdigest(),
        "sdist_sha256": hashlib.sha256(Path(sdist).read_bytes()).hexdigest(),
        "scope": "Private local artifact/source consistency; not public dependency/platform qualification",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("sdist", type=Path)
    args = parser.parse_args()
    print(check(Path(__file__).resolve().parents[1], args.wheel, args.sdist))
