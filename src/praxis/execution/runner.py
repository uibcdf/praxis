"""First sequential runner: pinned intent, phase gates, declared steps and preserved failures."""

from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from .._ackredit import capture_attempt
from .._diagnostics import advise
from .._field_checks import field_findings
from .._serialization import digest, snapshot
from ..applicability import assess_applicability, check_requirements, checker_references, summarize
from ..definitions import Capability, MethodRef, Protocol
from ..errors import (
    CancelledError,
    ContractError,
    IntegrityError,
    NotReadyError,
    RecordingError,
    WaitingForReview,
)
from ..provenance import environment_findings, environment_manifest, invocation_digest
from ..recording import NoRecorder
from ..selection import select
from .reports import AttemptRecord, PreparedInvocation


def now():
    return datetime.now(timezone.utc).isoformat()


def _configuration(protocol, supplied):
    configuration = snapshot(supplied)
    reasons = []
    names = {item.name for item in protocol.parameters}
    if set(configuration) - names:
        reasons.append("Undeclared scientific parameters were supplied")
    for item in protocol.parameters:
        if item.name not in configuration:
            if item.required:
                reasons.append(f"Required parameter is missing: {item.name}")
            else:
                configuration[item.name] = snapshot(item.default)
    return configuration, reasons


def _input_reasons(capability, inputs):
    names = {item.name for item in capability.inputs}
    reasons = []
    if set(inputs) - names:
        reasons.append("Undeclared input fields were supplied")
    for item in capability.inputs:
        if item.required and item.name not in inputs:
            reasons.append(f"Required input is missing: {item.name}")
    return reasons


