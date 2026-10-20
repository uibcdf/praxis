# Protocol proposal: Normalized bounded sigmoid fit with an observed-domain crossing

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:half-response-crossing@draft-1](response_capability.md)
- Protocol reference/version: stress:response-sigmoid@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Adds a smooth two-parameter increasing model and calls an explicitly selected normalization child.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed restricted smooth model for a half-response summary; model appropriateness needs scientific assessment.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: x = log10(c/c_ref), with c_ref = 1 in the declared concentration unit. y_hat = 1/(1 + exp(-s times (x-m))). Fit sum of squared residuals, s between 0.1 and 10. Crossing c_ref times 10**m is reportable only within the observed domain.
- Model assumptions and coverage: Increasing response, zero/one normalization anchors and this fixed-asymptote sigmoid are appropriate. Response values may be outside zero to one; they are not clamped.
- Comparability of outputs: Use identical raw data and exact child normalization/mask to isolate model differences. Different children or reviewed masks create a different comparison basis.

## 3. Contract compatibility and applicability

- Additional input/output requirements: At least five distinct positive concentrations; normalized mapping preserved. Exact optimizer/binding resolved before launch.
- Additional preconditions and scope: Child normalization readiness and sigmoid-model suitability findings pass; source domain declared.
- Invariant enforcement: Child invocation has its own checks/evidence and parent correlation. Provider fit operates on derived snapshots; independently verify in-domain crossing and mapping.
- Applicable: Supported child, sufficient distinct points and explicit evidence for the model assumptions.
- Inapplicable: Insufficient distinct concentrations or a known inappropriate fixed-asymptote/increasing model.
- Undetermined: Child QC pending, model suitability unresolved or numerical binding unverified; hold preparation or the affected child step.
- Limitations: Optimization may fail; a low residual does not validate the sigmoid or prove potency. This fixture does not compute statistical crossing uncertainty.
- Advantages and disadvantages: Proposed advantage versus piecewise monotone interpolation: a compact smooth curve under stronger assumptions. Disadvantages: model restrictions and solver dependence; scientific benefit is unmeasured.
- Favorable and discouraged scenarios: Proposed when the fixed-asymptote model has support and a smooth summary is useful; discouraged when the assay shape or anchors contradict that model.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| C1 | Check concentration inputs and invoke normalization Capability | Parent snapshot; explicit child Protocol/binding | Child result or pending/failed outcome | Praxis composition plus assay provider pending |
| C2 | Fit declared sigmoid from nine prescribed starts | C1 derived response; m at domain minimum/midpoint/maximum, s at 0.5/1/2 | Converged candidates and residuals | Scientific nonlinear-fit provider pending |
| C3 | Choose candidate and inspect crossing domain | C2 supported converged fits | Point crossing or unbracketed/inconclusive finding | Recipe selection and independent curve checker pending |

- Internal branches and selection rules: Child normalization is explicitly selected; the analytic scenario uses arithmetic controls. Choose lowest objective among converged starts; objectives within 1e-10 dimensionless tie by smaller m then s. No converged candidate yields inconclusive; no child failure substitution.
- Human judgment, if required: Model-suitability declaration may need scientific review. A reviewed normalization child requires its own recorded authority/outcome.
- Step evidence and effects: Derived curve/normalization results. Child review effects cannot be rolled back by parent fit cancellation. Known steps are correlated; opaque solver guarantees require provider evidence.
- Termination and convergence: Maximum 1000 iterations per start; provider must meet declared parameter/objective change tolerance 1e-8 and record termination. No best-found/global-optimum claim.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| child selection | Exact normalization Protocol/binding or pinned policy | Explicit input; analytic scenario uses arithmetic controls | Compatible child version and permitted selection only |
| s bounds | Dimensionless slope in log10 concentration | 0.1 through 10 | Changing model bounds requires scientific review |
| starts/budget/tolerance | Numerical procedure | Nine fixed starts; 1000 iterations; 1e-8 convergence, 1e-10 tie tolerance | Declared budget/tolerance variants; different model/start policy revises method |

- Reproducibility controls: Pin child definitions/masks, model, optimizer/binding and starts; record each actual fit and tie decision. c_ref conversion is explicit, making logarithms dimensionless.
- Variant boundary: Declared budgets/tolerances vary with records; free asymptotes, decreasing response or silent child changes revise scientific procedure/configuration as appropriate.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Normalization child | Assay provider via Praxis child Capability | Definition fixture exists; verified binding pending | #5/#6 | Child contract/checks and parent mappings |
| Nonlinear fit and independent curve checks | Scientific statistical provider, owner pending | No verified binding | #5/#6 | Model bounds, starts, convergence evidence, mapping and in-domain crossing |

- Software environment: Child/table quantity codec and optimizer numerical revision resolved; exact license/resource availability at preparation.
- Resources: Retained assay data, nine finite fits and optional human review; measured timing/memory/effort unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Composition must preserve child units/mask and parent sample IDs; independently evaluate curve at the reported crossing and retain failed/nonconverged starts.
- Implementations and binding choice: Optimizer/provider implementations need evidence for the declared model, starts and convergence; an alternate binding is recorded explicitly.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Concentrations and model prerequisites | Mandatory | Input checker and permitted model-scope declaration | Block failed/unknown |
| Child normalization contract | Mandatory | Exact child attempt/check findings | Hold pending child; propagate failed guarantee |
| Fit convergence and crossing domain | Mandatory for point claim | Provider termination plus independent evaluation | Return inconclusive/unbracketed; no extrapolated point |

- Input and pre-execution checks: Positive unit-bearing concentrations, at least five unique values, child readiness and model-scope evidence.
- Output checks: Source/child mappings, finite curve parameters, recorded convergence and in-domain point; no clipping or data mutation.
- Actual changes: Produce derived normalization, curves and crossing summaries; no editing assay data or control decisions.
- Outcome distinctions: Completed identified point; unbracketed/inconclusive; pending child review; child/fit failure; cancellation with retained child and candidate results.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Record parent and child selections/attempts, normalization basis, all fitted starts, actual stop rules and crossing status.
- Output ownership: Assay provider owns raw/normalized readings; fitting provider owns curve/crossing Results; Praxis owns composition and methodological evaluation.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Synthetic known crossing, insufficient points, flat 0.5 plateau, unbracketed domain, child contrast failure, pending human review and normalization-basis mismatch.
- Evaluation criteria and comparison basis: Known synthetic crossing and bounds, invariant/mapping compliance, failure coverage and residuals under a common normalization basis; no potency-only ranking.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
