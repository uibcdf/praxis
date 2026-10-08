"""Sequential benchmarks with immutable per-row checkpoints and separate failure domains."""

import math
from dataclasses import replace
from time import perf_counter
from uuid import uuid4

from .._implementation import callable_identity
from .._quantities import duration_record, duration_seconds, quantity_value
from .._serialization import snapshot
from ..errors import RecordingError
from ..execution.reports import MethodRequest
from ..execution.runner import execute, now, prepare
from ..provenance import environment_manifest
from ..recording import NoRecorder
from .definitions import BenchmarkResult, BenchmarkSpec

_STAGES = (
    "prepared",
    "method_started",
    "method",
    "evaluation_started",
    "metric_computed",
    "evaluated",
)


def _row(spec, case, method, replicate):
    return {
        "case": case.identifier,
        "scenario": case.scenario,
        "protocol_ref": method.protocol_ref.to_dict(),
        "binding_ref": method.binding_ref.to_dict(),
        "replicate": replicate,
        "seed": spec.seeds[replicate] if spec.seeds else None,
        "metrics": {},
        "evaluator_configuration": snapshot(spec.evaluator_configuration),
        "attempt_id": None,
        "prepared_id": None,
        "method_status": "not_started",
        "contract_status": "unassessed",
        "method_recording_status": "not_started",
        "metric_status": "unavailable",
        "metric_value": None,
        "failure_type": None,
        "timing_scope": "prepare through execute return/failure inspection, including initial row checkpoints and requested method recording; excludes terminal row checkpoint and evaluation",
        "elapsed": None,
        "evaluator_ref": spec.evaluator_ref.to_dict(),
        "evaluation_started": None,
        "evaluation_finished": None,
        "evaluation_elapsed": None,
        "evaluation_timing_scope": "evaluator + snapshot checkpoints + operation recording",
        "evaluation_failure_type": None,
        "evaluation_recording_status": "not_started",
        "recording_failure_type": None,
        "evaluation_recording_refs": [],
    }


def _checkpoint(records, identifier, ordinal, stage, row):
    records.store.put(
        {"kind": "benchmark-row", "id": identifier, "ordinal": ordinal, "stage": stage}, row
    )


def _measurement(value, spec):
    if not spec.metrics:
        if type(value) not in {int, float} or not math.isfinite(value):
            raise ValueError("Evaluator must return a finite dimensionless scalar")
        return value, {}
    if type(value) is not dict or set(value) != {metric.name for metric in spec.metrics}:
        raise ValueError("Evaluator must return exactly the declared named metrics")
    measurements = {}
    for metric in spec.metrics:
        item = value[metric.name]
        if metric.unit is not None:
            scalar = quantity_value(item, field=metric.quantity_field, unit=metric.unit)
            if getattr(scalar, "ndim", 0) != 0:
                raise ValueError("Benchmark metrics must be scalar")
            scalar = float(scalar)
        else:
            if type(item) not in {int, float}:
                raise ValueError("Dimensionless metrics must be numbers")
            scalar = item
        if not math.isfinite(scalar):
            raise ValueError("Benchmark metrics must be finite")
        measurements[metric.name] = {"value": snapshot(item), "status": "available"}
    return None, measurements


