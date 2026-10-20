# Capability proposal: Infer a half-normalized-response crossing from concentration series

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **what scientific task can be performed and what fulfilling it means**.

## 1. Proposal and responsibility

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Proposed maintainer(s): Pending scientific review and provider ownership agreement.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Proposed change: New hypothetical experimental Capability.
- Definition reference/version: stress:half-response-crossing@draft-1
- Related definitions and compatibility: Composes the normalization Capability; fitting numerical routines and assay data remain provider-owned. This does not define ligand affinity or project Evidence.

## 2. Scientific intent and need — minimum content

Estimate where a declared increasing concentration-response model crosses normalized response 0.5 within the observed concentration domain. For example, compare model-dependent assay summaries while retaining normalization and ambiguity.

## 3. Common contract — minimum content

| Input | Scientific meaning | Required information and constraints |
| --- | --- | --- |
| Assay series | Raw endpoint readings, positive concentrations and control context | Immutable assay snapshot, concentration unit, well/sample mapping and declared batch |
| Method constraints | Explicit normalization child choice and crossing/model scope | Exact child Protocol/policy, QC context and observed concentration domain |

| Output | Scientific meaning | Expected guarantees |
| --- | --- | --- |
| Curve representation | Declared increasing fitted/interpolated normalized response | Model, source mapping, child normalization reference and residuals retained |
| Crossing result | Concentration point, identified crossing interval or unbracketed/inconclusive finding | Concentration unit; no silent extrapolation or unique-point claim for a plateau |
| Method report | Parent/child checks, assumptions and termination | Model-dependent inference distinguished from established potency/biological mechanism |

- Invariants: Raw measurements and concentration identities unchanged; child contract preserved; crossing remains in observed domain.
- Authorized changes: Produce derived normalization, curves and crossing summaries; no editing assay data or control decisions.
- Successful fulfillment: Supported model and in-domain crossing point/interval, or explicit unsupported/unbracketed/inconclusive result. An interval of exact curve crossings is not a statistical confidence interval.
- Exclusions: Unstated extrapolation, affinity/mechanism inference, hiding nonconvergence, automatic ranking by crossing concentration and physical experiment replay.
- Input preservation and effects: Retain parent inputs and child acquisition/mask/normalization references. Human review effects, if selected, persist even if subsequent fitting fails.

## 4. Applicability and limitations

- Common preconditions: Positive finite concentrations and explicit units/mapping; increasing response interpretation declared; child normalization can satisfy its own contract.
- Scope: Endpoint concentration series; observed-domain increasing models with their explicit additional assumptions.
- Unsupported or excluded cases: Nonpositive concentrations, missing control contrast or no supported child normalization.
- Undetermined cases: Suitability of the increasing model, unresolved child QC or solver compatibility; selection can abstain.
- Limitations and uncertainty: Different models and normalization choices can yield different crossings; fitted residual alone is not scientific validity.

## 5. Candidate Protocols, selection, and provider needs

| Procedure/reference | Proposed relationship to the contract | Definition and validation status | Implementation status and outstanding work |
| --- | --- | --- | --- |
| [Normalized bounded sigmoid fit with an observed-domain crossing](response_sigmoid_protocol.md) | Adds a smooth two-parameter increasing model and calls an explicitly selected normalization child. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |
| [Monotone regression with piecewise log-concentration crossing](response_monotone_protocol.md) | Uses an explicitly selected normalization child and a monotone fitted curve with point/plateau outcomes. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |

- Selection between Protocols: Explicit sigmoid model or monotone piecewise interpolation. Child normalization selection is separately pinned and recorded before execution.
- Non-selection outcomes: Too few concentrations for the sigmoid method is scientific restriction; a missing optimizer is operational availability; unresolved reviewed controls block the chosen child.
- Selection record requirements: Preserve exact provisional definitions and eventual retained revisions, constraints, findings, actor/policy, selected Protocol and binding, and reasons for every excluded candidate.
- Scenario-dependent suitability: Smooth-model inference and flexible monotone interpolation address different assumptions. Favorable scenarios are hypotheses requiring scoped evaluation; no lower-crossing universal winner.

## 6. Evaluation, maturity, and evidence

- Proposed maturity/validation status and scope: Experimental design fixture; admission and validation pending.
- Evidence already available: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Synthetic known crossing, insufficient points, flat 0.5 plateau, unbracketed domain, child contrast failure, pending human review and normalization-basis mismatch.
- Acceptance criteria: Traceable nested method choice, unit-correct in-domain crossing or honest ambiguity, original-data preservation and explicit model/normalization basis.
- Outstanding questions: Nested request/binding interface (#6), scoped model recommendations (#7), comparable benchmark basis and evaluator failures (#8).

## 7. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Not scientifically reviewed; structural exercise uses local draft-1 on 2026-10-07.
- Outcome: Pending; the design walkthrough does not admit or validate a method.
- Rationale, scope, and conditions: Scientific substance, provider compatibility and measured utility require independent review.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
