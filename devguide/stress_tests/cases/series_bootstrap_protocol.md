# Protocol proposal: Fixed circular block bootstrap percentile interval

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:series-mean-uncertainty@draft-1](series_capability.md)
- Protocol reference/version: stress:circular-block-bootstrap@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Retains the same source mean and adds a stochastic empirical interval under declared block-resampling assumptions.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed resampling construction for an uncertainty interval; empirical performance remains to be assessed under known generators.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: For each of R replicates select ceiling(N/b) independent uniform start indices from 0 through N-1, copy b consecutive values with circular wrapping, and truncate the derived sample to N. Compute replicate means. Sort them; use nearest-rank 0.025 and 0.975 quantiles for the proposed nominal 95 percent interval.
- Model assumptions and coverage: Declared stationarity and suitability of circular block resampling at b; circular wrapping and chosen block length are explicit assumptions, not corrections of a nonstationary input.
- Comparability of outputs: Same source segment, mean target and nominal confidence level. Coverage and width are evaluated together; narrower is not automatically better.

## 3. Contract compatibility and applicability

- Additional input/output requirements: N at least 2b, finite uniformly sampled values; R at least 1000. Exact random-number implementation is resolved and retained before execution.
- Additional preconditions and scope: b and R fixed before resampling; mandatory sampling justification and actual PRNG revision/seed available.
- Invariant enforcement: Original series snapshots remain read-only; circular resamples and their index lineage are derived outputs. Independently check source mean, units, index bounds and sample counts.
- Applicable: Input-size and assumption findings pass for the declared segment and block length.
- Inapplicable: Source too short for declared b or circular-wrap assumptions known to be inappropriate.
- Undetermined: Resampling assumptions or random-number implementation unresolved; scientific unknowns and implementation unavailability remain separate.
- Limitations: Finite-resample Monte Carlo variation and source/block assumptions. Additional replicates do not fix insufficient sampling.
- Advantages and disadvantages: Proposed advantage versus normal block-mean interval: a separately defined empirical interval construction. Disadvantages: stochastic variation, additional compute and dependence on block/wrap choices; measured calibration unknown.
- Favorable and discouraged scenarios: Proposed for justified circular-block resampling and available compute; discouraged when wrap or stationarity assumptions are unsuitable.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| R1 | Check segment, b, R, PRNG and sampling assumptions | Snapshots and explicit configuration | Readiness findings | Statistical provider/reviewer pending |
| R2 | Generate R separately identified derived resamples and means | R1-supported configuration and seed | Replicate table and random-stream record | Versioned resampling provider pending |
| R3 | Compute nearest-rank endpoints and report original mean | R2 and original retained data | Conditional interval, source mean and diagnostics | Statistical evaluator/checker pending |

- Internal branches and selection rules: Every circular index is explicit in derived provenance; no adaptive replicate stopping or hidden seed retries.
- Human judgment, if required: An authorized scientist may supply the contract-permitted sampling declaration; that statement and its limitations are retained.
- Step evidence and effects: Derived statistical outputs only. Provider statements and independent arithmetic checks have separate evidence scopes.
- Termination and convergence: Exactly R replicates unless failed/cancelled; partial replicate count is not reported as the specified completed evaluation.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| b | Samples per circular block | Explicit input; scenario uses 8 | Positive with N at least 2b |
| R | Derived replicate count | Explicit 1000 in scenario | At least 1000 |
| seed and PRNG | Random stream identity | Seed 17 in scenario; PRNG/binding revision mandatory at launch | Explicit identity retained; no session default |

- Reproducibility controls: Retain PRNG identity/revision, seed, index stream or reconstructible stream specification, b, R and evaluator. Different random-stream implementations are not assumed bitwise replay-compatible.
- Variant boundary: Predeclared b, R and seed vary within this procedure; adaptive stopping or another interval construction revises it.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Circular resampling, PRNG and percentile evaluation | Statistical scientific provider, owner pending | No verified fixture binding | #5/#6 | Index/wrap/quantile rules, random stream identity and source preservation |
| Sampling assessment | Authorized scientist/provider | Scenario-specific, not assumed | #5/#7 | Resampling assumptions, scope and actor recorded |

- Software environment: Numerical binding and quantity representation resolved at launch; no installed statistical library is claimed.
- Resources: Finite N source values and R replicate means; retaining all derived indices/resamples needs an explicit storage policy. Measured costs unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Verify index wrapping, derived sample length, source immutability, quantile ranks and replay criteria for the actual random-number binding.
- Implementations and binding choice: External statistical/PRNG bindings pending; seed equality alone is insufficient compatibility evidence.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Segment/size/units before computation | Mandatory | Versioned checker and snapshot | Block failed/unknown |
| Sampling assumption and b justification | Mandatory | Permitted reviewer/provider declaration with scope | Unknown blocks supported interval |
| Mean/units/count after computation | Mandatory | Independent arithmetic checks | Violation prevents compliant completion |

- Input and pre-execution checks: R1 checks N at least 2b, R at least 1000, units, segment, sampling justification and exact PRNG/seed; the other Protocol's eight-block/divisibility rule does not apply.
- Output checks: Mean and interval units, source sample count, finite arithmetic, and explicit uncertainty limitations.
- Actual changes: Produce estimates, diagnostics and explicitly derived resamples; never rewrite the original trajectory. A constant estimate can be valid but zero estimated uncertainty needs its stated conditional basis.
- Outcome distinctions: Completed conditional estimate; inconclusive uncertainty; blocked prerequisites; partial replicates on failure/cancellation.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Also retain the random stream, per-replicate identity and actual R, quantile rule and source-versus-derived lineage.
- Output ownership: Statistical provider owns estimates/diagnostics; Praxis records method-specific requirements and assessment references.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Controlled synthetic stationary and nonstationary cases, correlation regimes, constant series and short series; test interval coverage only over declared replicated generators.
- Evaluation criteria and comparison basis: Coverage, width and bias across separately declared synthetic generators; no width-only ranking.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