def _evaluate(evaluator, case, outputs, row, context, checkpoint, spec):
    begin = perf_counter()
    row["evaluation_started"] = now()
    row["metric_status"] = "running"
    checkpoint("evaluation_started")
    error = None
    entered_evaluator = False
    phase = "recording"
    correlations = []
    recorder = context.recorder or NoRecorder()
    try:
        with recorder.operation(
            "praxis.evaluate",
            inputs={"attempt_id": row["attempt_id"]},
            implementation={"evaluator": str(case["evaluator_ref"])},
        ) as operation:
            correlation = operation.correlation()
            if correlation is not None:
                correlations.append(correlation)
            entered_evaluator = True
            phase = "evaluator"
            value = evaluator(
                snapshot(case["inputs"]),
                snapshot(outputs),
                **snapshot(spec.evaluator_configuration),
            )
            row["metric_value"], row["metrics"] = _measurement(value, spec)
            row["metric_status"] = "available"
            row["evaluation_recording_refs"] = correlations
            phase = "checkpoint"
            checkpoint("metric_computed")
            phase = "recording"
            operation.output("metric", value)
    except BaseException as caught:
        error = caught
        if phase == "recording" and isinstance(caught, RecordingError):
            row["recording_failure_type"] = type(caught).__name__
            if row["metric_status"] != "available":
                row["metric_status"] = "not_started" if not entered_evaluator else "unavailable"
        elif phase == "evaluator":
            row["evaluation_failure_type"] = type(caught).__name__
            row["failure_type"] = type(caught).__name__
            if row["metric_status"] != "available":
                row["metric_status"] = (
                    "interrupted"
                    if isinstance(caught, (KeyboardInterrupt, SystemExit))
                    else "evaluator_failed"
                )
        else:
            row["failure_type"] = type(caught).__name__
    finally:
        row["evaluation_finished"] = now()
        row["evaluation_elapsed"] = duration_record(
            perf_counter() - begin, "benchmark.evaluation_elapsed"
        )
        row["evaluation_recording_refs"] = correlations
        if context.recorder is None:
            row["evaluation_recording_status"] = "not_requested"
        else:
            try:
                row["evaluation_recording_status"] = recorder.coverage(correlations)
            except Exception as caught:
                row["evaluation_recording_status"] = "gap"
                row["recording_failure_type"] = type(caught).__name__
            if phase == "recording" and isinstance(error, RecordingError):
                row["evaluation_recording_status"] = "gap"
        try:
            checkpoint("evaluated")
        except Exception as persistence_error:
            if error is None:
                raise
            error.add_note(
                "Praxis could not persist the evaluation checkpoint: "
                + type(persistence_error).__name__
            )
    if error is not None and (
        not isinstance(error, Exception)
        or phase == "checkpoint"
        or phase == "recording"
        and not isinstance(error, RecordingError)
    ):
        raise error


def run_benchmark(spec, *, catalog, context, evaluators, identifier=None):
    """Retain planned rows and progress before executing providers or evaluators.

    Evaluators return a finite scalar or the explicitly declared named metrics.
    Checkpoints retain planned denominators; reanalysis never reruns providers.
    """
    spec = BenchmarkSpec.from_dict(spec.to_dict())
    evaluator = evaluators.get(spec.evaluator_ref)
    if evaluator is None:
        raise ValueError("The exact benchmark evaluator must be supplied explicitly")
    identifier = identifier or str(uuid4())
    schedule = [
        (case, method, replicate)
        for case in spec.cases
        for method in spec.methods
        for replicate in range(spec.replicates)
    ]
    rows = [_row(spec, *item) for item in schedule]
    initial = BenchmarkResult(
        identifier,
        spec,
        now(),
        None,
        tuple(snapshot(rows)),
        status="running",
        evaluator=callable_identity(evaluator),
        environment=environment_manifest(supplied=context.environment_metadata),
    )
    error = None
    admitted = False
    try:
        catalog.register(spec)
        context.records.store.put({"kind": "benchmark-spec", "ref": spec.ref.to_dict()}, spec)
        context.records.store.put({"kind": "benchmark-progress", "id": identifier}, initial)
        admitted = True
        for ordinal, (case, method, replicate) in enumerate(schedule):
            row = rows[ordinal]

            def checkpoint(stage):
                _checkpoint(context.records, identifier, ordinal, stage, row)

            begin = perf_counter()
            try:
                prepared = prepare(
                    MethodRequest(
                        spec.capability_ref,
                        case.inputs,
                        {
                            **method.configuration,
                            **({spec.seed_parameter: spec.seeds[replicate]} if spec.seeds else {}),
                        },
                        method.protocol_ref,
                        method.binding_ref,
                    ),
                    catalog=catalog,
                    context=context,
                )
            except BaseException as caught:
                row["method_status"] = "preparation_failed"
                row["failure_type"] = type(caught).__name__
                raise
            row["prepared_id"] = prepared.identifier
            checkpoint("prepared")
            attempt_id = str(uuid4())
            row["attempt_id"] = attempt_id
            row["method_status"] = "running"
            checkpoint("method_started")
            method_error = None
            try:
                outputs, attempt = execute(
                    prepared, catalog=catalog, context=context, identifier=attempt_id
                )
            except BaseException as caught:
                method_error = caught
                row["failure_type"] = type(caught).__name__
                outputs = None
                try:
                    attempt = context.records.attempt(attempt_id)
                except FileNotFoundError:
                    attempt = None
            row["elapsed"] = duration_record(perf_counter() - begin, "benchmark.method_elapsed")
            if attempt is not None:
                row["method_status"] = attempt.operational_status
                row["contract_status"] = attempt.contract_status
                row["method_recording_status"] = attempt.recording_status
            else:
                row["method_status"] = "incomplete"
            checkpoint("method")
            if method_error is not None and not isinstance(method_error, Exception):
                raise method_error
            if outputs is None or row["contract_status"] != "supported":
                continue
            _evaluate(
                evaluator,
                {"inputs": case.inputs, "evaluator_ref": spec.evaluator_ref},
                outputs,
                row,
                context,
                checkpoint,
                spec,
            )
    except BaseException as caught:
        error = caught
    if not admitted:
        error.add_note("Praxis benchmark: " + identifier)
        raise error
    if error is None:
        status = "completed"
    else:
        status = "interrupted" if isinstance(error, (KeyboardInterrupt, SystemExit)) else "failed"
    result = replace(initial, finished=now(), rows=tuple(snapshot(rows)), status=status)
    try:
        context.records.store.put({"kind": "benchmark-result", "id": identifier}, result)
    except Exception as persistence_error:
        if error is None:
            persistence_error.add_note("Praxis benchmark: " + identifier)
            raise
        error.add_note(
            "Praxis could not persist the terminal benchmark: " + type(persistence_error).__name__
        )
    if error is not None:
        error.add_note("Praxis benchmark: " + identifier)
        raise error
    return result


