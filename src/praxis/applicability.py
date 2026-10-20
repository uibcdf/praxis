"""Tri-state scientific checks, separate from implementation availability."""

from dataclasses import dataclass, replace

from ._diagnostics import advise
from ._field_checks import field_findings, parameter_findings
from ._serialization import Model, snapshot
from .definitions import CheckFinding
from .extensions import CheckResult


@dataclass(frozen=True)
class ApplicabilityReport(Model):
    schema = "praxis.applicability/0.1"
    outcome: str
    findings: tuple[CheckFinding, ...]


def evaluate_check(
    identifier, phase, mandatory, checker_ref, inputs, configuration, extensions, outputs=None
):
    checker = extensions.checkers.get(checker_ref)
    if checker is None:
        result = CheckResult("undetermined", "No checker is registered for this requirement")
    else:
        try:
            result = checker(snapshot(inputs), snapshot(configuration), snapshot(outputs))
            if type(result) is not CheckResult:
                raise TypeError("A checker must return CheckResult")
            result = CheckResult.from_dict(result.to_dict())
        except Exception as error:
            advise("PRAXIS-CHECKER-ERROR")
            return CheckFinding(
                identifier,
                phase,
                "checker_error",
                mandatory,
                checker_ref,
                f"Checker raised {type(error).__name__}; scientific conclusion is unresolved",
            )
    return CheckFinding(
        identifier,
        phase,
        result.outcome,
        mandatory,
        checker_ref,
        result.reason,
        result.evidence,
        result.coverage,
        result.evidence_records,
    )


def evidence_problem(requirement, finding, subject_digest, *, attempt_id=None, steps=()):
    records = finding.evidence_records
    if finding.outcome != "passed":
        return None
    if (
        requirement.review_required or requirement.coverage_required == "throughout"
    ) and not records:
        return "Required scoped evidence is absent"
    for record in records:
        if (
            record.requirement != requirement.identifier
            or record.subject_digest != subject_digest
            or record.kind not in requirement.accepted_evidence
            or record.outcome != "passed"
        ):
            return "Evidence basis, outcome or scientific subject does not match this requirement"
        if requirement.review_required and (
            record.kind != "human" or record.authority not in requirement.human_authorities
        ):
            return "Human evidence has no permitted authority for this contract"
        if requirement.coverage_required == "throughout":
            if (
                record.coverage != "throughout"
                or record.attempt_id != attempt_id
                or not set(steps) <= set(record.steps)
            ):
                return "Evidence does not cover this attempt and all required operation intervals"
    return None


def check_requirements(
    requirements,
    phase,
    inputs,
    configuration,
    extensions,
    outputs=None,
    *,
    reviews=(),
    subject_digest=None,
    attempt_id=None,
    steps=(),
):
    findings = []
    for item in requirements:
        if item.phase != phase:
            continue
        if item.review_required:
            matching = tuple(
                record
                for record in reviews
                if record.requirement == item.identifier
                and record.subject_digest == subject_digest
                and record.kind == "human"
                and record.authority in item.human_authorities
            )
            outcomes = {record.outcome for record in matching}
            outcome = next(iter(outcomes)) if len(outcomes) == 1 else "undetermined"
            finding = CheckFinding(
                item.identifier,
                phase,
                outcome,
                item.mandatory,
                item.checker_ref,
                "Permitted scoped human review inspected"
                if matching
                else "Human review is pending",
                evidence_records=matching,
            )
        else:
            finding = evaluate_check(
                item.identifier,
                phase,
                item.mandatory,
                item.checker_ref,
                inputs,
                configuration,
                extensions,
                outputs,
            )
        problem = evidence_problem(
            item, finding, subject_digest, attempt_id=attempt_id, steps=steps
        )
        if problem is not None:
            finding = replace(finding, outcome="undetermined", reason=problem)
        findings.append(finding)
    return tuple(findings)


def checker_references(capability, protocol):
    return (
        *tuple(
            item.checker_ref
            for item in (
                *capability.inputs,
                *capability.outputs,
                *capability.requirements,
                *protocol.requirements,
                *protocol.provenance_checks,
                *protocol.parameters,
            )
        ),
        *(step.condition_ref for step in protocol.steps),
    )


def summarize(findings):
    required = [item for item in findings if item.mandatory]
    if any(item.outcome == "failed" for item in required):
        return "inapplicable"
    if any(item.outcome != "passed" for item in required):
        return "undetermined"
    return "applicable"


def assess_applicability(capability, protocol, inputs, configuration, extensions, *, reviews=()):
    from .provenance import invocation_digest

    subject_digest = invocation_digest(capability.ref, protocol.ref, inputs, configuration)
    findings = (
        *field_findings(capability.inputs, "pre", inputs, configuration, extensions),
        *parameter_findings(protocol.parameters, inputs, configuration, extensions),
        *check_requirements(
            (*capability.requirements, *protocol.requirements, *protocol.provenance_checks),
            "pre",
            inputs,
            configuration,
            extensions,
            reviews=reviews,
            subject_digest=subject_digest,
        ),
    )
    if protocol.capability_ref != capability.ref:
        findings = (
            *findings,
            CheckFinding(
                "capability_association",
                "pre",
                "failed",
                True,
                None,
                "Protocol does not target this exact Capability",
            ),
        )
    return ApplicabilityReport(summarize(findings), findings)
