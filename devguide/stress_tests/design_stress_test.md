# Praxis design stress exercise

Four hypothetical Capabilities and eight Protocols exercise the
[programming design](../pending_proposals/initial_implementation_design.md) and
[proposal templates](../templates/README.md). The templates can express all four
cases after the revision-2 additions. The package responsibilities can accommodate
them, while executable schemas, bindings, human-step lifecycle and assessment
queries still require the decisions tracked in Praxis #5–#8.

This is a design simulation dated 2026-10-07. The filled proposals and walkthroughs
describe expected behavior under synthetic inputs and injected findings. No Praxis
runner, scientific provider or scientific-validation benchmark was executed.
The interface questions below describe that historical design state. The
[0.1.0 release record](../releases/0.1.0.md#issue-acceptance-and-remaining-work)
now records fulfilled local criteria for #4, #7 and #8 and implemented local
contract/request interfaces for #5/#6. Shared lifecycle ownership and the actual
scientific providers remain pending; these eight proposed methods have not been
executed or scientifically validated by the later local release qualification.
The small analytic reference values below check fixture arithmetic, not numerical
solver implementations or statistical calibration. Provisional `stress:` labels
identify local examples; they are not admitted immutable catalog identities.

## Method inventory

| Capability | Protocols | Stress on the design |
| --- | --- | --- |
| [Paired rigid geometry comparison](cases/geometry_capability.md) | [All-pair weighted fit](cases/geometry_full_protocol.md); [deterministic trimmed fit](cases/geometry_trimmed_protocol.md) | Read-only arrays, correspondence, quantities, different objectives, bounded iteration, multiple bindings and invariant evidence. |
| [Series mean and conditional uncertainty](cases/series_capability.md) | [Block means and approximate interval](cases/series_block_means_protocol.md); [circular block bootstrap](cases/series_bootstrap_protocol.md) | Sampling assumptions, random streams, derived replicates, cancellation and statistical uncertainty. |
| [Assay control normalization](cases/normalization_capability.md) | [Preapproved control means](cases/normalization_automatic_protocol.md); [reviewed controls and normalization](cases/normalization_reviewed_protocol.md) | Table lineage, external acquisition references, human authority, waiting steps, retained decisions and unrepeatable physical observations. |
| [Half-response crossing](cases/response_capability.md) | [Bounded sigmoid fit](cases/response_sigmoid_protocol.md); [monotone regression/interpolation](cases/response_monotone_protocol.md) | Child Capability calls, normalization selection, solver limits, unit-bearing point/interval outputs and model comparability. |

Each Capability uses all seven form sections; each Protocol uses all nine.
The examples retain substantive input/output contracts, procedure/model choices,
parameters, requirements, checks, actual evidence status and pending review.
Unknown implementations are justified in the execution fields rather than hidden
in the scientific procedure. Proposed advantages and disadvantages have explicit
conditions and are not presented as measured results.

## Registration and selection walkthrough

Register the four Capability definitions and eight Protocol definitions as
experimental proposals, preserving the exact local content used for the exercise.
No registration requires importing a geometry engine, statistical package, assay
instrument or Nextia. A missing scientific binding leaves execution unavailable
but does not erase an otherwise meaningful methodological definition.

The catalog links each Protocol to its target Capability and exposes requirements,
assumptions, scenario-dependent tradeoffs and lack of scientific assessment.
A request records its scientific purpose and constraints; discovery can return
several candidates without selecting one. Explicit choices or versioned policies
resolve the Protocol and its binding separately.

For the composed crossing methods, preparation pins the normalization Capability,
candidate child Protocol references, choice/policy and permitted QC authority.
The child invocation preserves the actually selected Protocol/binding and its
parent relationship. A human outcome or an intermediate numerical result need
not exist before the overall method starts; their checks gate the dependent
phase. A later catalog change cannot alter the recorded historical selection.

## Scenario walkthroughs

| Scenario | Inputs or injected finding | Expected consequence |
| --- | --- | --- |
| G1 proper fit | Four noncoplanar points B = A + (2, 3, 4) angstrom; fixed identity mapping and unit weights. | Identity rotation and that translation give zero full residual. Both Protocols retain every pair in the report; trimming additionally retains its actual fitted subset/history. |
| G2 ambiguous geometry | All selected fitting points are collinear and the request requires a unique transform. | A mandatory identifiability finding blocks the unsupported claim. No arbitrary unique rotation or substitute matching method. |
| G3 reflection and trimming limit | A mirrored input or an injected trimmed-subset cycle. | Mirrored inputs can still be compared by proper motion with residuals; reflection is never authorized. A cycle/budget stops trimming as unconverged, preserving the last fitted subset, not an unfitted candidate. |
| T1 unresolved sampling | N = 64, b = 8; sampling/equilibration justification is absent. | Arithmetic size is sufficient for block means, but the mandatory scientific assumption remains unknown. No supported uncertainty interval; any authorized exploratory estimate retains that limitation. |
| T2 cancelled resampling | Block-bootstrap configuration requests R = 1000 with a resolved synthetic stream; cancellation occurs after 412 replicates. | Keep source data, partial derived results, actual count and cancelled attempt. Do not label 412 replicates as completed R = 1000. A retry has its own identity and explicit stream configuration. |
| T3 seed without compatible stream | A historical seed is reused with another PRNG/binding revision. | Seed equality does not establish bitwise replay compatibility. Retain the historical revision; any supported substitution is explicit and output-comparison criteria remain conditional. |
| N1 automatic normalization | Three low controls at 0, three high controls at 100, threshold 1 signal unit; assay readings 0, 50, 100, 120. | Anchors 0 and 100 yield responses 0, 0.5, 1 and 1.2 with unchanged source IDs. No clamping of 1.2. |
| N2 inadequate contrast | Both control anchors are 10 signal units. | Contrast fails before division. Preserve unsupported normalization and its inputs; do not invent a response or biological conclusion. |
| N3 human review | Four eligible high controls, one documented instrument-invalid flag; permitted reviewer has not yet responded. | Start only with supported authority/evidence, then wait. An explicit supported exclusion retains three controls and permits dependent arithmetic. Unflagged or desired-response exclusions are rejected; timeout supplies no decision. |
| C1 reference sigmoid | Concentrations 1, 3, 10, 30, 100 micromolar; prescribed reference model m = 1, s = 2 in log10(c / 1 micromolar), with a common normalized table. | Reference crossing is 10 micromolar. A real fitted point still requires actual convergence and domain evidence; the analytic reference does not supply it. |
| C2 plateau crossing | Concentrations 1, 3, 10, 30, 100 micromolar and already monotone responses 0.1, 0.5, 0.5, 0.5, 0.9. | Piecewise model identifies crossing interval 3–30 micromolar. Do not report an arbitrary unique midpoint or call this a statistical confidence interval. |
| C3 failed child or changed basis | Child normalization has inadequate contrast, or two compared parent methods use different retained-control masks. | A failed child prevents fitting a supported parent result. Different masks remain different normalization bases and cannot silently support a model-only comparison. |
| B1 evaluator failure | Geometry benchmark plans three cases per Protocol: translated, degenerate and an outlier fixture. Inject one evaluator error after a completed full-fit method. | Distinguish method completion, blocked case and unavailable metric. Keep planned/eligible/executed/measured denominators; no zero-score substitution or automatic validation. |
| R1 recording gap | Provider computation returns but required record linkage cannot persist. | Operational result and recording completeness differ. Strict scope cannot claim complete durable commitment; recovery adds history and does not pretend the gap never occurred. |
| A1 conflicting assessment | Later reviewers disagree on a Protocol's usefulness for the same proposed scenario. | Retain both exact assessments and their scope. A new suitability revision cannot rewrite the historical Protocol or turn a benchmark score into validation. Query/projection policy remains an explicit decision in #7. |

These findings are scenario expectations, not observations from running the future
Praxis package. Unsupported, inconclusive and cancelled outcomes remain legitimate
recorded outcomes; they do not imply fulfillment of every requested scientific
guarantee.

## Complete composed-method trace

The monotone crossing Protocol can explicitly select reviewed normalization.
The following synthetic trace exposes the relationships the implementation must
preserve, including a retained human decision followed by parent failure.

| Record or step | Preserved relationship | Simulated outcome |
| --- | --- | --- |
| Parent request and selection | Crossing Capability, monotone Protocol, explicit child reviewed-normalization choice and exact provisional revisions. | No hidden change to automatic normalization. |
| Prepared parent invocation | Raw assay snapshot, concentrations/units, grouping, QC criteria, reviewer scope, child candidates and selected implementation requirements. | Upfront requirements supported; decision-dependent checks deferred to their declared phase. |
| Parent attempt and M1 | One attempt references the preparation and opens a child invocation. | Running; parent fitting has not started. |
| Child preparation and attempt | Normalization Capability/Protocol, parent reference, raw/mask snapshots and permitted reviewer/evidence. | Human-step prerequisites supported. |
| H1 and H2 | Request, actor/authority, incident evidence and decision relationship. | Waiting until an explicit synthetic reviewer response; no elapsed-time consent. |
| H2 completion | Retained original and revised control masks, accepted exclusion and rationale. | Supported review decision; remains historical even if a later step fails. |
| H3 and child completion | Anchor computation, contrast finding, normalized output reference and independent mapping/arithmetic checks. | Conditional contract-supported child result, with its own recording state. |
| Parent M2/M3 | Consumes the exact child output; preserves grouping, curve model and numerical checker identities. | Injected provider error interrupts parent inference; child output/review are retained. |
| Parent termination | Links failure, actual completed steps and available child/partial outputs. | No completed parent crossing or automatic rollback of the review. |
| New retry preparation/attempt | Explicitly chooses either retained child output under supported reuse rules or a new child invocation. | Separate identity; no unrecorded new review or silent continuation. |
| Audit and rendering | Read the preserved method/child/decision/output records and their evidence coverage. | Explain failure and supported child guarantees; create no project Evidence or new computation. |

The trace requires identified child steps and human waiting/cancellation semantics.
Those fit the proposed boundaries, but they are later execution capabilities;
the first catalog increment cannot execute this trace merely by storing its form.

## Benchmark and reporting exercise

The geometry benchmark specification fixes all-pair mapping/weights/units,
Protocol and binding revisions, three cases, checker/evaluator versions and a
common full-residual metric. It reports subset loss separately for trimmed fits.
Resource measurement states environment, warm-up and included preparation,
execution/checking/recording boundaries; no runtime or memory measurements are
invented for this design simulation.

In B1, each Protocol has three planned cases, two eligible/executed cases and one
scientifically unsupported case. The injected metric error leaves one available
measurement for full fitting and two for trimming. Report measurement availability
as both 1/2 versus 2/2 of executed cases and 1/3 versus 2/3 of planned cases. The
paired quality comparison has only the one shared measured case. Preserve the
missing outlier measurement rather than awarding a default score or attributing
an evaluator error to the fitted method. These counts follow the injected scenario,
not an executed benchmark.

A new analysis using a different evaluator revision links to the same preserved
method outputs and receives a new analysis identity. Rendering references the
chosen analysis and its source snapshots; it does not rerun the evaluator.
Scenario-dependent advantages can be proposed from these results only within their
basis and limitations, with scientific assessment and conflicting evidence visible.

For concentration-response comparisons, use the same normalized child output or
explicitly report that the entire composite pipeline differs. For time-series
interval comparisons, report coverage and width jointly under specified synthetic
generators; a narrow interval alone is not a favorable scientific verdict.

The exercise requires Capability/Protocol documentation, a selection comparison,
an execution report, an audit report and a benchmark report. Each has stable
source references after actual registration, versions, conditions, findings,
unknowns and disclosure scope. Nextia can subsequently interpret appropriate
references through an explicit project operation.

## Template findings

| Finding | Revision-2 response | Remaining limit |
| --- | --- | --- |
| Advantages/disadvantages and applicable-but-discouraged scenarios were implicit. | Dedicated Protocol fields and Capability suitability guidance identify conditions, alternatives and evidence strength. | Queryable claim/assessment representation remains #7. |
| Mandatory checks could remain narrative with unclear unknown/error handling. | Check table specifies phase, role, evidence scope and failure/indeterminate response. | Executable schema and gates remain #5. |
| Multiple implementations were not explicit. | Binding-choice field records compatibility and explicit selection. | Public request/binding interface remains #6. |
| Live inputs, human/external effects and audit coverage needed clearer declarations. | Input-preservation and step-evidence/effects fields retain snapshots, actors and limits. | Runtime instrumentation and human-step lifecycle remain #5/#6. |
| Stochastic and model-dependent outputs require distinct meanings. | Existing parameters, reproducibility, model/comparability and outcome fields can express the examples without molecular-only assumptions. | Concrete domain value/reference codecs and comparison rules need implementation review. |

All four Capabilities and eight Protocols can now be meaningfully submitted using
the forms. Human/assay steps need descriptive responsibility and evidence rather
than a compulsory software-engine name. A benchmark proposal still needs its own
specification; the Capability/Protocol evaluation sections link to it instead of
pretending to define its full execution and analysis lifecycle. Authoring support
for that specification is included in #8.

The walkthrough also exposed three consistency errors in the first filled drafts:
a reflected input was confused with permission to reflect, the bootstrap copy
retained another Protocol's block-count condition, and trimmed checks referred
to another procedure's step IDs. They were corrected. This demonstrates why
template completeness must be followed by substantive contract review.

## Structure findings

| Proposed responsibility | Fit in this exercise | Implementation obligation |
| --- | --- | --- |
| Definitions and catalog | All tasks retain independent intent, contracts, versions and unresolved implementations. | Semantic descriptors must support arrays, tables, quantities, assumptions and tagged point/interval/inconclusive results. |
| Applicability and selection | Different scientific restrictions, resource constraints and favorable scenarios remain separate. | Typed findings, abstention and scoped evidence queries; no hidden fallback. |
| Extensions and bindings | Geometry, statistical, assay, random-number, checker and metric roles fit external interfaces. | Compatible bindings and their actual versions need deterministic resolution and evidence. |
| Steps and runner | Fits, bounded trimming, resampling replicates, human decisions and child calls have identifiable relationships. | Phase-aware gates, waiting/cancellation, child correlation and partial-output handling; several features follow the first sequential runner. |
| Recording and audit | Definitions, actual intent/steps, external data and decision records retain their sources. | Historical snapshots, source/evidence coverage and Recorda integration; opaque-engine declarations cannot prove unobserved operations. |
| Benchmarks and reporting | Quality, coverage, model differences, unknown metrics and proposed tradeoffs remain expressible. | Evaluator records, honest denominators and derived report schemas. |

The proposed module responsibilities accommodate the four cases without requiring
one engine-specific class hierarchy per Capability or numerical algorithms in
Praxis core. This is a representational conclusion: runtime support depends on
the interfaces and guarantees still open below. The exercise supports proceeding
with a small catalog/documentation increment and using these cases as later
acceptance fixtures, rather than treating every planned runner feature as ready.

## Follow-up decisions

- [Praxis #5](https://github.com/uibcdf/praxis/issues/5): executable contracts,
  checker evidence/authority and phase/lifecycle gates.
- [Praxis #6](https://github.com/uibcdf/praxis/issues/6): requests, choices/bindings,
  preparation, nested invocation and authoritative record boundaries.
- [Praxis #7](https://github.com/uibcdf/praxis/issues/7): scoped assessments,
  suitability statements and conflicting history/status queries.
- [Praxis #8](https://github.com/uibcdf/praxis/issues/8): benchmark/evaluator records,
  comparison/resource conventions and derived reports.

Shared execution ownership remains under
[MOLI #28](https://github.com/uibcdf/moli/issues/28). These new examples supplement
the generic fixture of #1. The filled hydrogen proposals and substantive scientific
review requested in #4 remain separate follow-up work.
