from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING
from test_reporting_benchmarks import spec

import praxis
from praxis.errors import DefinitionError, NotReadyError


def quantity(value, field, unit="angstrom"):
    import pyunitwizard as puw

    return puw.QuantityRecord.from_quantity(
        puw.quantity(value, unit, form="pint"), field=field, unit=unit
    ).to_dict()


def physical_spec(inputs):
    return replace(
        spec(inputs),
        metrics=(
            praxis.MetricDefinition(
                "distance",
                "Fixture numeric value interpreted in a declared test unit",
                "angstrom",
                "fixture.distance",
            ),
            praxis.MetricDefinition("score", "Dimensionless fixture score"),
        ),
        evaluator_configuration={"scale": 2},
    )


def metric(inputs, outputs, *, scale):
    return {
        "distance": quantity(outputs["score"] * scale, "fixture.distance"),
        "score": outputs["score"],
    }


def test_multiple_metrics_quantities_and_denominators(workspace, inputs):
    catalog, context = workspace
    specification = physical_spec(inputs)
    result = praxis.run_benchmark(
        specification,
        catalog=catalog,
        context=context,
        evaluators={specification.evaluator_ref: metric},
    )
    assert result.rows[0]["metric_status"] == "available"
    assert result.rows[0]["metric_value"] is None
    assert result.rows[0]["metrics"]["distance"]["value"]["manifest"]["field"] == "fixture.distance"
    summary = praxis.summarize_benchmark(result)
    assert summary["groups"][0]["metrics"][0]["unit"] == "angstrom"
    assert summary["groups"][0]["metrics"][0]["sample_standard_deviation"] == 0
    assert summary["groups"][1]["metrics"][0]["missing"] == 2
    assert praxis.load_benchmark(result.identifier, records=context.records) == result
    assert (
        praxis.audit_benchmark(result.identifier, records=context.records).outcome == "consistent"
    )
    assert catalog.benchmarks_for(CAPABILITY) == (specification,)


@pytest.mark.parametrize("bad", ["wrong_field", "wrong_dimension", "missing", "infinite"])
def test_invalid_measurement_is_not_quality_or_engine_failure(workspace, inputs, bad):
    catalog, context = workspace
    specification = physical_spec(inputs)

    def evaluator(inputs, outputs, *, scale):
        values = metric(inputs, outputs, scale=scale)
        if bad == "wrong_field":
            values["distance"] = quantity(1, "another.field")
        elif bad == "wrong_dimension":
            values["distance"] = quantity(1, "fixture.distance", "second")
        elif bad == "missing":
            values.pop("distance")
        else:
            values["score"] = float("inf")
        return values

    result = praxis.run_benchmark(
        specification,
        catalog=catalog,
        context=context,
        evaluators={specification.evaluator_ref: evaluator},
    )
    assert result.rows[0]["method_status"] == "completed"
    assert result.rows[0]["metric_status"] == "evaluator_failed"
    assert result.rows[0]["metrics"] == {}


