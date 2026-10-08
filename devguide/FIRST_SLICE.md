# Experimental local implementation

The working Python implementation exercises the programming design under
[Praxis #1](https://github.com/uibcdf/praxis/issues/1) and the contract, invocation,
assessment and benchmark proposals [#5–#8](https://github.com/uibcdf/praxis/issues/5).
Definitions, local schemas and interfaces remain experimental. This guide describes
implemented behavior; [the programming design](pending_proposals/initial_implementation_design.md)
remains the broader target.

## Definitions, curation and historical identity

`Capability` states semantic inputs/outputs, intent, requirements and authorized
changes. `Protocol` states a procedure, exact target, parameters, provider/child
steps, provenance checks, resource/fidelity profile, tradeoffs and limitations.
`MethodRef` carries owner/kind/identifier/version; scientific versions differ from
schema versions. Catalog admission persists a definition without certifying it.

`Catalog.open(directory)` admits immutable JSON envelopes by exact identity and
content digest. Identical registration is idempotent; different content under the
same identity fails. Separate records preserve:

- `AdmissionReview`: exact definition digest, proposer/maintainer/reviewer/authority,
  outcome, conditions, explicit assessment evidence and optional source workflow.
  Promotion requires supporting assessments and does not rewrite the definition.
- `Assessment`: actor/authority, criteria, findings, evidence, limitations, exact
  subject and structured scenario, explicit supersession/withdrawal.
- `SuitabilityStatement`: favorable/discouraged/exclusion/unknown, criteria,
  scenario, alternative and proposed/estimated/measured/unknown evidence basis.
- `MethodStatus`: explicit experimental/deprecated/withdrawn event, reason,
  replacement and supersession; historical definitions are never deleted.

`assessments_for`, `suitability_for`, `reviews_for` return history or explicitly active
records. `status_for(ref, scenario=...)` projects exact-scenario judgments, keeping
unresolved contradictions visible. Timestamps never choose a winner. An omitted
scenario gathers recorded judgments for inspection and is not universal support.
`query` filters kind, text and semantic input/output names; discovery does not establish
applicability. `benchmarks_for` discovers exact registered specifications.

`export_bundle`/`import_bundle` preserve definitions and records with a bundle digest.
All schemas, associations and existing conflicts are checked before admission.
Schema migration requires an explicit incoming adapter; it cannot change scientific
identity. Existing records are not migrated in place. I/O failure may leave a partial
admission; retrying identical documents is safe. Envelopes establish local consistency,
not authentication, distributed transactions or power-loss durability across files.

## Selection, parameters and preparation

`MethodRequest` accepts a Capability, or an exact associated Protocol alone. A choice
can be explicit, or use the sole eligible candidate. Ambiguity abstains. Binding
selection is a separate exact choice; multiple bindings do not win by import order.

`SelectionPolicy` has an exact registered extension or the built-in unique-eligible
policy, structured criteria and scenario. Criteria can require applicability,
availability, supported assessments, measured favorable suitability, fidelity,
cost class or an expected-duration budget. Scientific support/suitability criteria
require a nonempty exact scenario. Unknown or contradictory evidence abstains. Missing
registered policies reject even an explicit Protocol choice.
Custom policies can choose only eligible candidates and retain their callable identity.
Selection records retain candidate definitions, findings/status, binding references,
criteria, reasons and policy implementation. No text claim becomes an automatic score.

Fields explicitly select `json`, `number`, `finite_number`, `string`, `boolean`,
`array`, `object` or `quantity`, optionally with a versioned semantic checker. Prose
alone is unresolved. Quantity fields use PyUnitWizard's sealed `QuantityRecord`,
explicit semantic field and compatible unit handshake. Parameters have the same
validators, units, quantity field, bounds, choices and optional checker. These checks
inspect declared structure/semantics; scientific nested configuration remains provider
work. Optional absent fields skip nonmandatorily; supplied fields must pass. All
retained ordinary JSON values and decoded physical values are finite.

`prepare(request, catalog=..., context=...)` saves inputs, resolved defaults,
configuration, exact definitions, binding/checker/policy identities, readiness reasons,
actor/declared authority and observed environment even when rejected. Environment
constraints can name exact Python/system/machine/package observations; unsupported
constraints do not silently pass. Application metadata records hardware/container/model
context when supplied. Observation is not environment authentication or a full machine
inventory; credentials and automatic GPU probes are not collected.

## Contract gates and evidence

`Requirement` declares pre/runtime/post phase, mandatory role, exact checker,
boundary/throughout coverage, permitted evidence kinds and optional human authorities.
`EvidenceRecord` binds a retained evidence reference to guarantee, invocation digest,
outcome, coverage, actor/authority/date and, for throughout claims, exact attempt and
all declared step identifiers. Evidence declarations do not authenticate their author
or independently inspect opaque native internals. Providers own enforcement; auditors
check preserved scope and consistency. Endpoint equality/restoration cannot prove
throughout preservation. `provenance_checks` explicitly verifies named mandatory
`provenance_requirements`; descriptive provenance without a verifier blocks readiness.

| Mandatory result | Preparation/consumption behavior |
| --- | --- |
| passed with required scope | Eligible at that phase; never scientific promotion |
| failed | Inapplicable precondition or violated runtime guarantee; support rejected |
| undetermined/checker_error/skipped | Unresolved; cannot support compliance |
| unresolved runtime human review | `WaitingForReview`, retained waiting attempt |
| advisory unresolved | Retained finding; does not replace a mandatory check |

Required preconditions are reevaluated at execution. Runtime recipes call
`runtime.check(id, outputs=...)` for each declared runtime guarantee exactly once.
A human record must match invocation digest and permitted authority. Human review
and executable checks have separate guarantee identities. An application
adds an actual review to `context.reviews` and explicitly retries as a new attempt;
there is no autonomous approval, suspended-process resumption or authenticated identity
service. A checker exception remains distinct from scientific failure.

## Execution and composition

`execute(prepared, catalog=..., context=...)` returns `(outputs, attempt)` on operational
completion. Operational, contract and operation-recording status are separate. Completion
can have unsupported postchecks. Native exceptions retain type and receive the attempt ID;
initial/terminal snapshots preserve failures, partial outputs, interrupted/cancelled/waiting
attempts. `retry_of` requires the same prepared intent and does not promise continuation
or rollback. Missing terminal evidence reads as incomplete, without an invented cause.

Bindings/checkers/policies are explicitly registered through `Extensions`; mappings are
read-only. Frozen implementation fingerprints detect observed Python code/defaults and
package changes. They do not capture transitive helpers, globals, closures, object state
or native internals. Explicit scientific inputs/settings remain essential. Changed exact
implementations reject consumption; method withdrawal/deprecation also blocks old intent.

Recipes declare `with runtime.step(id)` in order. A step may repeat a positive bounded
number of times. Conditional steps require a pinned condition checker via
`runtime.branch(id, outputs=...)`; pass enters its boundary, fail records a skip,
unknown abstains. Calls cannot silently omit steps or swallow a failed boundary.
`context.cancelled` is inspected at declared boundaries; it cannot preempt an opaque
solver or undo completed effects. Broad adaptive/unbounded workflows and parallel/DAG
scheduling are not implemented.

A `Step(kind="capability", child_capability_ref=...)` is invoked through
`runtime.invoke(id, inputs, configuration=..., protocol_ref=..., binding_ref=...)`.
The parent retains catalog candidates and implementation/checker identities throughout
reachable child procedures. Children get their own prepared/attempt records, parent/child
links, selection and checks; unsupported child results cannot support the parent. New
candidates cannot enter old intent. Recursion and excessive depth are prohibited.
These local method records are provisional; they are not another authoritative project
Run or ExecutionPlan. The shared invocation/transaction seam remains
[MOLI #28](https://github.com/uibcdf/moli/issues/28).

## Audit, reporting and replay

`audit_definition`, `audit_execution`, `audit_benchmark` independently inspect definitions
and saved evidence without invoking scientific recipes/evaluators/checkers. They return
consistent/violated/unverified with structured issues. Consistency is not scientific
validation. Execution audits include ordered/repeated/conditional boundaries, structural
values, consumed identities, scoped checks and child relationships. Benchmark audits
check the full schedule, method links and measurement types/units/configuration.

`describe_method`, `execution_document`, `benchmark_document`, `comparison_document`
and `audit_document` derive source-linked documents; `render` writes Markdown or escaped
HTML without computation. Protocol documentation includes its common Capability contract,
checks, typed parameters, resources, tradeoffs and review/assessment history. Comparison
requires one Capability and an explicit scenario; evidence basis, alternatives, conflicts
and unknown resource judgments remain visible. The caller controls disclosure/access.

`trace_execution(id, records=...)` reconstructs retained parent/child intent offline.
`replay_preflight` checks exact observed implementations/environment, current method status
and declared availability/provenance preconditions. Changed/missing/unauthorized references
must fail or remain unknown through provider checkers; there is no implicit substitute
or general reference resolver. `replay_execution` makes a **new** `replay_of` attempt;
only an explicitly supplied versioned comparator assesses output equivalence and its
finding is retained separately. It repeats neither human judgment nor physical events.
Checkers used for availability inspection must obey the provider's read-only contract.
Replay is local fresh execution, not generic Recorda replay or distributed recovery.

## Benchmarks and reanalysis

`BenchmarkSpec` records exact cases/scenarios/inputs, Protocol/binding configurations,
replicates, evaluator identity/configuration, declared comparison basis/limitations and
optional per-replicate seeds with a named scientific parameter. Seeds never overwrite
method configuration; records show supplied control, not proof an opaque engine used it.
A legacy evaluator returns a finite dimensionless scalar. Declared `MetricDefinition`
objects support a named metric vector with meaning/direction and physical unit/semantic
field. The vector must match exactly; invalid/missing measurements are evaluator failures,
not zero values, engine failures or scientific judgments.

`run_benchmark` uses ordinary preparation/execution and saves the full schedule before
work, plus immutable per-row checkpoints. Evaluator implementation, environment,
configuration, inputs/attempt links, timing, recording references and failures are retained.
Computed metrics persist before operation-output recording; later recording failure does
not erase them. Blocked, failed, interrupted and unstarted rows remain in the denominator.
`load_benchmark` reopens results or partial progress offline; it does not resume computation.

`reanalyze_benchmark(source_id, new_spec, ...)` preserves original sample, methods,
configurations, cases, replicates and seeds, checks source consistency, and evaluates
saved supported outputs with a new immutable analysis identity. No scientific method runs.
Original analysis remains retrievable. Evaluator/recording failures and interruptions retain
checkpoints just as in the original run.

`summarize_benchmark` provides per-case/method means and sample standard deviations,
available/missing/planned counts, physical units and measured durations. It states its
arithmetic scope, provides no independence assumption/confidence interval, and does not
rank protocols. Method durations include preparation/initial checkpoints/recording and
failure inspection; evaluation has a separate interval. No warm-up is removed; native
caches and missing hardware observations limit performance comparisons. Rich statistical
or scientific evaluation belongs to explicitly versioned evaluator extensions.

## Recorda and Ackredit

Recorda records **what happened and when**, with application-owned sessions. Praxis
supplies semantic method snapshots and correlates observed method/step/evaluator boundaries.
Pass `RecordaRecorder(session)` as `context.recorder`; Praxis never starts/stops that session.
Excluded capture policies and recording gaps stay visible. Coverage concerns declared
boundaries only, not provider internals, replay or distributed durability.

Set `context.attribution=True` inside an application-owned Ackredit session to retain its
portable attribution, including partial failures. Providers credit branches actually used;
Praxis neither credits candidate bibliography merely by reading it nor infers contributions.
There is no automatic Recorda-to-attribution evidence bridge.

## Scientific exercises and development

`examples/local_comparison.py` remains a fictional dimensionless regression fixture.
`examples/molsysmt_comparison.py DIRECTORY LOCAL_PDB` uses actual public MolSysMT parsing,
selection, fixed-frame RMSD and optimal-superposition RMSD. It saves quantities, source
content digest/correspondence, provider revision, benchmark, audit and reports. Identical,
controlled 1 nm translation and incompatible-quantity cases exercise two distinct
observables; they are not ranked as interchangeable or scientifically validated. Optional
qualification test `tests/test_real_provider.py` needs MolSysMT and its packaged 1vii PDB.

The [hydrogen Capability and two filled Protocol proposals](proposals/hydrogen_refinement/capability.md)
and [technical review](proposals/hydrogen_refinement/review.md) exercise the actual templates.
`Catalog.load_bundled(version="2")` registers strengthened experimental definitions;
version 1 stays unchanged. No hydrogen binding is executable: provider operations,
model/coverage decisions, scientific review and throughout proof remain pending under
[MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323).

Provision `devtools/conda-envs/development_env.yaml`, then use
`python -m pip install --no-deps --no-build-isolation --editable .`. Routine Python is 3.14;
metadata admits 3.11–3.14. `devtools/check_dependencies.py` verifies classified environment,
candidate Conda recipe and CI constraints, with negative conformance tests.
`devtools/moli_governance.py` checks the restored existing component governance surface.
The noarch candidate recipe is built without upload; the 0.1.0 release plan lives in
[the candidate record](releases/0.1.0.md). Public distribution needs its own decision.
Configured Linux/macOS lanes require actual remote installed-artifact qualification before
support/publication claims. See [remaining external decisions](IMPLEMENTATION_CHECKPOINT.md).
