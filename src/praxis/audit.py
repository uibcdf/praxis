"""Audit preserved evidence against frozen definitions, without calling providers."""

from dataclasses import dataclass

from ._field_checks import field_id, parameter_id, parameter_structural, structural_field
from ._serialization import Model
from .definitions import Capability, Parameter, Protocol


@dataclass(frozen=True)
class AuditIssue(Model):
    schema = "praxis.audit-issue/0.1"
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class AuditReport(Model):
    schema = "praxis.audit/0.1"
    attempt_id: str
    findings: tuple[str, ...]
    limitations: tuple[str, ...]
    outcome: str = "unverified"
    issues: tuple[AuditIssue, ...] = ()


def audit_execution(identifier, *, records, _visited=()):
    if identifier in _visited:
        return AuditReport(
            identifier,
            ("Cyclic child attempt relationship",),
            (),
            "violated",
            (AuditIssue("child_cycle", "violated", "Cyclic attempt references"),),
        )
    _visited = (*_visited, identifier)
    attempt = records.attempt(identifier)
    prepared = records.prepared(attempt.prepared_id)
    findings = [
        f"Operational outcome: {attempt.operational_status}",
        f"Contract outcome: {attempt.contract_status}",
        f"Operation recording: {attempt.recording_status}",
    ]
    issues = []

    def issue(code, message, severity="violated"):
        issues.append(AuditIssue(code, severity, message))

    complete = attempt.operational_status == "completed"
    supported = attempt.contract_status == "supported"
    if attempt.finished is None:
        findings.append("No retained terminal record; cause and final outcome remain unknown")
        issue("terminal_missing", findings[-1], "unverified")
    if not prepared.ready:
        findings.extend(prepared.reasons)
        if complete or supported:
            issue("not_ready", "A rejected preparation cannot support completed execution")
    try:
        capability = Capability.from_dict(prepared.definitions[0])
        protocol = Protocol.from_dict(prepared.definitions[1])
    except (ValueError, IndexError, TypeError, KeyError):
        issue(
            "definitions_missing",
            "Frozen Capability/Protocol definitions are unavailable",
            "violated" if complete or supported else "unverified",
        )
    else:
        if (
            capability.ref != prepared.capability_ref
            or protocol.capability_ref != capability.ref
            or protocol.ref != prepared.selection.protocol_ref
        ):
            issue("association_mismatch", "Frozen definitions disagree with the selected method")
        if (
            prepared.binding is None
            or prepared.selection.binding_ref is None
            or prepared.binding.get("ref") != prepared.selection.binding_ref.to_dict()
            or prepared.binding.get("protocol_ref") != protocol.ref.to_dict()
        ):
            issue(
                "binding_mismatch",
                "Frozen binding disagrees with the selected Protocol",
                "violated" if complete or supported else "unverified",
            )
        expected_implementations = (prepared.binding, *prepared.checkers)
        if complete or supported:
            if attempt.implementations != expected_implementations:
                issue(
                    "implementation_evidence",
                    "Consumed implementation identities are absent or differ",
                )
            if protocol.pending or any(step.pending for step in protocol.steps):
                issue(
                    "pending_protocol", "An unresolved procedure cannot support completed execution"
                )
        if complete or supported:
            schedule = [
                (step, iteration) for step in protocol.steps for iteration in range(step.repeat)
            ]
            expected_steps = [
                (step.identifier, step.provider, step.operation, iteration)
                for step, iteration in schedule
            ]
            actual_steps = [
                (
                    step.get("identifier"),
                    step.get("provider"),
                    step.get("operation"),
                    step.get("iteration", 0),
                )
                for step in attempt.steps
            ]
            if actual_steps != expected_steps or any(
                not step.get("started") or not step.get("finished") for step in attempt.steps
            ):
                issue(
                    "step_coverage", "Completed execution lacks the declared ordered step evidence"
                )
            for ordinal, (definition, iteration) in enumerate(schedule):
                if ordinal >= len(attempt.steps):
                    continue
                step = attempt.steps[ordinal]
                branch = [item for item in attempt.branches if item.get("ordinal") == ordinal]
                if definition.condition_ref is not None:
                    valid = (
                        len(branch) == 1
                        and branch[0].get("checker_ref") == definition.condition_ref.to_dict()
                        and branch[0].get("iteration") == iteration
                        and branch[0].get("finding", {}).get("outcome")
                        == ("failed" if step["status"] == "skipped" else "passed")
                    )
                    if not valid:
                        issue(
                            "branch_evidence",
                            "Conditional boundary has no matching retained decision",
                        )
                elif step["status"] == "skipped" or branch:
                    issue(
                        "branch_evidence",
                        "An unconditional boundary was skipped or given an undeclared branch",
                    )
                if step["status"] not in {"completed", "skipped"}:
                    issue("step_coverage", "A declared step did not complete")
        requirements = {
            (item.phase, item.identifier): item
            for item in (
                *capability.requirements,
                *protocol.requirements,
                *protocol.provenance_checks,
            )
        }
        expected = {}
        for requirement in (
            *capability.requirements,
            *protocol.requirements,
            *protocol.provenance_checks,
        ):
            expected[(requirement.phase, requirement.identifier)] = (
                requirement.mandatory,
                requirement.checker_ref,
                None,
            )
        for phase, fields, values in (
            ("pre", capability.inputs, prepared.inputs),
            ("post", capability.outputs, attempt.outputs or {}),
        ):
            for field in fields:
                expected[(phase, field_id(field, phase))] = (
                    field.required or field.name in values,
                    field.checker_ref,
                    field,
                )
        for parameter in protocol.parameters:
            expected[("pre", parameter_id(parameter))] = (
                parameter.required or parameter.name in prepared.configuration,
                parameter.checker_ref,
                parameter,
            )
        observed = {}
        for check in attempt.findings:
            findings.append(f"{check.phase}/{check.requirement}: {check.outcome}; {check.reason}")
            key = (check.phase, check.requirement)
            if key in observed:
                issue("duplicate_check", "More than one finding claims the same guarantee")
            observed[key] = check
            if key not in expected:
                issue("unexpected_check", "A finding has no matching frozen contract guarantee")
                continue
            mandatory, checker_ref, field = expected[key]
            values = (
                prepared.configuration
                if isinstance(field, Parameter)
                else prepared.inputs
                if check.phase == "pre"
                else attempt.outputs or {}
            )
            structural = (
                parameter_structural(field, values)
                if isinstance(field, Parameter)
                else structural_field(field, check.phase, values)
                if field
                else None
            )
            # Missing/structurally invalid fields never invoke their custom checker.
            expected_checker = (
                None
                if structural and (field.name not in values or structural.outcome == "failed")
                else checker_ref
            )
            if check.mandatory != mandatory or check.checker_ref != expected_checker:
                issue(
                    "check_identity",
                    "Finding necessity or checker identity contradicts its definition",
                )
            if structural is not None:
                if (
                    expected_checker is None
                    and check.outcome != structural.outcome
                    or structural.outcome == "failed"
                    and check.outcome != "failed"
                ):
                    issue(
                        "field_evidence", "Retained field value contradicts its claimed guarantee"
                    )
            requirement = requirements.get(key)
            if requirement is not None:
                from .applicability import evidence_problem
                from .provenance import invocation_digest

                problem = evidence_problem(
                    requirement,
                    check,
                    invocation_digest(
                        capability.ref, protocol.ref, prepared.inputs, prepared.configuration
                    ),
                    attempt_id=attempt.identifier,
                    steps=tuple(item.identifier for item in protocol.steps),
                )
                if problem:
                    issue("scoped_evidence", problem)
            if (
                check.outcome == "passed"
                and field is None
                and expected_checker is None
                and not (
                    requirement is not None
                    and requirement.review_required
                    and check.evidence_records
                )
            ):
                issue(
                    "checker_evidence",
                    "A descriptive requirement cannot establish a passed guarantee",
                )
            if check.outcome == "passed" and expected_checker is not None:
                pinned = next(
                    (
                        item
                        for item in prepared.checkers
                        if item["ref"] == expected_checker.to_dict()
                    ),
                    None,
                )
                if pinned is None or pinned.get("implementation") is None:
                    issue(
                        "checker_evidence", "Passed check has no pinned executable checker evidence"
                    )
        phases = {"pre", "runtime", "post"} if complete or supported else set()
        for key, (mandatory, _, _) in expected.items():
            if key[0] not in phases:
                continue
            check = observed.get(key)
            if check is None:
                issue(
                    "check_coverage",
                    "Terminal method conclusion lacks a declared guarantee finding",
                )
            elif mandatory and check.outcome != "passed":
                if supported:
                    issue("unsupported_claim", "Supported contract contradicts a mandatory finding")
                elif check.outcome not in {"failed"}:
                    issue(
                        "unresolved_check", "A mandatory guarantee remains unresolved", "unverified"
                    )
        if (complete or supported) and attempt.outputs is None:
            issue("outputs_missing", "Completed execution has no retained output object")
        if complete and all(key in observed for key in expected):
            all_passed = all(
                observed[key].outcome == "passed"
                for key, (mandatory, _, _) in expected.items()
                if mandatory
            )
            inferred = "supported" if all_passed else "unsupported"
            if attempt.contract_status != inferred:
                issue(
                    "conclusion_mismatch",
                    "Contract outcome contradicts the retained guarantee findings",
                )
    for child_id in attempt.child_ids:
        try:
            child = records.attempt(child_id)
        except FileNotFoundError:
            issue("child_missing", "Child attempt reference is unavailable", "unverified")
            continue
        if child.parent_id != identifier:
            issue("child_parent", "Child record identifies a different parent")
        if supported and child.contract_status != "supported":
            issue("child_contract", "Supported parent depends on an unsupported child")
        child_audit = audit_execution(child_id, records=records, _visited=_visited)
        issues.extend(child_audit.issues)
    if attempt.operational_status == "waiting":
        issue("human_pending", "Declared human gate remains pending", "unverified")
    if attempt.recording_status in {"gap", "incomplete", "pending"}:
        issue("recording_gap", "Declared operation recording remains incomplete", "unverified")
    outcome = (
        "violated"
        if any(item.severity == "violated" for item in issues)
        else ("unverified" if issues else "consistent")
    )
    findings.extend(item.message for item in issues)
    limitations = (
        "Consistency applies only to retained definitions, explicit checks and declared boundaries",
        "Local snapshot digests check content consistency, not authenticity",
        "Provider internal invariants are not established by boundary recording",
        "No scientific validation, reference availability check or replay is implied",
    )
    return AuditReport(identifier, tuple(findings), limitations, outcome, tuple(issues))


