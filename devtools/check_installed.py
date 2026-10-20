"""Qualify an installed candidate's identity, resources and dependency constraints."""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import tomllib
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name


def installed_versions(distributions):
    versions = {}
    for distribution in distributions:
        name = canonicalize_name(distribution.metadata["Name"])
        if name in versions and versions[name] != distribution.version:
            raise ValueError("Conflicting installed distribution metadata: " + name)
        versions[name] = distribution.version
    return dict(sorted(versions.items()))


def check_dependency_versions(project, versions, *, require_optional=True):
    requirements = list(project["dependencies"])
    if require_optional:
        for entries in project["optional-dependencies"].values():
            requirements.extend(entries)
    for text in requirements:
        required = Requirement(text)
        version = versions.get(canonicalize_name(required.name))
        if version is None or not required.specifier.contains(version):
            raise ValueError(f"Installed {required.name} {version} violates {required}")


def check(root, manifest, artifact, *, require_optional=True):
    import praxis

    root = Path(root).resolve()
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    package = Path(praxis.__file__).resolve().parent
    if package.is_relative_to(root):
        raise ValueError("Praxis resolves to the source checkout, not the installed artifact")
    if praxis.__version__ != project["version"] or manifest["version"] != project["version"]:
        raise ValueError("Installed runtime version differs")
    versions = installed_versions(importlib.metadata.distributions())
    if versions.get("praxis") != project["version"]:
        raise ValueError("Installed distribution version differs")
    if not SpecifierSet(project["requires-python"]).contains(platform.python_version()):
        raise ValueError("Installed Python violates requires-python")
    key = "conda_sha256" if str(artifact).endswith(".tar.bz2") else "wheel_sha256"
    if hashlib.sha256(Path(artifact).read_bytes()).hexdigest() != manifest[key]:
        raise ValueError("Installed candidate artifact digest differs")
    for name, digest in manifest["runtime_hashes"].items():
        path = package.parent / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("Installed resource differs: " + name)
    check_dependency_versions(project, versions, require_optional=require_optional)
    # Exercise a resource-loading path from the installed package.
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        praxis.Catalog(directory).load_bundled(version="2")
    return {
        "version": praxis.__version__,
        "python": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine(),
        "executable": sys.executable,
        "import_path": str(package),
        "artifact": Path(artifact).name,
        "artifact_sha256": manifest[key],
        "runtime_files": len(manifest["runtime_hashes"]),
        "packages": versions,
        "scope": "Installed identity/resources/dependency constraints; pytest results recorded separately",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if commit != manifest["source_commit"]:
        raise ValueError("Artifact manifest comes from a different source commit")
    result = check(Path(__file__).resolve().parents[1], manifest, args.artifact)
    result["source_commit"] = commit
    args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