def load_benchmark(identifier, *, records):
    """Read completed or partial results, without importing provider implementations."""
    try:
        result = BenchmarkResult.from_dict(
            records.store.get({"kind": "benchmark-result", "id": identifier})
        )
    except FileNotFoundError:
        initial = BenchmarkResult.from_dict(
            records.store.get({"kind": "benchmark-progress", "id": identifier})
        )
        rows = snapshot(initial.rows)
        for ordinal, row in enumerate(rows):
            for stage in _STAGES:
                try:
                    row = records.store.get(
                        {
                            "kind": "benchmark-row",
                            "id": identifier,
                            "ordinal": ordinal,
                            "stage": stage,
                        }
                    )
                except FileNotFoundError:
                    continue
            if row["method_status"] == "running":
                try:
                    attempt = records.attempt(row["attempt_id"])
                except FileNotFoundError:
                    row["method_status"] = "incomplete"
                else:
                    row["method_status"] = attempt.operational_status
                    row["contract_status"] = attempt.contract_status
                    row["method_recording_status"] = attempt.recording_status
            if row["metric_status"] == "running":
                row["metric_status"] = "incomplete"
            if row["evaluation_started"] is not None and row["evaluation_finished"] is None:
                row["evaluation_recording_status"] = "incomplete"
            rows[ordinal] = row
        result = replace(initial, rows=tuple(rows), status="incomplete")
    for row in result.rows:
        if row["elapsed"] is not None:
            duration_seconds(row["elapsed"], "benchmark.method_elapsed")
        if row["evaluation_elapsed"] is not None:
            duration_seconds(row["evaluation_elapsed"], "benchmark.evaluation_elapsed")
    return result


