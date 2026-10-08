# Protocol proposal: Fixed nonoverlapping block means with an approximate normal interval

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:series-mean-uncertainty@draft-1](series_capability.md)
- Protocol reference/version: stress:block-mean-normal@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Produces the common mean and a conditional approximate interval from block means.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed approximation: summarize sufficiently separated blocks and report the assumptions required for a normal interval; its calibration must be assessed.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: Partition N retained values into K nonoverlapping blocks of length b. Mean is the full-sample mean. Let s_B be sample standard deviation of block means; interval is mean plus/minus 1.96 times s_B/sqrt(K), proposed nominal 95 percent.
- Model assumptions and coverage: Stationary segment, effectively independent block means and adequacy of the interval approximation; human or provider evidence for the declared block length is mandatory.
- Comparability of outputs: Same source segment, mean target and nominal confidence level. Coverage and width are evaluated together; narrower is not automatically better.

## 3. Contract compatibility and applicability

- Additional input/output requirements: Uniform sampling, N divisible by b, at least eight blocks, finite values in one unit.
- Additional preconditions and scope: b declared before analysis; mandatory sampling declaration supports the intended conditional interpretation.
- Invariant enforcement: Read retained snapshots; compute block tables separately. Independently recompute mean/sample count and check units; no automatic burn-in removal.
- Applicable: Input-size and assumption findings pass for the declared segment and block length.
- Inapplicable: Fewer than eight blocks or N not divisible by declared b under this procedure; no silent tail removal.
- Undetermined: Stationarity, block dependence or approximation adequacy lacks required evidence; hold supported-interval readiness.
- Limitations: Approximate conditional interval; block choice and finite source data limit claims. Degenerate block variance does not prove exact physical certainty.
- Advantages and disadvantages: Proposed advantage versus resampling: fewer analysis operations and compact block diagnostics. Disadvantage: specific normal/independent-block approximation. Runtime and coverage comparisons are unmeasured.
- Favorable and discouraged scenarios: Proposed where block assumptions are justified and a compact approximation is useful; discouraged where its conditional model is scientifically inappropriate.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| B1 | Verify segment, units, size and mandatory assumptions | Snapshots and b | Readiness findings | Time-series checker/reviewer pending |
| B2 | Compute all K block means and the original mean | B1-supported segment | Derived block table and mean | Statistical provider operation pending |
| B3 | Compute proposed interval and report diagnostics | B2 and confidence convention | Interval or inconclusive findings | Statistical provider/checker pending |

- Internal branches and selection rules: Unknown assumption cannot be converted into pass by a variance calculation. No tail deletion or hidden block-length adjustment.
- Human judgment, if required: An authorized scientist may supply the contract-permitted sampling declaration; that statement and its limitations are retained.
- Step evidence and effects: Derived statistical outputs only. Provider statements and independent arithmetic checks have separate evidence scopes.
- Termination and convergence: Finite block computation; no adaptive search for a convenient interval width.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| b | Number of samples per block | Explicit input; stress scenario uses 8 | Positive integer; N divisible by b and K at least 8 |
| confidence convention | Dimensionless nominal level | 0.95 with fixed coefficient 1.96 in this fixture | Changing the interval convention revises this procedure |

- Reproducibility controls: Snapshot, segment, b, numerical binding and block table retained; deterministic arithmetic, no random seed.
- Variant boundary: Different predeclared b values are permitted with their evidence; adaptive block selection is a different procedure.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Block and arithmetic operations | Statistical scientific provider, owner pending | No verified fixture binding | #5/#6 | Known means, units, all-sample inclusion and arithmetic checks |
| Sampling assessment | Authorized scientist/provider | Scenario-specific, not assumed | #5/#7 | Scope, rationale and actor recorded |

- Software environment: Numerical binding and quantity representation resolved at launch; no installed statistical library is claimed.
- Resources: Finite N values and K block means; measured memory/runtime unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Check N/b, retained samples and independently recomputed means; assumption findings have their own scope.
- Implementations and binding choice: Numerical/statistical bindings pending; algorithm-compatible implementations need retained evidence and exact revisions.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Segment/size/units before computation | Mandatory | Versioned checker and snapshot | Block failed/unknown |
| Sampling assumption and b justification | Mandatory | Permitted reviewer/provider declaration with scope | Unknown blocks supported interval |
| Mean/units/count after computation | Mandatory | Independent arithmetic checks | Violation prevents compliant completion |

- Input and pre-execution checks: Segment, units, finite values, block count and mandatory sampling declaration.
- Output checks: Mean and interval units, source sample count, finite arithmetic, and explicit uncertainty limitations.
- Actual changes: Produce estimates, diagnostics and explicitly derived resamples; never rewrite the original trajectory. A constant estimate can be valid but zero estimated uncertainty needs its stated conditional basis.
- Outcome distinctions: Completed conditional estimate; inconclusive uncertainty with available mean; blocked assumptions/size; failed/cancelled derived computation.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Sampling declaration, segment boundaries, b, K, block table and interval convention retained.
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
