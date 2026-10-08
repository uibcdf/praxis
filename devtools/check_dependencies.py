"""Read-only dependency-route preflight; interval parsing adapted from Recorda's MIT tool.

Owns Praxis route inventory, not a new MOLI contract. No network or source installation.
"""

import json
import re
import sys
import tomllib
from pathlib import Path

import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version


def bounds(specifiers):
    lower, upper = None, None
    for spec in specifiers:
        op, text = spec.operator, spec.version
        if op == "==" and text.endswith(".*"):
            parts = list(map(int, text[:-2].split(".")))
            next_parts = [*parts[:-1], parts[-1] + 1]
            candidates = [
                (">=", Version(text[:-2])),
                ("<", Version(".".join(map(str, next_parts)))),
            ]
        elif op in {">=", ">", "<=", "<", "=="}:
            candidates = [(op, Version(text))]
        else:
            raise ValueError(f"unsupported preflight constraint: {spec}")
        for operator, version in candidates:
            if operator in {">=", ">", "=="}:
                candidate = (version, operator != ">")
                if (
                    lower is None
                    or candidate[0] > lower[0]
                    or (candidate[0] == lower[0] and not candidate[1])
                ):
                    lower = candidate
            if operator in {"<=", "<", "=="}:
                candidate = (version, operator != "<")
                if (
                    upper is None
                    or candidate[0] < upper[0]
                    or (candidate[0] == upper[0] and not candidate[1])
                ):
                    upper = candidate
    if (
        lower
        and upper
        and (lower[0] > upper[0] or (lower[0] == upper[0] and not (lower[1] and upper[1])))
    ):
        raise ValueError("empty runtime constraint")
    return lower, upper


def contained(candidate, required):
    lo, hi = bounds(candidate)
    rlo, rhi = bounds(required)
    return not (
        rlo
        and (lo is None or lo[0] < rlo[0] or (lo[0] == rlo[0] and lo[1] and not rlo[1]))
        or rhi
        and (hi is None or hi[0] > rhi[0] or (hi[0] == rhi[0] and hi[1] and not rhi[1]))
    )


def conda_requirement(text):
    match = re.fullmatch(r"([A-Za-z0-9_-]+)\s*(.*)", text)
    if not match:
        raise ValueError(f"invalid Conda dependency: {text}")
    name, constraint = match.groups()
    if constraint.startswith("=") and not constraint.startswith("=="):
        version = constraint[1:].split("=", 1)[0]
        if len(version.split(".")) < 3:
            version += ".*"
        constraint = "==" + version
    return Requirement(name + constraint.replace(" ", ""))


def check_source_candidate(name, version, commit, required):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"{name}: sibling source needs a full commit SHA")
    requirement = required.get(canonicalize_name(name))
    if requirement is None or not requirement.specifier.contains(version):
        raise ValueError(f"{name}: source version {version} violates {requirement}")


def audit(root):
    root = Path(root)
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    required = {canonicalize_name(r.name): r for r in map(Requirement, project["dependencies"])}
    required["python"] = Requirement("python" + project["requires-python"])
    inventory = json.loads((root / "devtools/dependency_routes.json").read_text())
    for kind, directory, pattern in (
        ("environments", "devtools/conda-envs", "*.yaml"),
        ("recipes", "devtools/conda-build", "**/meta.yaml"),
    ):
        discovered = {str(path.relative_to(root)) for path in (root / directory).glob(pattern)}
        if discovered != set(inventory[kind]):
            raise ValueError("Unclassified or missing runtime route: " + kind)
        for route in inventory[kind]:
            data = yaml.safe_load((root / route).read_text())
            entries = data["requirements"]["run"] if kind == "recipes" else data["dependencies"]
            supplied = {
                canonicalize_name(r.name): r
                for r in map(conda_requirement, (item for item in entries if isinstance(item, str)))
            }
            for name, requirement in required.items():
                candidate = supplied.get(name)
                if candidate is None or not contained(candidate.specifier, requirement.specifier):
                    raise ValueError(f"{route}: {name} has {candidate}; requires {requirement}")
            if kind == "recipes" and (
                data["package"]["name"] != project["name"]
                or str(data["package"]["version"]) != project["version"]
            ):
                raise ValueError(route + ": package identity differs from pyproject")
    workflows = {
        str(path.relative_to(root)) for path in (root / ".github/workflows").glob("*.y*ml")
    }
    if workflows != set(inventory["workflows"]):
        raise ValueError("Unclassified or missing workflow route")
    for route in inventory["workflows"]:
        for job in yaml.safe_load((root / route).read_text()).get("jobs", {}).values():
            steps = job.get("steps", [])
            environments = [
                step.get("with", {}).get("environment-file")
                for step in steps
                if step.get("uses", "").startswith("mamba-org/setup-micromamba@")
            ]
            if any(item not in inventory["environments"] for item in environments):
                raise ValueError(route + ": unclassified CI environment")
            installs = any(
                re.search(r"pip install[^\n]*\s\.\s*(?:$|\n)", step.get("run", ""))
                for step in steps
            )
            if installs and not environments:
                raise ValueError(route + ": no Conda runtime route for local no-deps installation")
            if any(
                step.get("uses", "").startswith("actions/checkout@")
                and step.get("with", {}).get("repository")
                for step in steps
            ):
                raise ValueError(route + ": sibling source route requires explicit review")
    for source in inventory["sibling_sources"]:
        check_source_candidate(source["name"], source["version"], source["commit"], required)
    return {
        "project": project["name"],
        "routes": inventory,
        "scope": "Declared constraints only; no solver, public channel or installed-provider qualification",
    }


if __name__ == "__main__":
    try:
        audit(Path(__file__).resolve().parents[1])
    except (ValueError, KeyError, OSError) as error:
        print("Dependency preflight rejected: " + str(error), file=sys.stderr)
        raise SystemExit(1)
    print("Praxis dependency route constraints are consistent.")
