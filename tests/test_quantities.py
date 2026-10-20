from copy import deepcopy

import pytest
import pyunitwizard as puw
from pyunitwizard.record import RecordError

from praxis._quantities import duration_record, duration_seconds


def test_duration_uses_seconds_under_nondefault_application_policy():
    with puw.context(default_form="pint", standard_units=["nanosecond"]):
        record = duration_record(0.25, "benchmark.method_elapsed")
        assert duration_seconds(record, "benchmark.method_elapsed") == 0.25
        converted = puw.QuantityRecord.from_dict(record).to_quantity(
            field="benchmark.method_elapsed", unit="millisecond", form="pint"
        )
        assert float(puw.get_value(converted, to_unit="millisecond")) == 250
        assert set(puw.configure.get_standard_units()) == {"nanosecond"}


def test_duration_rejects_field_substitution_and_codec_tampering():
    record = duration_record(0.25, "benchmark.method_elapsed")
    with pytest.raises(RecordError):
        duration_seconds(record, "benchmark.evaluation_elapsed")
    damaged = deepcopy(record)
    damaged["manifest"]["unit"] = "nanosecond"
    with pytest.raises(RecordError):
        duration_seconds(damaged, "benchmark.method_elapsed")
