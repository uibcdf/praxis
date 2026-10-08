"""Real provider integration: paired C-alpha RMSD under two explicit frame conventions.

The two observables answer different questions and are never ranked as interchangeable.
MolSysMT owns parsing, correspondence selection, RMSD and optimal superposition.
"""

import argparse
import hashlib
import json
from pathlib import Path

import praxis
from praxis._quantities import quantity_record, quantity_value

CAPABILITY = praxis.MethodRef("capability", "molecular.paired_rmsd", "1")
DIRECT = praxis.MethodRef("protocol", "molecular.fixed_frame_rmsd", "1")
FITTED = praxis.MethodRef("protocol", "molecular.optimal_superposition_rmsd", "1")
INPUT_CHECK = praxis.MethodRef("extension", "molsysmt_example.correspondence", "1")
OUTPUT_CHECK = praxis.MethodRef("extension", "molsysmt_example.rmsd_output", "1")
REFERENCE_CHECK = praxis.MethodRef("extension", "molsysmt_example.source_available", "1")


def binding_ref(protocol):
    return praxis.MethodRef("extension", protocol.identifier + ".molsysmt", "1")


def _inputs(inputs, configuration, outputs):
    import numpy as np

    left = np.asarray(quantity_value(inputs["left"], field="comparison.left", unit="nanometer"))
    right = np.asarray(quantity_value(inputs["right"], field="comparison.right", unit="nanometer"))
    indices = inputs["source"]["atom_indices"]
    passed = (
        left.shape == right.shape == (1, len(indices), 3)
        and len(indices) >= 3
        and len(set(indices)) == len(indices)
    )
    return praxis.CheckResult(
        "passed" if passed else "failed",
        "Single-frame paired finite coordinates and retained C-alpha correspondence checked",
    )


def _source(inputs, configuration, outputs):
    document = inputs["source"]
    try:
        actual = hashlib.sha256(Path(document["path"]).read_bytes()).hexdigest()
    except (FileNotFoundError, PermissionError):
        return praxis.CheckResult(
            "undetermined", "The retained source cannot currently be inspected"
        )
    return praxis.CheckResult(
        "passed" if actual == document["sha256"] else "failed",
        "Local PDB content digest checked; file ownership is unchanged",
    )


def _outputs(inputs, configuration, outputs):
    value = float(quantity_value(outputs["rmsd"], field="comparison.rmsd", unit="nanometer"))
    return praxis.CheckResult(
        "passed"
        if value >= 0 and outputs["convention"] in {"fixed_frame", "optimal_superposition"}
        else "failed",
        "Nonnegative physical RMSD and explicit frame convention; scientific usefulness unassessed",
    )


def direct_recipe(inputs, configuration, context):
    import molsysmt as msm
    import pyunitwizard as puw

    left = puw.QuantityRecord.from_dict(inputs["left"]).to_quantity(
        field="comparison.left", unit="nanometer", form="pint"
    )
    right = puw.QuantityRecord.from_dict(inputs["right"]).to_quantity(
        field="comparison.right", unit="nanometer", form="pint"
    )
    with context.step("measure"):
        result = msm.structure.get_rmsd(
            left,
            reference_molecular_system=right,
            engine="MolSysMT",
            use_gpu=False,
            parallel=False,
            num_threads=1,
        )
    return {
        "rmsd": quantity_record(result[0], field="comparison.rmsd", unit="nanometer"),
        "convention": "fixed_frame",
        "provider_version": msm.__version__,
    }


def fitted_recipe(inputs, configuration, context):
    import molsysmt as msm
    import pyunitwizard as puw

    left = puw.QuantityRecord.from_dict(inputs["left"]).to_quantity(
        field="comparison.left", unit="nanometer", form="pint"
    )
    right = puw.QuantityRecord.from_dict(inputs["right"]).to_quantity(
        field="comparison.right", unit="nanometer", form="pint"
    )
    with context.step("measure"):
        result = msm.structure.get_least_rmsd(
            left,
            reference_molecular_system=right,
            engine="MolSysMT",
            use_gpu=False,
            parallel=False,
            num_threads=1,
        )
    return {
        "rmsd": quantity_record(result[0], field="comparison.rmsd", unit="nanometer"),
        "convention": "optimal_superposition",
        "provider_version": msm.__version__,
    }


