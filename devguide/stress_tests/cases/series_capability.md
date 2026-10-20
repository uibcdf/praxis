# Capability proposal: Estimate a scalar mean and conditional uncertainty from a time series

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **what scientific task can be performed and what fulfilling it means**.

## 1. Proposal and responsibility

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Proposed maintainer(s): Pending scientific review and provider ownership agreement.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Proposed change: New hypothetical experimental Capability.
- Definition reference/version: stress:series-mean-uncertainty@draft-1
- Related definitions and compatibility: A statistical analysis Capability; generating a trajectory or deciding its project relevance is outside its contract.

## 2. Scientific intent and need — minimum content

Estimate the arithmetic mean of a declared analysis segment and uncertainty under stated sampling assumptions. For example, characterize a scalar observable measured along a simulation without certifying equilibrium from one trace.

## 3. Common contract — minimum content

| Input | Scientific meaning | Required information and constraints |
| --- | --- | --- |
| Series snapshot | Ordered finite scalar observable values and sampling times | Value unit, time unit, sampling interval and explicit retained segment |
| Sampling declaration | Assumptions supporting the analysis target | Stationarity/equilibration and block-choice justification, with responsible actor/evidence |

| Output | Scientific meaning | Expected guarantees |
| --- | --- | --- |
| Estimate | Arithmetic mean of all retained samples | Value unit and exact segment/sample count |
| Uncertainty result | Interval with confidence level and method assumptions, or explicit inconclusive outcome | No fabricated interval when checks or evaluation fail |
| Diagnostics | Analysis configuration, checks and effective block/replicate counts | Input order and original data retained; no silent sample exclusion |

- Invariants: Original values, order, times and segment identity remain unchanged; derived resamples have separate identities.
- Authorized changes: Produce estimates, diagnostics and explicitly derived resamples; never rewrite the original trajectory. A constant estimate can be valid but zero estimated uncertainty needs its stated conditional basis.
- Successful fulfillment: Report the mean and a supported conditional interval, or an explicit inconclusive uncertainty result retaining the available mean and reasons.
- Exclusions: Generating samples, proving equilibrium, turning conditional uncertainty into validated physical truth, and creating Nextia Evidence.
- Input preservation and effects: Retain provider snapshots and segment selection. No input mutation or physical effects.

## 4. Applicability and limitations

- Common preconditions: Finite scalar samples, explicit segment/units and sufficient evidence for each Protocol's mandatory sampling assumptions.
- Scope: Uniformly sampled single scalar series; supported segment and block choice declared before analysis.
- Unsupported or excluded cases: Undeclared irregular sampling, mixed nonconvertible units or missing segment identity.
- Undetermined cases: Stationarity or adequate block length may remain scientifically unresolved; diagnostics alone do not prove either.
- Limitations and uncertainty: Intervals are conditional on sampling/model assumptions; more bootstrap replicates do not create more independent source observations.

## 5. Candidate Protocols, selection, and provider needs

| Procedure/reference | Proposed relationship to the contract | Definition and validation status | Implementation status and outstanding work |
| --- | --- | --- | --- |
| [Fixed nonoverlapping block means with an approximate normal interval](series_block_means_protocol.md) | Produces the common mean and a conditional approximate interval from block means. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |
| [Fixed circular block bootstrap percentile interval](series_bootstrap_protocol.md) | Retains the same source mean and adds a stochastic empirical interval under declared block-resampling assumptions. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |

- Selection between Protocols: Explicit approximate block-mean or block-bootstrap choice, with block length and assumptions. Unknown prerequisites lead to abstention or inconclusive exploratory analysis.
- Non-selection outcomes: Insufficient independent-block justification differs from a missing random-number provider.
- Selection record requirements: Preserve exact provisional definitions and eventual retained revisions, constraints, findings, actor/policy, selected Protocol and binding, and reasons for every excluded candidate.
- Scenario-dependent suitability: A block-mean approximation may be convenient for compact analysis; resampling offers a different empirical interval construction with added computation. These are proposed tradeoffs, not validated coverage claims.

## 6. Evaluation, maturity, and evidence

- Proposed maturity/validation status and scope: Experimental design fixture; admission and validation pending.
- Evidence already available: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Controlled synthetic stationary and nonstationary cases, correlation regimes, constant series and short series; test interval coverage only over declared replicated generators.
- Acceptance criteria: Correct sample mean and units, complete seeds/configuration, no unsupported interval claim; nominal coverage is a separate empirical validation question.
- Outstanding questions: Sampling assumption assessment, random-number compatibility and scoped coverage evidence remain under #5–#8.

## 7. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Not scientifically reviewed; structural exercise uses local draft-1 on 2026-10-07.
- Outcome: Pending; the design walkthrough does not admit or validate a method.
- Rationale, scope, and conditions: Scientific substance, provider compatibility and measured utility require independent review.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
