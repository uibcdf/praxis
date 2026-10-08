# Protocol proposal: Monotone regression with piecewise log-concentration crossing

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:half-response-crossing@draft-1](response_capability.md)
- Protocol reference/version: stress:response-monotone@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Uses an explicitly selected normalization child and a monotone fitted curve with point/plateau outcomes.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed increasing shape-constrained summary without the fixed sigmoid form; scientific value is conditional on the declared monotonicity assumption.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: Group repeated log10 concentration values using arithmetic response means with group counts as weights. Solve weighted squared-error nondecreasing regression. Linearly interpolate fitted responses in log10 concentration between distinct observed points; report every in-domain crossing of 0.5 as a point or contiguous plateau interval.
- Model assumptions and coverage: Increasing response is scientifically appropriate; piecewise interpolation in log10 concentration is explicitly assumed. No extrapolation or sigmoid model.
- Comparability of outputs: Use identical raw data and exact child normalization/mask to isolate model differences. Different children or reviewed masks create a different comparison basis.

## 3. Contract compatibility and applicability

- Additional input/output requirements: At least two distinct positive concentrations and supported normalization child. Provider must resolve monotone regression implementation before use.
- Additional preconditions and scope: Child normalization readiness and increasing-shape suitability findings pass; source domain, grouping and output meanings are declared.
- Invariant enforcement: Child invocation has its own checks/evidence and parent correlation. Provider fit operates on derived snapshots; independently verify in-domain crossing and mapping.
- Applicable: Supported child, sufficient distinct points and explicit evidence for the model assumptions.
- Inapplicable: Fewer than two distinct positive concentrations or a known inappropriate increasing model.
- Undetermined: Child QC pending, model suitability unresolved or numerical binding unverified; hold preparation or the affected child step.
- Limitations: Plateaus can make crossing an interval; group averaging/interpolation are model choices. An interval of curve crossings is not sampling uncertainty.
- Advantages and disadvantages: Proposed advantage versus sigmoid: avoids its fixed smooth shape and represents plateau ambiguity. Disadvantages: interpolation/grouping assumptions and potentially less compact/smooth representation; measured accuracy unknown.
- Favorable and discouraged scenarios: Proposed for justified monotone shape where sigmoid assumptions lack support; discouraged when nonmonotonic response is scientifically relevant.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| M1 | Check inputs and call explicitly selected normalization child | Parent snapshots and child selection | Supported child table or pending/failed outcome | Praxis composition and assay provider pending |
| M2 | Group duplicates and solve weighted monotone regression | M1 normalized responses and positive concentrations | Fitted nondecreasing table with group lineage | Statistical provider pending |
| M3 | Interpolate in log concentration and locate crossing set | M2 fitted points and observed domain | Point, plateau interval or unbracketed result | Curve/checker provider pending |

- Internal branches and selection rules: A reviewed child is allowed only by explicit choice; its pending review holds the dependent calculation. A supported flat fitted segment equal to 0.5 forms a plateau; near-threshold values within tolerance without supported equality are numerically ambiguous, not silently broadened into an exact interval. No arbitrary midpoint is presented as a unique crossing.
- Human judgment, if required: Optional explicitly selected reviewed-normalization child records its own permitted QC decision. Monotonicity suitability needs evidence distinct from that QC approval.
- Step evidence and effects: Derived curve/normalization results. Child review effects cannot be rolled back by parent fit cancellation. Known steps are correlated; opaque solver guarantees require provider evidence.
- Termination and convergence: Finite monotone regression and crossing computation; convergence/feasibility evidence required from provider. No repeated human review to optimize a desired crossing.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| child selection | Exact normalization method/binding | Mandatory explicit input; reviewed child is exercised in one scenario | Compatible references and recorded mask |
| crossing tolerance | Dimensionless response comparison | Explicit 1e-10 in this fixture | Positive and retained; near-threshold values flagged numerically ambiguous |
| log-concentration convention | Dimensionless interpolation coordinate | log10(c / c_ref), c_ref = 1 declared concentration unit | Changing interpolation coordinate revises the method |

- Reproducibility controls: Retain child result, duplicate grouping and weights, provider revision, curve table, tolerance and exact interval status.
- Variant boundary: Declared tolerance/binding choices retain the method; a smoothing penalty, altered grouping rule or extrapolation changes it.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Normalization child | Assay provider via Praxis child Capability | Definition fixture exists; verified binding pending | #5/#6 | Child mask/units/mapping and permitted review evidence |
| Monotone regression and crossing checks | Scientific statistical provider, owner pending | No verified binding | #5/#6 | Grouping weights, monotonicity and exact point/plateau/domain checks |

- Software environment: Resolved child/table quantity codec and monotone-regression numerical binding at launch; no live instrument is needed for report rendering.
- Resources: Retained assay data and one finite grouped monotone solve/crossing computation, plus any explicitly selected human child review; measured costs unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Plateau, exact point and unbracketed fixtures; original duplicate mappings and child decisions retained; no interval-to-point collapse.
- Implementations and binding choice: Explicit monotone-regression and crossing-check bindings need feasibility, grouping and tolerance evidence; a nonlinear sigmoid optimizer is not a compatible replacement.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Concentrations and shape prerequisites | Mandatory | Input checker and permitted scientific scope declaration | Block failed/unknown |
| Child normalization/review | Mandatory | Child attempt/checks and authorized decision where selected | Hold unknown/review-pending; no automatic consent |
| Monotonicity and crossing set | Mandatory for identified crossing claim | Independent fitted-table/domain checks | Inconclusive/violation if unsupported; plateau remains interval |

- Input and pre-execution checks: Positive concentrations, at least two unique values, child readiness and increasing-shape evidence.
- Output checks: Nondecreasing fitted values, mapping/group counts, unit-correct in-domain crossing set and honest plateau status.
- Actual changes: Produce derived normalization, curves and crossing summaries; no editing assay data or control decisions.
- Outcome distinctions: Completed point or plateau interval; unbracketed/inconclusive; pending/rejected child review; failed/cancelled.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Record child review correlation, grouped input lineage, monotone feasibility and crossing-set/ambiguity status.
- Output ownership: Assay provider owns raw/normalized readings; fitting provider owns curve/crossing Results; Praxis owns composition and methodological evaluation.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Synthetic known crossing, insufficient points, flat 0.5 plateau, unbracketed domain, child contrast failure, pending human review and normalization-basis mismatch.
- Evaluation criteria and comparison basis: Compare on identical child normalization and common in-domain crossing criteria; interval-identification and model fit are separate from statistical confidence.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