def prepare(request, *, catalog, context):
    if request.capability_ref is None:
        if request.protocol_ref is None:
            raise NotReadyError("Request requires a Capability or exact Protocol")
        requested_protocol = catalog.get(request.protocol_ref)
        if (
            not isinstance(requested_protocol, Protocol)
            or requested_protocol.capability_ref is None
        ):
            raise NotReadyError("Protocol request has no target Capability")
        request = replace(request, capability_ref=requested_protocol.capability_ref)
    capability = catalog.get(request.capability_ref)
    if not isinstance(capability, Capability):
        raise NotReadyError("Request must identify an exact Capability")
    selection = select(request, catalog, context.extensions, reviews=context.reviews)
    reasons = list(selection.reasons)
    if catalog.status_for(capability.ref)["maturity"] != "experimental":
        reasons.append("Capability is deprecated or withdrawn")
    inputs = snapshot(request.inputs)
    configuration = snapshot(request.configuration)
    reasons.extend(_input_reasons(capability, inputs))
    definitions = [capability.to_dict()]
    binding_description = None
    dependencies = tuple(context.environment_requirements.get("packages", {}))
    findings = ()
    checkers = ()
    if selection.protocol_ref is not None:
        protocol = catalog.get(selection.protocol_ref)
        definitions.append(protocol.to_dict())
        checkers = context.extensions.describe_checkers(checker_references(capability, protocol))
        configuration, config_reasons = _configuration(protocol, configuration)
        reasons.extend(config_reasons)
        findings = assess_applicability(
            capability, protocol, inputs, configuration, context.extensions, reviews=context.reviews
        ).findings
        if summarize(findings) != "applicable":
            reasons.append("Mandatory scientific preconditions are not all passed")
        if protocol.pending or any(item.pending for item in protocol.steps):
            reasons.append("Protocol has unresolved scientific or implementation work")
        verified = {item.identifier for item in protocol.provenance_checks if item.mandatory}
        if set(protocol.provenance_requirements) - verified:
            reasons.append("Protocol provenance requirements have no declared mandatory verifier")
        if selection.binding_ref is not None:
            binding = context.extensions.bindings[selection.binding_ref]
            binding_description = binding.description()
            dependencies = (*dependencies, *binding.dependencies)
            from depdigest import is_installed

            if any(not is_installed(module) for module in binding.dependencies):
                reasons.append("A required implementation dependency is unavailable")
    catalog_snapshot = ()
    child_implementations = []
    if selection.protocol_ref is not None and any(
        step.kind == "capability" for step in protocol.steps
    ):
        catalog_snapshot = tuple(item.to_dict() for item in catalog.definitions())
        for step in protocol.steps:
            if step.kind != "capability":
                continue
            child_capability = catalog.get(step.child_capability_ref)
            candidates = catalog.protocols_for(child_capability.ref)
            if step.child_protocol_ref is not None:
                candidates = tuple(
                    item for item in candidates if item.ref == step.child_protocol_ref
                )
            if not candidates:
                reasons.append(
                    "Declared child has no compatible Protocol candidate: " + step.identifier
                )

            def pin_children(capability, protocols, root_step, seen=()):
                for candidate in protocols:
                    if candidate.ref in seen:
                        continue
                    for child_binding in context.extensions.bindings_for(candidate.ref):
                        if (
                            step.child_binding_ref is not None
                            and root_step == step.identifier
                            and capability.ref == child_capability.ref
                            and child_binding.ref != step.child_binding_ref
                        ):
                            continue
                        child_implementations.append(
                            {
                                "step": root_step,
                                "binding": child_binding.description(),
                                "checkers": list(
                                    context.extensions.describe_checkers(
                                        checker_references(capability, candidate)
                                    )
                                ),
                            }
                        )
                    for nested in candidate.steps:
                        if nested.kind != "capability":
                            continue
                        nested_capability = catalog.get(nested.child_capability_ref)
                        nested_candidates = catalog.protocols_for(nested_capability.ref)
                        if nested.child_protocol_ref is not None:
                            nested_candidates = tuple(
                                item
                                for item in nested_candidates
                                if item.ref == nested.child_protocol_ref
                            )
                        pin_children(
                            nested_capability, nested_candidates, root_step, (*seen, candidate.ref)
                        )

            pin_children(child_capability, candidates, step.identifier)
        for step in protocol.steps:
            if step.kind == "capability" and not any(
                item["step"] == step.identifier for item in child_implementations
            ):
                reasons.append("Declared child has no available implementation: " + step.identifier)
    observed = environment_manifest(dependencies, supplied=context.environment_metadata)
    reasons.extend(environment_findings(context.environment_requirements, observed))
    prepared = PreparedInvocation(
        str(uuid4()),
        now(),
        capability.ref,
        selection,
        inputs,
        configuration,
        tuple(definitions),
        binding_description,
        findings,
        not reasons,
        tuple(reasons),
        checkers=checkers,
        environment_requirements=snapshot(context.environment_requirements),
        environment_observed=observed,
        actor=context.actor,
        authority=context.authority,
        catalog_snapshot=catalog_snapshot,
        child_implementations=tuple(child_implementations),
    )
    context.records.save_prepared(prepared)
    return prepared


def _verify_policy_pin(prepared, extensions):
    if prepared.selection.policy_implementation is not None:
        from ..selection import BUILTIN_POLICY

        policy_ref = MethodRef.from_dict(prepared.selection.policy_implementation["ref"])
        if (
            policy_ref != BUILTIN_POLICY
            and extensions.describe_policy(policy_ref) != prepared.selection.policy_implementation
        ):
            raise NotReadyError("Pinned selection policy has changed")


def _verify_child_pins(prepared, extensions):
    for item in prepared.child_implementations:
        reference = MethodRef.from_dict(item["binding"]["ref"])
        current = extensions.bindings.get(reference)
        if current is None or current.description() != item["binding"]:
            raise NotReadyError("Pinned nested child implementation is unavailable or changed")
        refs = tuple(MethodRef.from_dict(check["ref"]) for check in item["checkers"])
        if list(extensions.describe_checkers(refs)) != item["checkers"]:
            raise NotReadyError("Pinned nested child checker is unavailable or changed")