def audit_definition(reference, *, catalog):
    """Inspect registration, contract coverage and review basis without executing checkers."""
    from ._serialization import digest

    definition = catalog.get(reference)
    if not isinstance(definition, (Capability, Protocol)):
        raise TypeError("Definition audit requires a Capability or Protocol")
    issues = []

    def unresolved(code, message):
        issues.append(AuditIssue(code, "unverified", message))

    capability = (
        definition
        if isinstance(definition, Capability)
        else (catalog.get(definition.capability_ref) if definition.capability_ref else None)
    )
    if capability is None:
        unresolved("capability_missing", "Protocol has no associated common contract")
    else:
        for field in (*capability.inputs, *capability.outputs):
            if field.validator is None and field.checker_ref is None:
                unresolved(
                    "field_unresolved",
                    "Semantic field lacks executable representation: " + field.name,
                )
    requirements = (*capability.requirements,) if capability else ()
    if isinstance(definition, Protocol):
        requirements = (*requirements, *definition.requirements, *definition.provenance_checks)
        if definition.pending or any(step.pending for step in definition.steps):
            unresolved("pending_implementation", "Protocol declares unresolved provider work")
        if set(definition.provenance_requirements) - {
            item.identifier for item in definition.provenance_checks if item.mandatory
        }:
            unresolved(
                "provenance_verifier", "Provenance guarantees need invocation-specific evidence"
            )
    for requirement in requirements:
        if requirement.mandatory and requirement.checker_ref is None:
            unresolved(
                "checker_unresolved",
                "Mandatory guarantee has no checker: " + requirement.identifier,
            )
    if not catalog.reviews_for(reference):
        unresolved("admission_unreviewed", "No explicit admission review is retained")
    status = catalog.status_for(reference)
    if status["validation"] in {"unassessed", "inconclusive", "conflicting"}:
        unresolved(
            "validation_unresolved",
            "No uncontradicted scientific assessment covers this definition",
        )
    return AuditReport(
        str(reference),
        (
            "Definition content digest: " + digest(definition),
            "Catalog maturity: " + status["maturity"],
            *[issue.message for issue in issues],
        ),
        ("No provider is invoked; structural inspection is not scientific certification",),
        "unverified" if issues else "consistent",
        tuple(issues),
    )


