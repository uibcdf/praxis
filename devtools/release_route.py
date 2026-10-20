"""Read-only gates for publishing the exact qualified Conda file; no registry writes."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

REPOSITORY = "uibcdf/praxis"
REGISTRY = "https://api.anaconda.org/package/uibcdf/praxis"


def read_json(url, *, token=None, absent_ok=False):
    headers = {"Accept": "application/json", "User-Agent": "praxis-release-review"}
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=headers), timeout=30
        ) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if absent_ok and error.code == 404:
            return {"files": []}
        raise ValueError(f"Registry/CI query failed with HTTP {error.code}") from error


def validate_run(run, jobs, source):
    if (
        run["head_sha"] != source
        or run["conclusion"] != "success"
        or run["status"] != "completed"
        or run["head_branch"] != "main"
        or run["head_repository"]["full_name"] != REPOSITORY
        or run["path"] != ".github/workflows/tests.yml"
    ):
        raise ValueError("Producer is not the successful exact-head default-branch test workflow")
    required = {"quality", "candidate / build", "Publish measured default-branch coverage"}
    required.update(
        f"tests ({system}, {minor})"
        for system in ("ubuntu-latest", "macos-latest")
        for minor in ("3.11", "3.12", "3.13", "3.14")
    )
    observed = {job["name"]: job["conclusion"] for job in jobs}
    if not required.issubset(observed) or any(value != "success" for value in observed.values()):
        raise ValueError("Exact candidate is missing a passing required job")


def matching_files(snapshot, coordinate):
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("files"), list):
        raise ValueError("Invalid registry snapshot")
    return [item for item in snapshot["files"] if item.get("basename") == coordinate]


def require_unoccupied(snapshot, coordinate):
    if matching_files(snapshot, coordinate):
        raise ValueError(
            "Conda coordinate is occupied under a label; never replace or force-upload"
        )


def verify_public(snapshot, coordinate, version, expected):
    matches = matching_files(snapshot, coordinate)
    if len(matches) != 1:
        raise ValueError("Public coordinate is missing or ambiguous")
    item = matches[0]
    if (
        item.get("version") != version
        or item.get("sha256") != expected
        or "main" not in item.get("labels", [])
    ):
        raise ValueError("Public coordinate version, digest or main label differs")


def identity(root, source, version, *, require_tag):
    if not re.fullmatch(r"[0-9a-f]{40}", source) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
    ):
        raise ValueError("Invalid full source SHA or public X.Y.Z version")
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=root).strip()
    if actual != source or project["version"] != version:
        raise ValueError("Checkout/version differs from release candidate")
    if require_tag:
        tagged = subprocess.check_output(
            ["git", "rev-parse", "--verify", f"refs/tags/{version}^{{commit}}"], text=True, cwd=root
        ).strip()
        if tagged != source:
            raise ValueError("Release tag differs from the qualified source")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("gates", "preflight", "verify-public"))
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = os.environ["PRAXIS_CANDIDATE_SHA"]
    version = os.environ["PRAXIS_RELEASE_VERSION"]
    publish = os.environ.get("PRAXIS_PUBLISH", "false")
    if publish not in {"true", "false"}:
        raise ValueError("Publish choice must be true or false")
    identity(root, source, version, require_tag=publish == "true")
    receipt = {"source_commit": source, "version": version, "command": args.command}
    if args.command == "gates":
        run_id = os.environ["PRAXIS_CANDIDATE_RUN_ID"]
        if not re.fullmatch(r"[1-9][0-9]*", run_id):
            raise ValueError("Candidate run ID must be numeric")
        token = os.environ["GH_TOKEN"]
        url = f"https://api.github.com/repos/{REPOSITORY}/actions/runs/{run_id}"
        run = read_json(url, token=token)
        attempt = run["run_attempt"]
        jobs = read_json(url + f"/attempts/{attempt}/jobs?per_page=100", token=token)
        if jobs["total_count"] != len(jobs["jobs"]):
            raise ValueError("Incomplete candidate job listing")
        validate_run(run, jobs["jobs"], source)
        artifact = f"praxis-candidate-{source}-{run_id}-{attempt}"
        receipt.update(run_url=run["html_url"], run_attempt=attempt, artifact_name=artifact)
        with open(os.environ["GITHUB_OUTPUT"], "a") as stream:
            stream.write("artifact_name=" + artifact + "\n")
    else:
        directory = root / "dist/candidate"
        manifest = json.loads((directory / "artifacts.json").read_text())
        if manifest["source_commit"] != source or manifest["version"] != version:
            raise ValueError("Downloaded candidate belongs to another source/version")
        name = f"praxis-{version}-py_0.tar.bz2"
        artifact = directory / name
        expected = manifest["conda_sha256"]
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
            raise ValueError("Downloaded candidate bytes differ")
        coordinate = "noarch/" + name
        receipt.update(coordinate=f"uibcdf/praxis/{version}/{coordinate}", artifact_sha256=expected)
        if args.command == "preflight":
            # The all-label package endpoint is independent of the write client.
            require_unoccupied(read_json(REGISTRY, absent_ok=True), coordinate)
            receipt["publication_credential_available"] = bool(
                os.environ.get("PRAXIS_UPLOAD_CREDENTIAL_PRESENT")
            )
            if publish == "true" and not os.environ.get("PRAXIS_UPLOAD_CREDENTIAL_PRESENT"):
                raise ValueError("ANACONDA_UIBCDF_TOKEN must be configured before publication")
            with open(os.environ["GITHUB_OUTPUT"], "a") as stream:
                stream.write(
                    "artifact="
                    + str(artifact)
                    + "\npackage_spec="
                    + receipt["coordinate"]
                    + "\nsha256="
                    + expected
                    + "\n"
                )
        else:
            for attempt in range(4):
                try:
                    verify_public(
                        read_json(REGISTRY, absent_ok=True), coordinate, version, expected
                    )
                    break
                except ValueError:
                    if attempt == 3:
                        raise
                    time.sleep(2)
            receipt["public_label"] = "main"
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
