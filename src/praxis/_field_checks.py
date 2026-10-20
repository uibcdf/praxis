"""Explicit field guarantees. Descriptive prose never becomes an inferred validator."""

import math
from dataclasses import replace

from ._serialization import snapshot
from .definitions import CheckFinding
from .errors import DefinitionError


def field_id(field, phase):
    return f"praxis.field/{phase}/{field.name}"


def structural_field(field, phase, values):
    """Inspect only built-in structural guarantees; custom field checks are separate."""
    identifier = field_id(field, phase)
    if field.name not in values:
        return CheckFinding(
            identifier,
            phase,
            "failed" if field.required else "skipped",
            field.required,
            None,
            "Required field is missing" if field.required else "Optional field was not supplied",
            coverage="field presence",
        )
    value = values[field.name]
    try:
        snapshot(value)
    except DefinitionError:
        return CheckFinding(
            identifier,
            phase,
            "failed",
            True,
            None,
            "Field is not a finite JSON value",
            coverage="JSON structure",
        )
    validator = field.validator
    if validator is None:
        return CheckFinding(
            identifier,
            phase,
            "undetermined",
            True,
            field.checker_ref,
            "Field representation has no executable structural validator",
        )
    if validator == "quantity":
        from ._quantities import quantity_value

        try:
            value = quantity_value(
                value,
                field=field.quantity_field or "protocol.parameter/" + field.name,
                unit=field.unit,
            )
            value = value.tolist() if hasattr(value, "tolist") else value
            snapshot(value)

            def numeric(item):
                return (
                    all(numeric(v) for v in item)
                    if type(item) is list
                    else type(item) in (int, float)
                )

            if not numeric(value):
                raise ValueError("Quantity must contain finite real numeric values")
        except Exception:
            return CheckFinding(
                identifier,
                phase,
                "failed",
                True,
                None,
                "Shared quantity codec, semantic field or physical unit check failed",
                coverage="sealed quantity and unit handshake",
            )
        return CheckFinding(
            identifier,
            phase,
            "passed",
            True,
            None,
            "Shared sealed quantity representation inspected",
            coverage="sealed quantity and unit handshake",
        )
    passed = {
        "json": True,
        "number": type(value) in (int, float),
        "finite_number": type(value) is int or type(value) is float and math.isfinite(value),
        "string": type(value) is str,
        "boolean": type(value) is bool,
        "array": type(value) is list,
        "object": type(value) is dict,
    }[validator]
    if not passed:
        return CheckFinding(
            identifier,
            phase,
            "failed",
            True,
            None,
            "Field does not satisfy its explicit structural validator",
            coverage="structural validator: " + validator,
        )
    if field.unit not in (None, "dimensionless"):
        return CheckFinding(
            identifier,
            phase,
            "undetermined",
            True,
            field.checker_ref,
            "Physical field requires a quantity-aware provider checker",
            coverage="structure only; unit guarantee unresolved",
        )
    return CheckFinding(
        identifier,
        phase,
        "passed",
        True,
        None,
        "Explicit structural field guarantee inspected",
        coverage="structural validator: " + validator,
    )


def field_findings(fields, phase, inputs, configuration, extensions, outputs=None):
    from .applicability import evaluate_check

    values = inputs if phase == "pre" else outputs or {}
    findings = []
    for field in fields:
        structural = structural_field(field, phase, values)
        if (
            field.checker_ref is not None
            and field.name in values
            and structural.outcome != "failed"
        ):
            structural = evaluate_check(
                field_id(field, phase),
                phase,
                True,
                field.checker_ref,
                inputs,
                configuration,
                extensions,
                outputs,
            )
        findings.append(structural)
    return tuple(findings)


def parameter_id(parameter):
    return "praxis.parameter/pre/" + parameter.name


def parameter_structural(parameter, configuration):
    finding = replace(
        structural_field(parameter, "pre", configuration), requirement=parameter_id(parameter)
    )
    if finding.outcome != "passed":
        return finding
    value = configuration[parameter.name]
    if parameter.unit not in (None, "dimensionless") and parameter.validator == "quantity":
        from ._quantities import quantity_value

        value = quantity_value(
            value,
            field=parameter.quantity_field or "protocol.parameter/" + parameter.name,
            unit=parameter.unit,
        )
        value = value.tolist() if hasattr(value, "tolist") else value
    if (parameter.minimum is not None or parameter.maximum is not None) and type(value) not in (
        int,
        float,
    ):
        return replace(finding, outcome="failed", reason="Bounded parameter must be a real scalar")
    if (
        parameter.minimum is not None
        and value < parameter.minimum
        or parameter.maximum is not None
        and value > parameter.maximum
    ):
        return replace(finding, outcome="failed", reason="Parameter lies outside declared bounds")
    if parameter.choices and configuration[parameter.name] not in parameter.choices:
        return replace(finding, outcome="failed", reason="Parameter is not a declared variant")
    return finding


def parameter_findings(parameters, inputs, configuration, extensions):
    from .applicability import evaluate_check

    findings = []
    for parameter in parameters:
        finding = parameter_structural(parameter, configuration)
        if (
            parameter.checker_ref is not None
            and parameter.name in configuration
            and finding.outcome != "failed"
        ):
            finding = evaluate_check(
                parameter_id(parameter),
                "pre",
                True,
                parameter.checker_ref,
                inputs,
                configuration,
                extensions,
            )
        findings.append(finding)
    return tuple(findings)
