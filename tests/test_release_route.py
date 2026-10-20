"""Read-only publication gates must reject stale, incomplete or occupied candidates."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "praxis_release_route", ROOT / "devtools/release_route.py"
)
route = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(route)
COORDINATE = "noarch/praxis-0.1.0-py_0.tar.bz2"
DIGEST = "a" * 64


def registry(*, digest=DIGEST, labels=("main",)):
    return {
        "files": [
            {"basename": COORDINATE, "version": "0.1.0", "sha256": digest, "labels": list(labels)}
        ]
    }


def test_occupied_coordinate_under_another_label_is_never_overwritten():
    with pytest.raises(ValueError, match="occupied"):
        route.require_unoccupied(registry(labels=("staging",)), COORDINATE)


def test_changed_public_bytes_are_rejected():
    with pytest.raises(ValueError, match="digest"):
        route.verify_public(registry(digest="b" * 64), COORDINATE, "0.1.0", DIGEST)


def test_staged_file_is_not_public_delivery():
    with pytest.raises(ValueError, match="main label"):
        route.verify_public(registry(labels=("staging",)), COORDINATE, "0.1.0", DIGEST)


def test_invalid_registry_response_does_not_mean_unoccupied():
    with pytest.raises(ValueError, match="Invalid registry"):
        route.require_unoccupied({}, COORDINATE)


def producer():
    source = "c" * 40
    run = {
        "head_sha": source,
        "conclusion": "success",
        "status": "completed",
        "head_branch": "main",
        "head_repository": {"full_name": "uibcdf/praxis"},
        "path": ".github/workflows/tests.yml",
    }
    names = ["quality", "candidate / build", "Publish measured default-branch coverage"]
    names += [
        f"tests ({system}, {minor})"
        for system in ("ubuntu-latest", "macos-latest")
        for minor in ("3.11", "3.12", "3.13", "3.14")
    ]
    return run, [{"name": name, "conclusion": "success"} for name in names], source


def test_complete_exact_producer_and_empty_coordinate_pass():
    run, jobs, source = producer()
    route.validate_run(run, jobs, source)
    route.require_unoccupied({"files": []}, COORDINATE)
    route.verify_public(registry(), COORDINATE, "0.1.0", DIGEST)


def test_another_source_commit_cannot_certify_publication():
    run, jobs, _ = producer()
    with pytest.raises(ValueError, match="exact-head"):
        route.validate_run(run, jobs, "d" * 40)


def test_skipped_coverage_cannot_be_used_as_passed_gate():
    run, jobs, source = producer()
    jobs[2]["conclusion"] = "skipped"
    with pytest.raises(ValueError, match="passing required job"):
        route.validate_run(run, jobs, source)


def test_missing_installed_platform_lane_blocks_publication():
    run, jobs, source = producer()
    with pytest.raises(ValueError, match="passing required job"):
        route.validate_run(run, jobs[:-1], source)
