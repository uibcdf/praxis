"""Use the provider's sealed quantity codec, with an explicit field/unit handshake."""


def duration_record(seconds, field):
    import pyunitwizard as puw

    quantity = puw.quantity(seconds, "second", form="pint")
    return puw.QuantityRecord.from_quantity(quantity, field=field, unit="second").to_dict()


def duration_seconds(document, field):
    import pyunitwizard as puw

    quantity = puw.QuantityRecord.from_dict(document).to_quantity(
        field=field, unit="second", dimensionality={"[T]": 1}, form="pint"
    )
    import math

    value = float(puw.get_value(quantity, to_unit="second"))
    if not math.isfinite(value):
        raise ValueError("Duration must be finite")
    return value


def quantity_value(document, *, field, unit):
    """Decode the shared sealed codec in the contract's unit; never change application policy."""
    import pyunitwizard as puw

    quantity = puw.QuantityRecord.from_dict(document).to_quantity(
        field=field, unit=unit, form="pint"
    )
    return puw.get_value(quantity, to_unit=unit)


def quantity_record(quantity, *, field, unit):
    import pyunitwizard as puw

    return puw.QuantityRecord.from_quantity(quantity, field=field, unit=unit).to_dict()