def build(directory, pdb_path):
    import molsysmt as msm
    import pyunitwizard as puw

    pdb_path = Path(pdb_path).resolve()
    selection = 'atom_name=="CA"'
    coordinates = msm.get(str(pdb_path), selection=selection, structure_indices=0, coordinates=True)
    indices = list(msm.select(str(pdb_path), selection=selection))
    source = {
        "owner": "molsysmt-example",
        "path": str(pdb_path),
        "sha256": hashlib.sha256(pdb_path.read_bytes()).hexdigest(),
        "atom_indices": indices,
        "selection": selection,
        "provider_version": msm.__version__,
    }
    left = quantity_record(coordinates, field="comparison.left", unit="nanometer")
    right = quantity_record(coordinates, field="comparison.right", unit="nanometer")
    moved = coordinates + puw.quantity([1.0, 0, 0], "nanometer", form="pint")
    translated = quantity_record(moved, field="comparison.right", unit="nanometer")
    catalog = praxis.Catalog.open(Path(directory) / "catalog")
    capability = praxis.Capability(
        CAPABILITY,
        "Paired molecular RMSD",
        "Measure RMS displacement of explicitly corresponding atoms under the reported coordinate convention.",
        (
            praxis.Field(
                "left",
                "Query single-frame coordinates",
                "Shared QuantityRecord",
                "nanometer",
                validator="quantity",
                quantity_field="comparison.left",
            ),
            praxis.Field(
                "right",
                "Reference single-frame coordinates",
                "Shared QuantityRecord",
                "nanometer",
                validator="quantity",
                quantity_field="comparison.right",
            ),
            praxis.Field(
                "source",
                "Retained source and ordered atom correspondence",
                "JSON object",
                validator="object",
            ),
        ),
        (
            praxis.Field(
                "rmsd",
                "Paired RMS displacement",
                "Shared QuantityRecord",
                "nanometer",
                validator="quantity",
                quantity_field="comparison.rmsd",
            ),
            praxis.Field("convention", "Coordinate convention used", "string", validator="string"),
            praxis.Field(
                "provider_version",
                "Actual scientific provider revision",
                "string",
                validator="string",
            ),
        ),
        requirements=(
            praxis.Requirement(
                "paired_coordinates",
                "Single-frame coordinates with explicit correspondence",
                checker_ref=INPUT_CHECK,
            ),
            praxis.Requirement(
                "rmsd_contract",
                "Nonnegative physical RMSD with declared convention",
                "post",
                checker_ref=OUTPUT_CHECK,
            ),
        ),
        authorized_changes=("None; providers receive decoded copies of retained inputs",),
        limitations=(
            "Fixed-frame and fitted RMSD answer different questions; values alone do not rank protocols or validate a protein model",
        ),
    )
    catalog.register(capability)
    extensions = praxis.Extensions()
    for ref, checker in (
        (INPUT_CHECK, _inputs),
        (OUTPUT_CHECK, _outputs),
        (REFERENCE_CHECK, _source),
    ):
        extensions.register_checker(ref, checker)
    for ref, recipe, convention, operation in (
        (DIRECT, direct_recipe, "fixed_frame", "molsysmt.structure.get_rmsd"),
        (FITTED, fitted_recipe, "optimal_superposition", "molsysmt.structure.get_least_rmsd"),
    ):
        protocol = praxis.Protocol(
            ref,
            convention + " RMSD",
            "Invoke the declared public MolSysMT operation with CPU, one thread, no GPU; retain physical result and convention.",
            CAPABILITY,
            (praxis.Step("measure", "Measure paired molecular RMSD", "molsysmt", operation),),
            scientific_basis=(operation,),
            provenance_requirements=("source.available",),
            provenance_checks=(
                praxis.Requirement(
                    "source.available",
                    "Original local PDB reference and digest remain available",
                    checker_ref=REFERENCE_CHECK,
                ),
            ),
            resources=praxis.ResourceProfile("declared_coordinate_convention", "unknown", ("CPU",)),
            tradeoffs=(
                praxis.Tradeoff(
                    "favorable",
                    "A shared frame is meaningful"
                    if ref == DIRECT
                    else "Rigid translation/rotation is irrelevant to the question",
                    "This convention corresponds to the stated comparison goal",
                    basis="proposed",
                    alternative=FITTED if ref == DIRECT else DIRECT,
                ),
            ),
        )
        catalog.register(protocol)
        extensions.register_binding(
            praxis.ImplementationBinding(
                binding_ref(ref),
                ref,
                recipe,
                "Real public provider operation; one frame, explicit ordered CA correspondence and unit roundtrip",
                dependencies=("molsysmt",),
            )
        )
    context = praxis.ExecutionContext(
        extensions,
        praxis.MethodRecords(Path(directory) / "records"),
        environment_metadata={"scientific_provider": {"molsysmt": msm.__version__}},
    )
    return catalog, context, {"left": left, "right": right, "source": source}, translated


