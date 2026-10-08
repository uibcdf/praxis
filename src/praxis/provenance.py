"""Observed local environment and explicitly declared execution authority."""

import platform
from importlib.metadata import PackageNotFoundError, version

from ._serialization import digest, snapshot


def environment_manifest(dependencies=(), *, supplied=None):
    versions = {}
    for name in dict.fromkeys(
        (*dependencies, "praxis", "argdigest", "depdigest", "smonitor", "pyunitwizard")
    ):
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "packages": versions,
        "application": snapshot(supplied or {}),
        "scope": "Local platform and installed distribution metadata; no credentials or automatic GPU/container probes",
    }


def environment_findings(requirements, manifest):
    reasons = []
    for key in ("python", "system", "machine"):
        if key in requirements and requirements[key] != manifest[key]:
            reasons.append(
                f"Environment {key}: expected {requirements[key]!r}, observed {manifest[key]!r}"
            )
    for name, expected in requirements.get("packages", {}).items():
        actual = manifest["packages"].get(name)
        if actual is None or actual != expected:
            reasons.append(
                f"Environment package {name}: expected {expected!r}, observed {actual!r}"
            )
    if set(requirements) - {"python", "system", "machine", "packages"}:
        reasons.append("Environment requirements contain unverifiable fields")
    return tuple(reasons)


def invocation_digest(capability_ref, protocol_ref, inputs, configuration):
    return digest(
        {
            "capability": capability_ref.to_dict(),
            "protocol": protocol_ref.to_dict(),
            "inputs": inputs,
            "configuration": configuration,
        }
    )