def reanalyze_benchmark(source_id, spec, *, catalog, context, evaluators, identifier=None):
    """Measure retained successful outputs with another immutable evaluator specification."""
    source = load_benchmark(source_id, records=context.records)
    from ..audit import audit_benchmark

    if audit_benchmark(source_id, records=context.records).outcome == "violated":
        raise ValueError("Original benchmark evidence is inconsistent")
    spec = BenchmarkSpec.from_dict(spec.to_dict())
    if spec.ref == source.spec.ref:
        raise ValueError("Reanalysis requires a new benchmark version or identity")
    # Comparison semantics and evaluator may change; the original sample may not.
    for name in ("capability_ref", "cases", "methods", "replicates", "seeds", "seed_parameter"):
        if getattr(spec, name) != getattr(source.spec, name):
            raise ValueError("Reanalysis cannot change the original " + name)
    evaluator = evaluators.get(spec.evaluator_ref)
    if evaluator is None:
        raise ValueError("The exact reanalysis evaluator must be supplied explicitly")
    retained = []
    for row in source.rows:
        if row["contract_status"] != "supported" or row["method_status"] != "completed":
            retained.append(None)
            continue
        attempt = context.records.attempt(row["attempt_id"])
        prepared = context.records.prepared(attempt.prepared_id)
        if attempt.contract_status != "supported" or attempt.outputs is None:
            raise ValueError("Retained method outcome disagrees with benchmark sample")
        retained.append((prepared.inputs, attempt.outputs))
    identifier = identifier or str(uuid4())
    schedule = [
        (case, method, replicate)
        for case in spec.cases
        for method in spec.methods
        for replicate in range(spec.replicates)
    ]
    if len(source.rows) != len(schedule):
        raise ValueError("Reanalysis requires the full original sample schedule")
    rows = []
    for original, item in zip(source.rows, schedule, strict=True):
        row = _row(spec, *item)
        for name in (
            "attempt_id",
            "prepared_id",
            "method_status",
            "contract_status",
            "method_recording_status",
            "elapsed",
            "failure_type",
            "timing_scope",
        ):
            row[name] = original[name]
        rows.append(row)
    initial = BenchmarkResult(
        identifier,
        spec,
        now(),
        None,
        tuple(snapshot(rows)),
        status="running",
        evaluator=callable_identity(evaluator),
        environment=environment_manifest(supplied=context.environment_metadata),
        analysis_of=source_id,
    )
    catalog.register(spec)
    context.records.store.put({"kind": "benchmark-spec", "ref": spec.ref.to_dict()}, spec)
    context.records.store.put({"kind": "benchmark-progress", "id": identifier}, initial)
    error = None
    try:
        for ordinal, data in enumerate(retained):
            if data is None:
                continue
            inputs, outputs = data
            _evaluate(
                evaluator,
                {"inputs": inputs, "evaluator_ref": spec.evaluator_ref},
                outputs,
                rows[ordinal],
                context,
                lambda stage, ordinal=ordinal: _checkpoint(
                    context.records, identifier, ordinal, stage, rows[ordinal]
                ),
                spec,
            )
    except BaseException as caught:
        error = caught
    result = replace(
        initial,
        finished=now(),
        rows=tuple(snapshot(rows)),
        status="completed"
        if error is None
        else ("interrupted" if isinstance(error, (KeyboardInterrupt, SystemExit)) else "failed"),
    )
    try:
        context.records.store.put({"kind": "benchmark-result", "id": identifier}, result)
    except BaseException as persistence_error:
        if error is None:
            persistence_error.add_note("Praxis benchmark: " + identifier)
            raise
        error.add_note("Could not persist reanalysis: " + type(persistence_error).__name__)
    if error is not None:
        error.add_note("Praxis benchmark: " + identifier)
        raise error
    return result


def summarize_benchmark(result):
    """Descriptive sample statistics with explicit missing counts; no scientific ranking."""
    from statistics import mean, stdev

    summary = {
        "benchmark": result.spec.ref.to_dict(),
        "status": result.status,
        "analysis_of": result.analysis_of,
        "groups": [],
        "scope": "Arithmetic mean and sample standard deviation of retained replicates; no independence assumption, confidence interval or automatic validation",
    }
    for method in result.spec.methods:
        for case in result.spec.cases:
            rows = [
                row
                for row in result.rows
                if row["case"] == case.identifier
                and row["protocol_ref"] == method.protocol_ref.to_dict()
                and row["binding_ref"] == method.binding_ref.to_dict()
            ]
            metric_groups = []
            definitions = result.spec.metrics or (None,)
            for metric in definitions:
                values = []
                for row in rows:
                    if row["metric_status"] != "available":
                        continue
                    if metric is None:
                        values.append(row["metric_value"])
                    else:
                        item = row["metrics"][metric.name]["value"]
                        values.append(
                            float(
                                quantity_value(item, field=metric.quantity_field, unit=metric.unit)
                            )
                            if metric.unit
                            else item
                        )
                metric_groups.append(
                    {
                        "name": metric.name if metric else result.spec.metric,
                        "unit": metric.unit if metric else None,
                        "available": len(values),
                        "missing": len(rows) - len(values),
                        "mean": mean(values) if values else None,
                        "sample_standard_deviation": stdev(values) if len(values) > 1 else None,
                    }
                )
            durations = [
                duration_seconds(row["elapsed"], "benchmark.method_elapsed")
                for row in rows
                if row["elapsed"] is not None
            ]
            summary["groups"].append(
                {
                    "case": case.identifier,
                    "scenario": case.scenario,
                    "protocol_ref": method.protocol_ref.to_dict(),
                    "planned": result.spec.replicates,
                    "retained": len(rows),
                    "metrics": metric_groups,
                    "method_elapsed": {
                        "unit": "second",
                        "available": len(durations),
                        "missing": len(rows) - len(durations),
                        "mean": mean(durations) if durations else None,
                        "sample_standard_deviation": stdev(durations)
                        if len(durations) > 1
                        else None,
                        "scope": rows[0]["timing_scope"] if rows else "unavailable",
                        "warmup": "No warm-up requested or removed; provider internal caches not controlled",
                    },
                }
            )
    return snapshot(summary)
