"""Packaging routes must retain the public runtime closure before expensive builds."""

import importlib.util
import shutil
from pathlib import Path

import pytest
from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]
MODULE = importlib.util.spec_from_file_location(
    "praxis_dependency_preflight", ROOT / "devtools/check_dependencies.py"
)
preflight = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(preflight)


@pytest.fixture
def routes(tmp_path):
    shutil.copy(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    shutil.copytree(ROOT / "devtools", tmp_path / "devtools")
    shutil.copytree(ROOT / ".github", tmp_path / ".github")
    return tmp_path


def test_runtime_metadata_and_all_declared_routes_agree(routes):
    assert preflight.audit(routes)["project"] == "praxis"


def test_missing_recipe_runtime_dependency_is_rejected(routes):
    path = routes / "devtools/conda-build/meta.yaml"
    path.write_text(path.read_text().replace("    - pyunitwizard >=0.28.1,<0.29\n", ""))
    with pytest.raises(ValueError, match="pyunitwizard"):
        preflight.audit(routes)


def test_stale_environment_floor_is_rejected(routes):
    path = routes / "devtools/conda-envs/test_env.yaml"
    path.write_text(path.read_text().replace("pyunitwizard=0.28.1", "pyunitwizard>=0.27,<0.29"))
    with pytest.raises(ValueError, match="pyunitwizard"):
        preflight.audit(routes)


def test_unclassified_runtime_route_is_rejected(routes):
    shutil.copy(
        routes / "devtools/conda-envs/test_env.yaml", routes / "devtools/conda-envs/another.yaml"
    )
    with pytest.raises(ValueError, match="Unclassified"):
        preflight.audit(routes)


def test_optional_provider_below_declared_floor_is_rejected(routes):
    path = routes / "devtools/conda-envs/test_env.yaml"
    path.write_text(path.read_text().replace("ackredit=0.12.0", "ackredit=0.10.1"))
    with pytest.raises(ValueError, match="optional ackredit"):
        preflight.audit(routes)


def test_source_candidate_below_public_floor_is_rejected():
    with pytest.raises(ValueError, match="violates"):
        preflight.check_source_candidate(
            "pyunitwizard",
            "0.28.0",
            "a" * 40,
            {"pyunitwizard": Requirement("pyunitwizard>=0.28.1,<0.29")},
        )


def test_no_deps_ci_requires_classified_conda_runtime(routes):
    path = routes / ".github/workflows/tests.yml"
    path.write_text(
        path.read_text().replace(
            "environment-file: devtools/conda-envs/test_env.yaml", "environment-file: absent.yaml"
        )
    )
    with pytest.raises(ValueError, match="unclassified CI"):
        preflight.audit(routes)