class RecipeContext:
    """Declared boundaries, bounded repetition, runtime gates and pinned child calls."""

    def __init__(
        self,
        protocol,
        recorder,
        recording_refs,
        *,
        prepared,
        context,
        catalog,
        identifier,
        ancestors,
    ):
        self.protocol = protocol
        self.prepared = prepared
        self.context = context
        self.catalog = catalog
        self.identifier = identifier
        self.ancestors = ancestors
        self.recorder = recorder
        self.recording_refs = recording_refs
        self.steps = []
        self.branches = []
        self.runtime_findings = []
        self.child_ids = []
        self.schedule = tuple(
            (step, iteration) for step in protocol.steps for iteration in range(step.repeat)
        )

    def _cancel(self):
        if self.context.cancelled:
            raise CancelledError("Application cancellation observed at a declared boundary")

    def _next(self, identifier):
        self._cancel()
        ordinal = len(self.steps)
        if ordinal >= len(self.schedule) or self.schedule[ordinal][0].identifier != identifier:
            raise ContractError("Recipe steps must match the declared bounded procedure")
        return self.schedule[ordinal]

    def branch(self, identifier, *, outputs=None):
        from ..applicability import evaluate_check

        definition, iteration = self._next(identifier)
        if definition.condition_ref is None:
            raise ContractError("Branch requires a declared condition checker")
        if any(item["ordinal"] == len(self.steps) for item in self.branches):
            raise ContractError("A branch decision cannot be silently replaced")
        finding = evaluate_check(
            "branch/" + identifier,
            "runtime",
            True,
            definition.condition_ref,
            self.prepared.inputs,
            self.prepared.configuration,
            self.context.extensions,
            outputs,
        )
        decision = {
            "identifier": identifier,
            "iteration": iteration,
            "ordinal": len(self.steps),
            "checker_ref": definition.condition_ref.to_dict(),
            "finding": finding.to_dict(),
        }
        self.branches.append(decision)
        if finding.outcome not in {"passed", "failed"}:
            raise NotReadyError("Branch condition is unresolved")
        if finding.outcome == "failed":
            self.steps.append(
                {
                    "identifier": identifier,
                    "provider": definition.provider,
                    "operation": definition.operation,
                    "iteration": iteration,
                    "started": now(),
                    "finished": now(),
                    "status": "skipped",
                    "observation_scope": "declared branch not taken",
                }
            )
            return False
        return True

    @contextmanager
    def step(self, identifier):
        definition, iteration = self._next(identifier)
        if definition.condition_ref is not None and not any(
            item["ordinal"] == len(self.steps) and item["finding"]["outcome"] == "passed"
            for item in self.branches
        ):
            raise ContractError("A conditional step requires its recorded branch decision")
        entry = {
            "identifier": identifier,
            "provider": definition.provider,
            "operation": definition.operation,
            "iteration": iteration,
            "started": now(),
            "finished": None,
            "status": "running",
            "observation_scope": "declared recipe boundary",
        }
        self.steps.append(entry)
        try:
            with self.recorder.operation(
                "praxis.step",
                parameters={"step": identifier, "iteration": iteration},
                implementation={"provider": definition.provider, "operation": definition.operation},
            ) as operation:
                correlation = operation.correlation()
                if correlation is not None:
                    self.recording_refs.append(correlation)
                yield operation
            entry["status"] = "completed"
        except WaitingForReview:
            entry["status"] = "waiting"
            raise
        except CancelledError:
            entry["status"] = "cancelled"
            raise
        except BaseException:
            entry["status"] = "failed"
            raise
        finally:
            entry["finished"] = now()

    def check(self, identifier, *, outputs=None):
        self._cancel()
        capability = Capability.from_dict(self.prepared.definitions[0])
        requirements = (
            *capability.requirements,
            *self.protocol.requirements,
            *self.protocol.provenance_checks,
        )
        requirement = next(
            (
                item
                for item in requirements
                if item.identifier == identifier and item.phase == "runtime"
            ),
            None,
        )
        if requirement is None or any(
            item.requirement == identifier for item in self.runtime_findings
        ):
            raise ContractError("Runtime guarantee must be declared and inspected exactly once")
        finding = check_requirements(
            (requirement,),
            "runtime",
            self.prepared.inputs,
            self.prepared.configuration,
            self.context.extensions,
            outputs,
            reviews=self.context.reviews,
            subject_digest=invocation_digest(
                capability.ref, self.protocol.ref, self.prepared.inputs, self.prepared.configuration
            ),
            attempt_id=self.identifier,
            steps=tuple(step.identifier for step in self.protocol.steps),
        )[0]
        self.runtime_findings.append(finding)
        if finding.mandatory and finding.outcome != "passed":
            if requirement.review_required and finding.outcome != "failed":
                raise WaitingForReview("Declared human review remains unresolved")
            if finding.outcome == "failed":
                raise ContractError("Runtime contract guarantee failed")
            raise NotReadyError("Runtime contract guarantee lacks sufficient evidence")
        return finding

    def invoke(
        self, identifier, inputs, *, configuration=None, protocol_ref=None, binding_ref=None
    ):
        from ..catalog.catalog import snapshot_catalog
        from .reports import MethodRequest

        definition, _ = self._next(identifier)
        if definition.kind != "capability":
            raise ContractError("Child invocation requires a declared Capability step")
        if (
            definition.child_capability_ref in self.ancestors
            or len(self.ancestors) >= self.context.max_depth
        ):
            raise ContractError("Recursive or excessive Capability composition is prohibited")
        _verify_child_pins(self.prepared, self.context.extensions)
        frozen = snapshot_catalog(self.prepared.catalog_snapshot)
        request = MethodRequest(
            definition.child_capability_ref,
            inputs,
            configuration or {},
            protocol_ref or definition.child_protocol_ref,
            binding_ref or definition.child_binding_ref,
        )
        prepared = prepare(request, catalog=frozen, context=self.context)
        if not prepared.ready:
            raise NotReadyError("Child preparation is not ready: " + "; ".join(prepared.reasons))
        descriptions = [
            item
            for item in self.prepared.child_implementations
            if item["step"] == identifier
            and item["binding"]["ref"] == (prepared.binding or {}).get("ref")
        ]
        if (
            not descriptions
            or prepared.binding != descriptions[0]["binding"]
            or list(prepared.checkers) != descriptions[0]["checkers"]
        ):
            raise NotReadyError(
                "Selected child implementation differs from preserved parent candidates"
            )
        if (
            self.catalog.status_for(prepared.capability_ref)["maturity"] != "experimental"
            or self.catalog.status_for(prepared.selection.protocol_ref)["maturity"]
            != "experimental"
        ):
            raise NotReadyError("Selected child method has been withdrawn or deprecated")
        child_id = str(uuid4())
        self.child_ids.append(child_id)
        with self.step(identifier):
            outputs, attempt = execute(
                prepared,
                catalog=frozen,
                context=self.context,
                identifier=child_id,
                parent_id=self.identifier,
                _ancestors=self.ancestors,
            )
            if attempt.contract_status != "supported":
                raise ContractError("Child invocation did not support its Capability contract")
            return outputs, attempt

    def verify(self):
        self._cancel()
        if len(self.steps) != len(self.schedule) or any(
            step["status"] not in {"completed", "skipped"} for step in self.steps
        ):
            raise ContractError("Recipe did not complete all declared step boundaries")
        capability = Capability.from_dict(self.prepared.definitions[0])
        expected = {
            item.identifier
            for item in (
                *capability.requirements,
                *self.protocol.requirements,
                *self.protocol.provenance_checks,
            )
            if item.phase == "runtime"
        }
        if expected != {item.requirement for item in self.runtime_findings}:
            raise ContractError("Recipe omitted declared runtime guarantee checks")


