"""Fictional paired-coordinate fixture; not a validated protein comparison engine.

All coordinates are dimensionless fixture values. Molecular correspondence,
physical quantities and structural alignment remain scientific-provider work.
"""

import argparse
import json
import math
from pathlib import Path

import praxis

CAPABILITY = praxis.MethodRef("capability", "synthetic.paired_structure_comparison", "1")
RMSD = praxis.MethodRef("protocol", "synthetic.paired_rmsd", "1")
MAXIMUM = praxis.MethodRef("protocol", "synthetic.maximum_displacement", "1")
INPUT_CHECK = praxis.MethodRef("extension", "fixture.paired_coordinates", "1", "fixture")
OUTPUT_CHECK = praxis.MethodRef("extension", "fixture.finite_score", "1", "fixture")
RMSD_BINDING = praxis.MethodRef("extension", "fixture.rmsd_recipe", "1", "fixture")
MAXIMUM_BINDING = praxis.MethodRef("extension", "fixture.maximum_recipe", "1", "fixture")


def _inputs(inputs, configuration, outputs):
    left, right = inputs.get("left"), inputs.get("right")
    if left is None or right is None:
        return praxis.CheckResult("undetermined", "Both paired coordinate sets are required")
    if type(left) is not list or type(right) is not list or not left or len(left) != len(right):
        return praxis.CheckResult("failed", "Coordinate sets must have equal positive length")
    for point in [*left, *right]:
        if (
            type(point) is not list
            or len(point) != 3
            or any(type(value) not in {int, float} or not math.isfinite(value) for value in point)
        ):
            return praxis.CheckResult(
                "failed", "Each fixture coordinate must have three finite values"
            )
    return praxis.CheckResult("passed", "Paired finite dimensionless fixture coordinates inspected")


def _outputs(inputs, configuration, outputs):
    score = outputs.get("score") if outputs else None
    if type(score) not in {int, float} or not math.isfinite(score) or score < 0:
        return praxis.CheckResult("failed", "A finite nonnegative displacement score is required")
    return praxis.CheckResult(
        "passed", "Output score inspected; scientific improvement is unassessed"
    )


def _squared_displacements(inputs):
    return [
        sum((a - b) ** 2 for a, b in zip(left, right))
        for left, right in zip(inputs["left"], inputs["right"])
    ]


def rmsd_recipe(inputs, configuration, context):
    with context.step("measure"):
        values = _squared_displacements(inputs)
        score = math.sqrt(sum(values) / len(values))
    return {"score": score, "metric": "paired_rmsd"}


def maximum_recipe(inputs, configuration, context):
    with context.step("measure"):
        score = math.sqrt(max(_squared_displacements(inputs)))
    return {"score": score, "metric": "maximum_displacement"}


