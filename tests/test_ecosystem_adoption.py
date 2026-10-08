"""Adoption checks cover application authority and public invalid-input behavior."""

import os
import subprocess
import sys

import pytest

import praxis
from praxis.errors import DefinitionError


def test_application_quantity_policy_survives_import_and_first_request():
    code = """from copy import deepcopy
import pyunitwizard as puw
with puw.context(default_form="pint", standard_units=["nanosecond"]):
    before = (deepcopy(puw.configure.get_standard_units()),
              puw.configure.get_default_form(), puw.configure.get_default_parser())
    import praxis
    from praxis._arguments import request_values
    from praxis._quantities import duration_record, duration_seconds
    request_values({"value": 1}, {})
    assert duration_seconds(duration_record(0.25, "duration"), "duration") == 0.25
    after = (puw.configure.get_standard_units(), puw.configure.get_default_form(),
             puw.configure.get_default_parser())
    assert after == before
"""
    subprocess.run(
        [sys.executable, "-B", "-c", code],
        check=True,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
    )


@pytest.mark.parametrize("invalid", [[], {"value": float("nan")}, {"value": object()}])
def test_public_request_rejects_non_object_or_non_json_arguments(invalid):
    with pytest.raises(DefinitionError):
        praxis.MethodRequest(praxis.MethodRef("capability", "fixture", "1"), invalid)