def execute(
    prepared,
    *,
    catalog,
    context,
    retry_of=None,
    identifier=None,
    parent_id=None,
    replay_of=None,
    _ancestors=(),
):
    """Return outputs and a retained record. Failures retain their record and re-raise.

    Exceptions receive only a safe attempt-ID note; scientific error types/messages
    are neither replaced nor copied into persisted method records.
    """
    identifier = identifier or str(uuid4())
    if retry_of is not None:
        previous = context.records.attempt(retry_of)
        if previous.prepared_id != prepared.identifier:
            raise NotReadyError("A retry must reference the same prepared intent")
    attempt = AttemptRecord(
        identifier,
        prepared.identifier,
        now(),
        None,
        "running",
        "unassessed",
        "pending" if context.recorder else "not_requested",
        (),
        (),
        None,
        environment_manifest(
            (prepared.binding or {}).get("dependencies", [])
            + list(prepared.environment_requirements.get("packages", {})),
            supplied=context.environment_metadata,
        ),
        retry_of=retry_of,
        parent_id=parent_id,
        replay_of=replay_of,
        actor=context.actor,
        authority=context.authority,
    )
    try:
        context.records.save_attempt(attempt)
    except BaseException as error:
        error.add_note("Praxis method attempt: " + identifier)
        raise
    recorder = context.recorder or NoRecorder()
    correlations = []
    recipe_context = None
    findings = ()
    outputs = None
    captured = None
    error = None
    contract_status = "unassessed"
    implementations = ()
    try:
        retained = context.records.prepared(prepared.identifier)
        if digest(retained) != digest(prepared):
            raise IntegrityError("Prepared intent differs from its preserved snapshot")
        if not prepared.ready:
            raise NotReadyError("Prepared invocation is not ready: " + "; ".join(prepared.reasons))
        capability = Capability.from_dict(prepared.definitions[0])
        protocol = Protocol.from_dict(prepared.definitions[1])
        reasons = environment_findings(prepared.environment_requirements, attempt.environment)
        if reasons:
            raise NotReadyError("; ".join(reasons))
        for definition in (capability, protocol):
            if catalog.status_for(definition.ref)["maturity"] != "experimental":
                raise NotReadyError("Method is withdrawn, deprecated or has conflicting status")
            if digest(catalog.get(definition.ref)) != digest(definition):
                raise IntegrityError("Catalog definition no longer matches prepared intent")
        _verify_policy_pin(prepared, context.extensions)
        binding = context.extensions.bindings.get(prepared.selection.binding_ref)
        if binding is None or binding.description() != prepared.binding:
            raise NotReadyError("Pinned binding is unavailable or has changed")
        checkers = context.extensions.describe_checkers(checker_references(capability, protocol))
        if checkers != prepared.checkers:
            raise NotReadyError("Pinned checkers are unavailable or have changed")
        _verify_child_pins(prepared, context.extensions)
        implementations = (binding.description(), *checkers)
        from depdigest import check_dependency

        for module in binding.dependencies:
            check_dependency(module, caller="Praxis implementation binding", pypi_name=None)
        # Preparation is not an authorization to bypass checks at actual consumption.
        findings = assess_applicability(
            capability,
            protocol,
            prepared.inputs,
            prepared.configuration,
            context.extensions,
            reviews=context.reviews,
        ).findings
        if summarize(findings) != "applicable":
            raise NotReadyError("Mandatory preconditions no longer support execution")
        recipe_context = RecipeContext(
            protocol,
            recorder,
            correlations,
            prepared=prepared,
            context=context,
            catalog=catalog,
            identifier=identifier,
            ancestors=(*_ancestors, capability.ref),
        )
        recipe_context._cancel()
        prepared_path = context.records.save_prepared(prepared)
        operation_inputs = {"prepared_id": prepared.identifier, "attempt_id": identifier}
        if context.recorder is not None:
            operation_inputs["prepared"] = recorder.reference(
                prepared_path, "prepared/" + prepared.identifier
            )
        with recorder.operation(
            "praxis.execute",
            inputs=operation_inputs,
            implementation={"protocol": str(protocol.ref), "binding": str(binding.ref)},
        ) as operation:
            correlation = operation.correlation()
            if correlation is not None:
                correlations.append(correlation)
            with capture_attempt(identifier, context.attribution) as captured:
                result = binding.recipe(
                    snapshot(prepared.inputs), snapshot(prepared.configuration), recipe_context
                )
                if type(result) is not dict:
                    raise ContractError("First-slice recipes return JSON output objects")
                outputs = snapshot(result)
                recipe_context.verify()
                if any(item.required and item.name not in outputs for item in capability.outputs):
                    raise ContractError("Required Capability outputs are missing")
                post = (
                    *field_findings(
                        capability.outputs,
                        "post",
                        prepared.inputs,
                        prepared.configuration,
                        context.extensions,
                        outputs,
                    ),
                    *check_requirements(
                        (
                            *capability.requirements,
                            *protocol.requirements,
                            *protocol.provenance_checks,
                        ),
                        "post",
                        prepared.inputs,
                        prepared.configuration,
                        context.extensions,
                        outputs,
                        reviews=context.reviews,
                        subject_digest=invocation_digest(
                            capability.ref, protocol.ref, prepared.inputs, prepared.configuration
                        ),
                        attempt_id=identifier,
                        steps=tuple(step.identifier for step in protocol.steps),
                    ),
                )
                findings = (*findings, *recipe_context.runtime_findings, *post)
                contract_status = "supported" if summarize(post) == "applicable" else "unsupported"
            operation.output("contract_status", contract_status)
    except BaseException as caught:
        error = caught
        if isinstance(error, ContractError):
            contract_status = "violated"
    finally:
        recording_status = "not_requested"
        if context.recorder is not None:
            try:
                recording_status = (
                    "not_started" if recipe_context is None else recorder.coverage(correlations)
                )
                # Any excluded step prevents a complete-boundaries claim.
                if recipe_context is not None and len(correlations) != 1 + sum(
                    step["status"] != "skipped" for step in recipe_context.steps
                ):
                    recording_status = "omitted_by_policy"
                if isinstance(error, RecordingError):
                    recording_status = "gap"
            except Exception:
                recording_status = "gap"
            if recording_status == "gap":
                advise("PRAXIS-RECORDING-GAP")
        if recipe_context is not None:
            retained_keys = {(item.phase, item.requirement) for item in findings}
            findings = (
                *findings,
                *(
                    item
                    for item in recipe_context.runtime_findings
                    if (item.phase, item.requirement) not in retained_keys
                ),
            )
        if isinstance(error, WaitingForReview):
            status = "waiting"
        elif isinstance(error, CancelledError):
            status = "cancelled"
        elif isinstance(error, (KeyboardInterrupt, SystemExit)):
            status = "interrupted"
        elif isinstance(error, NotReadyError):
            status = "blocked"
        else:
            status = "failed" if error is not None else "completed"
        attribution = captured.attribution.to_dict() if captured is not None else None
        final = replace(
            attempt,
            finished=now(),
            operational_status=status,
            contract_status=contract_status,
            recording_status=recording_status,
            findings=tuple(findings),
            steps=tuple(recipe_context.steps) if recipe_context else (),
            outputs=outputs,
            failure_type=type(error).__name__ if error else None,
            recording_refs=tuple(correlations),
            attribution=attribution,
            implementations=implementations,
            child_ids=tuple(recipe_context.child_ids) if recipe_context else (),
            branches=tuple(recipe_context.branches) if recipe_context else (),
        )
        try:
            context.records.save_attempt(final)
        except BaseException as persistence_error:
            if error is None:
                persistence_error.add_note("Praxis method attempt: " + identifier)
                raise
            error.add_note(
                "Praxis could not persist the terminal method record: "
                + type(persistence_error).__name__
            )
        if error is not None:
            error.add_note("Praxis method attempt: " + identifier)
    if error is not None:
        raise error
    return outputs, final