def audit_benchmark(identifier, *, records):
    """Check method links, scheduled denominators and evaluator result consistency offline."""
    from .benchmarks import load_benchmark

    result = load_benchmark(identifier, records=records)
    issues = []

    def issue(code, message, severity="violated"):
        issues.append(AuditIssue(code, severity, message))

    schedule = [
        (case.identifier, method.protocol_ref.to_dict(), method.binding_ref.to_dict(), replicate)
        for case in result.spec.cases
        for method in result.spec.methods
        for replicate in range(result.spec.replicates)
    ]
    actual = [
        (row.get("case"), row.get("protocol_ref"), row.get("binding_ref"), row.get("replicate"))
        for row in result.rows
    ]
    if actual != schedule:
        issue("benchmark_schedule", "Retained rows disagree with the full declared schedule")
    for row in result.rows:
        if row.get("evaluator_ref") != result.spec.evaluator_ref.to_dict():
            issue("evaluator_identity", "Measurement identifies another evaluator version")
        if row.get("metric_status") == "available":
            from .benchmarks.runner import _measurement

            try:
                value = (
                    {key: item["value"] for key, item in row.get("metrics", {}).items()}
                    if result.spec.metrics
                    else row.get("metric_value")
                )
                _measurement(value, result.spec)
            except (ValueError, KeyError, TypeError):
                issue(
                    "metric_evidence",
                    "Available measurements contradict their declared types/units",
                )
        if row.get("evaluator_configuration", {}) != result.spec.evaluator_configuration:
            issue(
                "evaluator_configuration",
                "Retained evaluator configuration contradicts the specification",
            )
        if row.get("evaluation_recording_status") in {"gap", "incomplete"}:
            issue(
                "evaluation_recording_gap",
                "Evaluator recording has incomplete coverage",
                "unverified",
            )
        if row.get("attempt_id") is not None:
            try:
                attempt = records.attempt(row["attempt_id"])
            except FileNotFoundError:
                issue(
                    "attempt_missing",
                    "Benchmark refers to an unavailable method attempt",
                    "unverified",
                )
                continue
            if (
                row["method_status"] != attempt.operational_status
                or row["contract_status"] != attempt.contract_status
            ):
                issue("attempt_outcome", "Benchmark row contradicts its retained method attempt")
            prepared = records.prepared(attempt.prepared_id)
            if (
                prepared.selection.protocol_ref.to_dict()
                if prepared.selection.protocol_ref
                else None
            ) != row["protocol_ref"] or (
                prepared.selection.binding_ref.to_dict() if prepared.selection.binding_ref else None
            ) != row["binding_ref"]:
                issue("method_identity", "Benchmark row contradicts its consumed method identity")
            for finding in audit_execution(attempt.identifier, records=records).issues:
                issues.append(finding)
    if result.status != "completed":
        issue("benchmark_incomplete", "Benchmark has no completed schedule", "unverified")
    outcome = (
        "violated"
        if any(item.severity == "violated" for item in issues)
        else ("unverified" if issues else "consistent")
    )
    return AuditReport(
        identifier,
        (
            "Benchmark status: " + result.status,
            "Retained scheduled rows: " + str(len(result.rows)),
            "Exact specification: " + str(result.spec.ref),
            *[item.message for item in issues],
        ),
        ("Audits retained measurement evidence; does not recompute scientific metrics",),
        outcome,
        tuple(issues),
    )
