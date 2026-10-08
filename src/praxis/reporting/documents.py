"""Derived documents retain source snapshots and honest limitations."""

from dataclasses import dataclass

from .._quantities import duration_seconds
from .._serialization import Model, encode
from ..benchmarks import BenchmarkResult, summarize_benchmark
from ..definitions import Capability, Protocol
from ..execution.reports import AttemptRecord
from ..execution.runner import now


@dataclass(frozen=True)
class Document(Model):
    schema = "praxis.document/0.1"
    title: str
    generated: str
    source: dict[str, object]
    paragraphs: tuple[str, ...]
    columns: tuple[str, ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()
    disclosure_scope: str = "all supplied content; caller controls sharing"


def describe_method(reference, *, catalog):
    definition = catalog.get(reference)
    if not isinstance(definition, (Capability, Protocol)):
        raise TypeError("Method documentation requires a Capability or Protocol")
    paragraphs = [
        f"Exact method: {definition.ref}",
        "Projected catalog status: " + encode(catalog.status_for(reference)),
    ]
    source = definition.to_dict()
    if isinstance(definition, Capability):
        paragraphs.append(definition.intent)
        columns = ("Protocol", "Status", "Pending")
        rows = tuple(
            (str(item.ref), item.status, "; ".join(item.pending))
            for item in catalog.protocols_for(reference)
        )
    elif isinstance(definition, Protocol):
        paragraphs.extend((f"Capability: {definition.capability_ref}", definition.procedure))
        if definition.capability_ref is not None:
            capability = catalog.get(definition.capability_ref)
            source = {"protocol": source, "capability": capability.to_dict()}
            paragraphs.append("Common contract: " + capability.intent)
            for direction, fields in (("Input", capability.inputs), ("Output", capability.outputs)):
                paragraphs.extend(
                    f"Common {direction} {item.name}: {item.meaning}; unit: {item.unit}; validator: {item.validator}; checker: {item.checker_ref}"
                    for item in fields
                )
            paragraphs.extend(
                "Common authorized change: " + item for item in capability.authorized_changes
            )
            paragraphs.extend(
                f"Common requirement {item.identifier} ({item.phase}; coverage: {item.coverage_required}): {item.description}"
                for item in capability.requirements
            )
        paragraphs.extend("Scientific basis: " + item for item in definition.scientific_basis)
        paragraphs.extend("Pending: " + item for item in definition.pending)
        paragraphs.extend(
            f"{item.kind} ({item.basis}; {item.conditions}): {item.statement}"
            + ("; support: " + "; ".join(item.support) if item.support else "")
            + ("; alternative: " + str(item.alternative) if item.alternative else "")
            for item in definition.tradeoffs
        )
        if definition.resources is not None:
            paragraphs.append("Resource/fidelity profile: " + encode(definition.resources))
        columns = ("Step", "Provider", "Operation", "Pending")
        rows = tuple(
            (item.identifier, item.provider, item.operation, "; ".join(item.pending))
            for item in definition.steps
        )
    else:
        raise TypeError("Method documentation requires a Capability or Protocol")
    paragraphs.extend("Limitation: " + item for item in definition.limitations)
    if isinstance(definition, Capability):
        for direction, fields in (("Input", definition.inputs), ("Output", definition.outputs)):
            paragraphs.extend(
                f"{direction} {item.name}: {item.meaning}; representation: {item.representation}; "
                f"unit: {item.unit or 'not specified'}; required: {item.required}; "
                f"validator: {item.validator or 'unresolved'}; field checker: {item.checker_ref or 'none'}"
                for item in fields
            )
        paragraphs.extend("Authorized change: " + item for item in definition.authorized_changes)
        paragraphs.extend("Scientific reference: " + item for item in definition.references)
    else:
        paragraphs.extend(
            f"Parameter {item.name}: {item.description}; required: {item.required}; "
            + ("no default" if item.required else "default: " + encode(item.default))
            + f"; validator: {item.validator}; unit: {item.unit}; semantic field: {item.quantity_field}; bounds: {item.minimum}..{item.maximum}; choices: {encode(item.choices)}; checker: {item.checker_ref}"
            for item in definition.parameters
        )
        paragraphs.extend(
            "Required provenance: " + item for item in definition.provenance_requirements
        )
    requirements = (
        definition.requirements
        if isinstance(definition, Capability)
        else (*definition.requirements, *definition.provenance_checks)
    )
    paragraphs.extend(
        f"Requirement {item.identifier} ({item.phase}; mandatory: {item.mandatory}): "
        f"{item.description}; checker: {item.checker_ref or 'unresolved'}"
        for item in requirements
    )
    paragraphs.extend(
        f"Assessment {item.ref}: {item.outcome}; scope: {item.scope}; actor: {item.actor}; "
        + "; ".join(item.findings)
        for item in catalog.assessments_for(reference)
    )
    paragraphs.extend(
        "Admission review: " + encode(item) for item in catalog.reviews_for(reference)
    )
    paragraphs.extend(
        "Scenario suitability: " + encode(item) for item in catalog.suitability_for(reference)
    )
    paragraphs.append(
        "Registration and successful execution do not establish scientific validation."
    )
    return Document(definition.title, now(), source, tuple(paragraphs), columns, rows)


def execution_document(attempt, *, records=None):
    if not isinstance(attempt, AttemptRecord):
        raise TypeError("Expected an AttemptRecord")
    paragraphs = [
        f"Attempt: {attempt.identifier}",
        f"Prepared intent: {attempt.prepared_id}",
        f"Operational outcome: {attempt.operational_status}",
        f"Contract outcome: {attempt.contract_status}",
        f"Operation recording: {attempt.recording_status}",
        f"Started: {attempt.started}; finished: {attempt.finished}",
        f"Actor: {attempt.actor}; authority: {attempt.authority}",
        "Actual environment: " + encode(attempt.environment),
    ]
    if attempt.failure_type:
        paragraphs.append("Failure type: " + attempt.failure_type)
    paragraphs.extend(attempt.limitations)
    paragraphs.extend(
        f"Step {item['identifier']}: {item['status']}; provider: {item['provider']}; "
        f"started: {item['started']}; finished: {item['finished']}"
        for item in attempt.steps
    )
    paragraphs.append("Retained outputs: " + encode(attempt.outputs))
    source = attempt.to_dict()
    if records is not None:
        prepared = records.prepared(attempt.prepared_id)
        paragraphs.extend(
            (
                f"Capability: {prepared.capability_ref}",
                f"Protocol: {prepared.selection.protocol_ref}",
                f"Binding: {prepared.selection.binding_ref}",
                "Resolved configuration: " + encode(prepared.configuration),
                "Retained inputs: " + encode(prepared.inputs),
            )
        )
        source = {"attempt": source, "prepared": prepared.to_dict()}
    rows = tuple(
        (item.phase, item.requirement, item.outcome, item.reason) for item in attempt.findings
    )
    if attempt.attribution is not None:
        # Render preserved portable bibliography without importing or crediting work.
        paragraphs.extend(
            "Bibliography: " + item.get("title", item["id"])
            for item in attempt.attribution.get("items", [])
        )
    return Document(
        "Method execution",
        now(),
        source,
        tuple(paragraphs),
        ("Phase", "Requirement", "Outcome", "Reason"),
        rows,
    )


def benchmark_document(result):
    if not isinstance(result, BenchmarkResult):
        raise TypeError("Expected a BenchmarkResult")
    available = sum(row["metric_status"] == "available" for row in result.rows)
    paragraphs = (
        result.spec.purpose,
        f"Exact benchmark: {result.spec.ref}",
        f"Benchmark status: {result.status}",
        "Comparison basis: " + result.spec.comparison_basis,
        "Evaluator implementation: " + encode(result.evaluator),
        "Evaluator configuration: " + encode(result.spec.evaluator_configuration),
        "Evaluator environment: " + encode(result.environment),
        "Analysis of: " + str(result.analysis_of),
        "Replicate seed controls: "
        + encode({"parameter": result.spec.seed_parameter, "seeds": result.spec.seeds}),
        "Descriptive statistics: " + encode(summarize_benchmark(result)),
        f"Available measurements: {available}/{len(result.rows)} scheduled invocations",
        "Failed, blocked and unmeasured invocations remain in the denominator.",
        "No aggregate ranking or automatic scientific validation is inferred.",
        *result.spec.limitations,
    )
    rows = tuple(
        (
            row["case"],
            str(row["replicate"]),
            row["protocol_ref"]["identifier"] + "@" + row["protocol_ref"]["version"],
            row["method_status"],
            row["contract_status"],
            row["metric_status"],
            row.get("evaluation_recording_status", "unknown"),
            encode(row.get("metrics", {})) if result.spec.metrics else str(row["metric_value"]),
            str(duration_seconds(row["elapsed"], "benchmark.method_elapsed"))
            if row["elapsed"] is not None
            else "Unavailable",
        )
        for row in result.rows
    )
    return Document(
        "Method benchmark",
        now(),
        result.to_dict(),
        paragraphs,
        (
            "Case",
            "Replicate",
            "Protocol",
            "Method",
            "Contract",
            "Metric status",
            "Metric recording",
            result.spec.metric,
            "Elapsed seconds",
        ),
        rows,
    )


def audit_document(audit):
    from ..audit import AuditReport

    if not isinstance(audit, AuditReport):
        raise TypeError("Expected an AuditReport")
    return Document(
        "Methodological audit",
        now(),
        audit.to_dict(),
        ("Audit outcome: " + audit.outcome, *audit.findings, *audit.limitations),
        ("Issue", "Severity", "Finding"),
        tuple((item.code, item.severity, item.message) for item in audit.issues),
    )


def comparison_document(references, *, catalog, scenario):
    """Compare recorded judgments for an exact scenario; never infer a universal winner."""
    references = tuple(references)
    definitions = tuple(catalog.get(ref) for ref in references)
    if not definitions or any(not isinstance(item, Protocol) for item in definitions):
        raise TypeError("Comparison requires Protocol definitions")
    if len({item.capability_ref for item in definitions}) != 1:
        raise ValueError("Comparisons require one common Capability contract")
    rows = []
    sources = []
    for definition in definitions:
        state = catalog.status_for(definition.ref, scenario=scenario)
        statements = catalog.suitability_for(definition.ref, scenario=scenario)
        assessments = catalog.assessments_for(definition.ref, scenario=scenario)
        sources.append(
            {
                "definition": definition.to_dict(),
                "status": state,
                "suitability": [item.to_dict() for item in statements],
                "assessments": [item.to_dict() for item in assessments],
            }
        )
        rows.append(
            (
                str(definition.ref),
                state["maturity"],
                state["validation"],
                state["suitability"],
                definition.resources.fidelity
                if definition.resources and definition.resources.fidelity
                else "unknown",
                definition.resources.cost_class
                if definition.resources and definition.resources.cost_class
                else "unknown",
                (
                    str(
                        duration_seconds(
                            definition.resources.expected_duration, "protocol.expected_duration"
                        )
                    )
                    + " ("
                    + definition.resources.basis
                    + ")"
                )
                if definition.resources
                and definition.resources.expected_duration
                and definition.resources.conditions == scenario
                else "Unknown for this scenario",
                "; ".join(
                    item.outcome
                    + " ("
                    + item.basis
                    + "; criteria: "
                    + ", ".join(item.criteria)
                    + "): "
                    + item.rationale
                    + " ["
                    + str(item.ref)
                    + "]; support: "
                    + ", ".join(item.supporting_refs)
                    + ("; alternative: " + str(item.alternative) if item.alternative else "")
                    for item in statements
                )
                or "Unknown",
            )
        )
    return Document(
        "Scenario-specific Protocol comparison",
        now(),
        {"scenario": scenario, "methods": sources},
        (
            "Common Capability: " + str(definitions[0].capability_ref),
            "Exact scenario: " + encode(scenario),
            "Applicability and implementation availability still require an invocation check.",
            "Conflicting, proposed and missing evidence are retained; no universal ranking is inferred.",
        ),
        (
            "Protocol",
            "Maturity",
            "Assessment",
            "Suitability",
            "Fidelity",
            "Cost",
            "Expected seconds",
            "Recorded history/basis",
        ),
        tuple(rows),
    )
