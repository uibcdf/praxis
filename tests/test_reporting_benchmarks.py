import subprocess
import sys

import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING

import praxis


def spec(inputs):
    return praxis.BenchmarkSpec(
        praxis.MethodRef("benchmark", "test", "1"),
        "Fictional fixture",
        CAPABILITY,
        (
            praxis.BenchmarkCase("valid", inputs, "paired"),
            praxis.BenchmarkCase("invalid", {"left": [[0, 0, 0]], "right": []}, "unpaired"),
        ),
        (praxis.BenchmarkMethod(RMSD, RMSD_BINDING),),
        praxis.MethodRef("extension", "fixture.metric", "1"),
        "dimensionless score",
        "One declared statistic",
        replicates=2,
    )


def test_benchmark_keeps_failed_cases_and_reopens_without_evaluator(workspace, inputs):
    catalog, context = workspace
    specification = spec(inputs)
    calls = []

    def evaluator(inputs, outputs):
        calls.append(1)
        return outputs["score"]

    result = praxis.run_benchmark(
        specification,
        catalog=catalog,
        context=context,
        evaluators={specification.evaluator_ref: evaluator},
    )
    assert len(result.rows) == 4 and len(calls) == 2
    assert sum(row["method_status"] == "blocked" for row in result.rows) == 2
    assert result == praxis.load_benchmark(result.identifier, records=context.records)
    report = praxis.render(praxis.benchmark_document(result))
    assert "2/4" in report and "blocked" in report
    assert len(calls) == 2
    assert catalog.assessments_for(RMSD) == ()


def test_evaluator_failure_does_not_become_zero_score_or_method_failure(workspace, inputs):
    catalog, context = workspace
    specification = spec(inputs)

    def fails(inputs, outputs):
        raise ValueError("metric unavailable")

    result = praxis.run_benchmark(
        specification,
        catalog=catalog,
        context=context,
        evaluators={specification.evaluator_ref: fails},
    )
    assert result.rows[0]["method_status"] == "completed"
    assert result.rows[0]["metric_status"] == "evaluator_failed"
    assert result.rows[0]["metric_value"] is None


def test_reports_render_html_safely(workspace):
    from dataclasses import replace

    catalog, context = workspace
    document = praxis.describe_method(RMSD, catalog=catalog)
    document = replace(document, title="<script>alert(1)</script>", paragraphs=("a|b\nc",))
    assert "<script>" not in praxis.render(document, format="html")
    assert "&lt;script&gt;" in praxis.render(document, format="html")
    assert "a\\|b<br>c" in praxis.render(document)
    with pytest.raises(ValueError):
        praxis.render(document, format="unsupported")


def test_reopen_attempt_and_render_in_fresh_process_without_provider(workspace, prepared, tmp_path):
    catalog, context = workspace
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    code = """import sys, praxis
r = praxis.MethodRecords(sys.argv[1]); a = r.attempt(sys.argv[2])
assert a.operational_status == "completed"
assert "Contract outcome: supported" in praxis.render(praxis.execution_document(a))
assert "local_comparison" not in sys.modules and "ackredit" not in sys.modules and "recorda" not in sys.modules
"""
    subprocess.run(
        [sys.executable, "-B", "-c", code, str(tmp_path / "records"), attempt.identifier],
        check=True,
    )