def evaluate(inputs, outputs):
    return {"rmsd": outputs["rmsd"], "matched_atoms": len(inputs["source"]["atom_indices"])}


def run(directory, pdb_path):
    import pyunitwizard as puw

    directory = Path(directory)
    catalog, context, inputs, translated = build(directory, pdb_path)
    spec = praxis.BenchmarkSpec(
        praxis.MethodRef("benchmark", "molecular.rmsd_provider_acceptance", "1"),
        "Exercise real public provider APIs and physical result retention",
        CAPABILITY,
        (
            praxis.BenchmarkCase("identical", inputs, "same local PDB coordinates"),
            praxis.BenchmarkCase(
                "translated",
                {**inputs, "right": translated},
                "Controlled rigid translation by 1 nm along x",
            ),
            praxis.BenchmarkCase(
                "incompatible",
                {
                    **inputs,
                    "right": quantity_record(
                        puw.QuantityRecord.from_dict(inputs["right"]).to_quantity(
                            field="comparison.right", unit="nanometer", form="pint"
                        ),
                        field="wrong.semantic.field",
                        unit="nanometer",
                    ),
                },
                "Unverified semantic quantity field",
            ),
        ),
        tuple(praxis.BenchmarkMethod(ref, binding_ref(ref)) for ref in (DIRECT, FITTED)),
        praxis.MethodRef("extension", "molsysmt_example.physical_metrics", "1"),
        "Physical RMSD and correspondence size",
        "Compare each convention against its own controlled expectation; do not rank raw observables across conventions",
        metrics=(
            praxis.MetricDefinition(
                "rmsd", "Declared-convention RMSD", "nanometer", "comparison.rmsd"
            ),
            praxis.MetricDefinition("matched_atoms", "Number of explicitly paired C-alpha atoms"),
        ),
        limitations=(
            "One protein and controlled translations test integration; no general scientific validation",
        ),
    )
    result = praxis.run_benchmark(
        spec, catalog=catalog, context=context, evaluators={spec.evaluator_ref: evaluate}
    )
    for name, document in (
        ("benchmark", praxis.benchmark_document(result)),
        (
            "audit",
            praxis.audit_document(
                praxis.audit_benchmark(result.identifier, records=context.records)
            ),
        ),
        ("capability", praxis.describe_method(CAPABILITY, catalog=catalog)),
        (
            "comparison",
            praxis.comparison_document(
                (DIRECT, FITTED), catalog=catalog, scenario={"goal": "rigid_motion_invariant"}
            ),
        ),
    ):
        (directory / (name + ".md")).write_text(praxis.render(document), encoding="utf-8")
    (directory / "summary.json").write_text(
        json.dumps(praxis.summarize_benchmark(result), indent=2), encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("pdb", type=Path)
    args = parser.parse_args()
    result = run(args.directory, args.pdb)
    print(
        json.dumps(
            {
                "benchmark": result.identifier,
                "rows": len(result.rows),
                "available": sum(row["metric_status"] == "available" for row in result.rows),
            },
            indent=2,
        )
    )