def build_fixture(directory):
    directory = Path(directory)
    catalog = praxis.Catalog.open(directory / "catalog")
    capability = praxis.Capability(
        CAPABILITY,
        "Paired structure comparison fixture",
        "Quantify displacement of paired synthetic coordinate sets in one declared frame.",
        (
            praxis.Field(
                "left",
                "First coordinate set",
                "JSON array of paired triples",
                "dimensionless",
                validator="array",
            ),
            praxis.Field(
                "right",
                "Second coordinate set",
                "JSON array of paired triples",
                "dimensionless",
                validator="array",
            ),
        ),
        (
            praxis.Field(
                "score",
                "Nonnegative displacement statistic",
                "finite number",
                "dimensionless",
                validator="finite_number",
            ),
            praxis.Field(
                "metric",
                "Statistic used; raw different statistics are not interchangeable",
                "string",
                validator="string",
            ),
        ),
        requirements=(
            praxis.Requirement(
                "paired_coordinates", "Finite paired coordinates", checker_ref=INPUT_CHECK
            ),
            praxis.Requirement(
                "finite_score", "Finite nonnegative output", "post", checker_ref=OUTPUT_CHECK
            ),
        ),
        authorized_changes=("None; input coordinate sets remain unchanged",),
        limitations=(
            "Fictional fixture; no molecular correspondence, fitting or protein validation",
        ),
    )
    catalog.register(capability)
    for reference, title, basis in (
        (RMSD, "Paired RMSD", "Root mean squared paired displacement"),
        (MAXIMUM, "Maximum displacement", "Largest paired displacement"),
    ):
        protocol = praxis.Protocol(
            reference,
            title,
            basis + " without coordinate fitting.",
            CAPABILITY,
            (praxis.Step("measure", "Measure displacement", "fixture", reference.identifier),),
            scientific_basis=(basis,),
            tradeoffs=(
                praxis.Tradeoff(
                    "discouraged",
                    "Unaligned molecular structures",
                    "This fixture does not estimate structural alignment or atom mapping",
                ),
            ),
            limitations=(
                "No claim of scientific superiority; statistics measure different properties",
            ),
        )
        catalog.register(protocol)
    extensions = praxis.Extensions()
    extensions.register_checker(INPUT_CHECK, _inputs)
    extensions.register_checker(OUTPUT_CHECK, _outputs)
    extensions.register_binding(
        praxis.ImplementationBinding(
            RMSD_BINDING,
            RMSD,
            rmsd_recipe,
            "Fictional fixture implements the declared sequential measure step and output contract",
        )
    )
    extensions.register_binding(
        praxis.ImplementationBinding(
            MAXIMUM_BINDING,
            MAXIMUM,
            maximum_recipe,
            "Fictional fixture implements the declared sequential measure step and output contract",
        )
    )
    context = praxis.ExecutionContext(extensions, praxis.MethodRecords(directory / "records"))
    return catalog, context


def run(directory):
    directory = Path(directory)
    catalog, context = build_fixture(directory)
    inputs = {"left": [[0, 0, 0], [1, 0, 0]], "right": [[0, 0, 0], [1, 1, 0]]}
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING),
        catalog=catalog,
        context=context,
    )
    outputs, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    # Reopen semantic records; rendering needs no provider calls.
    reopened = praxis.MethodRecords(directory / "records")
    (directory / "execution.md").write_text(
        praxis.render(
            praxis.execution_document(reopened.attempt(attempt.identifier), records=reopened)
        ),
        encoding="utf-8",
    )
    audit = praxis.audit_execution(attempt.identifier, records=reopened)
    (directory / "audit.json").write_text(json.dumps(audit.to_dict(), indent=2), encoding="utf-8")
    for reference in (CAPABILITY, RMSD):
        (directory / f"{reference.kind}.md").write_text(
            praxis.render(praxis.describe_method(reference, catalog=catalog)), encoding="utf-8"
        )
    spec = praxis.BenchmarkSpec(
        praxis.MethodRef("benchmark", "fixture.displacement_detection", "1"),
        "Exercise independent method/evaluator records and inspectable failures",
        CAPABILITY,
        (
            praxis.BenchmarkCase(
                "unchanged", {"left": [[0, 0, 0]], "right": [[0, 0, 0]]}, "identical fixture"
            ),
            praxis.BenchmarkCase("changed", inputs, "one displaced fixture point"),
            praxis.BenchmarkCase(
                "incompatible", {"left": [[0, 0, 0]], "right": []}, "unpaired fixture"
            ),
        ),
        (
            praxis.BenchmarkMethod(RMSD, RMSD_BINDING),
            praxis.BenchmarkMethod(MAXIMUM, MAXIMUM_BINDING),
        ),
        praxis.MethodRef("extension", "fixture.displacement_detection_metric", "1", "fixture"),
        "correct displacement detection (dimensionless 0 or 1)",
        "Both statistics must detect exact equality/difference in these fixtures; raw scores are not compared",
        limitations=("Three fictional cases do not establish protein-method validation",),
    )

    def evaluate(inputs, outputs):
        return int((outputs["score"] > 0) == (inputs["left"] != inputs["right"]))

    result = praxis.run_benchmark(
        spec, catalog=catalog, context=context, evaluators={spec.evaluator_ref: evaluate}
    )
    (directory / "benchmark.md").write_text(
        praxis.render(praxis.benchmark_document(result)), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "outputs": outputs,
                "attempt": attempt.identifier,
                "benchmark": result.identifier,
                "directory": str(directory),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory for catalog, records and reports")
    run(parser.parse_args().directory)