def test_reanalysis_uses_outputs_without_methods_and_preserves_history(
    workspace, inputs, monkeypatch
):
    import praxis.benchmarks.runner as runner

    catalog, context = workspace
    original = spec(inputs)
    source = praxis.run_benchmark(
        original,
        catalog=catalog,
        context=context,
        evaluators={original.evaluator_ref: lambda i, o: o["score"]},
    )
    changed = replace(
        physical_spec(inputs),
        ref=replace(original.ref, version="2"),
        evaluator_ref=replace(original.evaluator_ref, version="2"),
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("Scientific methods must not run during reanalysis")

    monkeypatch.setattr(runner, "execute", forbidden)
    result = praxis.reanalyze_benchmark(
        source.identifier,
        changed,
        catalog=catalog,
        context=context,
        evaluators={changed.evaluator_ref: metric},
    )
    assert result.analysis_of == source.identifier
    assert [row["attempt_id"] for row in result.rows] == [row["attempt_id"] for row in source.rows]
    assert len([row for row in result.rows if row["metric_status"] == "available"]) == 2
    assert praxis.load_benchmark(source.identifier, records=context.records) == source
    assert (
        praxis.audit_benchmark(result.identifier, records=context.records).outcome == "consistent"
    )
    assert catalog.assessments_for(RMSD) == ()


def test_reanalysis_rejects_changed_sample(workspace, inputs):
    catalog, context = workspace
    original = spec(inputs)
    source = praxis.run_benchmark(
        original,
        catalog=catalog,
        context=context,
        evaluators={original.evaluator_ref: lambda i, o: o["score"]},
    )
    changed = replace(
        original,
        ref=replace(original.ref, version="2"),
        cases=(replace(original.cases[0], inputs={"left": [], "right": []}),),
    )
    with pytest.raises(ValueError, match="original cases"):
        praxis.reanalyze_benchmark(
            source.identifier,
            changed,
            catalog=catalog,
            context=context,
            evaluators={changed.evaluator_ref: lambda i, o: 0},
        )


def test_reanalysis_interruption_retains_planned_rows(workspace, inputs):
    catalog, context = workspace
    original = spec(inputs)
    source = praxis.run_benchmark(
        original,
        catalog=catalog,
        context=context,
        evaluators={original.evaluator_ref: lambda i, o: o["score"]},
    )
    changed = replace(original, ref=replace(original.ref, version="2"))
    calls = []

    def interrupted(i, o):
        calls.append(1)
        if len(calls) == 2:
            raise KeyboardInterrupt()
        return o["score"]

    with pytest.raises(KeyboardInterrupt) as error:
        praxis.reanalyze_benchmark(
            source.identifier,
            changed,
            catalog=catalog,
            context=context,
            evaluators={changed.evaluator_ref: interrupted},
            identifier="interrupted-analysis",
        )
    result = praxis.load_benchmark("interrupted-analysis", records=context.records)
    assert len(result.rows) == 4 and result.rows[0]["metric_status"] == "available"
    assert result.rows[1]["metric_status"] == "interrupted"
    assert "Praxis benchmark: interrupted-analysis" in error.value.__notes__


def test_replay_is_linked_and_comparison_is_explicit(workspace, prepared):
    catalog, context = workspace
    original_outputs, original = praxis.execute(prepared, catalog=catalog, context=context)
    preflight = praxis.replay_preflight(original.identifier, catalog=catalog, context=context)
    assert preflight.ready
    outputs, attempt, comparison = praxis.replay_execution(
        original.identifier,
        catalog=catalog,
        context=context,
        comparator=lambda before, after: praxis.CheckResult(
            "passed" if before == after else "failed", "Exact fixture equality"
        ),
        comparator_ref=praxis.MethodRef("extension", "fixture.equal", "1"),
    )
    assert outputs == original_outputs and attempt.replay_of == original.identifier
    assert attempt.identifier != original.identifier and comparison["outcome"] == "passed"
    assert (
        praxis.trace_execution(attempt.identifier, records=context.records)["prepared"]
        == prepared.to_dict()
    )
    assert catalog.assessments_for(RMSD) == ()


def test_replay_preflight_reports_environment_drift_without_execution(workspace, prepared):
    catalog, context = workspace
    _, original = praxis.execute(prepared, catalog=catalog, context=context)
    context.environment_metadata = {"container": "different"}
    preflight = praxis.replay_preflight(original.identifier, catalog=catalog, context=context)
    assert not preflight.ready and any("application" in reason for reason in preflight.reasons)
    with pytest.raises(NotReadyError):
        praxis.replay_execution(original.identifier, catalog=catalog, context=context)


def test_provenance_requires_an_explicit_mandatory_verifier(workspace, inputs):
    catalog, context = workspace
    protocol = catalog.get(RMSD)
    checked_ref = replace(RMSD, version="provenance")
    checker_ref = praxis.MethodRef("extension", "fixture.reference-available", "1")
    requirement = praxis.Requirement(
        "provider.reference",
        "Declared retained provider reference remains resolvable",
        "pre",
        checker_ref=checker_ref,
    )
    checked = replace(
        protocol,
        ref=checked_ref,
        provenance_requirements=(requirement.identifier,),
        provenance_checks=(requirement,),
    )
    catalog.register(checked)
    binding = context.extensions.bindings[RMSD_BINDING]
    binding_ref = replace(RMSD_BINDING, version="provenance")
    context.extensions.register_binding(replace(binding, ref=binding_ref, protocol_ref=checked_ref))
    availability = [True]
    context.extensions.register_checker(
        checker_ref,
        lambda i, c, o: praxis.CheckResult(
            "passed" if availability[0] else "failed",
            "Provider lookup result; no scientific calculation",
        ),
    )
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=checked_ref, binding_ref=binding_ref),
        catalog=catalog,
        context=context,
    )
    assert prepared.ready
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    availability[0] = False
    preflight = praxis.replay_preflight(attempt.identifier, catalog=catalog, context=context)
    assert not preflight.ready
    assert any(
        finding["requirement"] == requirement.identifier and finding["outcome"] == "failed"
        for finding in preflight.findings
    )
    assert (
        praxis.audit_execution(attempt.identifier, records=context.records).outcome == "consistent"
    )


def test_invalid_seed_controls_cannot_overwrite_configuration(inputs):
    with pytest.raises(DefinitionError, match="one integer"):
        replace(spec(inputs), seeds=(1,), seed_parameter="seed")
    with pytest.raises(DefinitionError, match="overwrite"):
        replace(
            spec(inputs),
            seeds=(1, 2),
            seed_parameter="seed",
            methods=(praxis.BenchmarkMethod(RMSD, RMSD_BINDING, {"seed": 99}),),
        )
