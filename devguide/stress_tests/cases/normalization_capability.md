# Capability proposal: Normalize assay readings against declared control populations

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **what scientific task can be performed and what fulfilling it means**.

## 1. Proposal and responsibility

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Proposed maintainer(s): Pending scientific review and provider ownership agreement.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Proposed change: New hypothetical experimental Capability.
- Definition reference/version: stress:assay-control-normalization@draft-1
- Related definitions and compatibility: A reusable assay-processing Capability; data acquisition and project interpretation retain their separate owners. Also a child task for concentration-response inference.

## 2. Scientific intent and need — minimum content

Convert endpoint assay readings into dimensionless responses relative to explicitly retained low/high controls. For example, normalize a plate before curve analysis while preserving raw observations and control decisions.

## 3. Common contract — minimum content

| Input | Scientific meaning | Required information and constraints |
| --- | --- | --- |
| Reading/control table | Provider-owned endpoint values, sample/well IDs and fixed low/high labels | One convertible signal unit, immutable acquisition snapshot and initial eligibility mask |
| QC/normalization context | Control eligibility criteria and contrast threshold | Instrument/status observations and permitted reviewer role; threshold has explicit signal unit |

| Output | Scientific meaning | Expected guarantees |
| --- | --- | --- |
| Normalized table | y = (reading minus L)/(H minus L) for each retained assay row | Dimensionless values, original IDs, L/H and retained-control mask; do not silently clamp |
| Control and review report | Anchor estimates, exclusions and evidence | Raw measurements preserved; every exclusion has criterion, source and actor |

- Invariants: Raw values, labels, identities and acquisition provenance remain unchanged throughout; excluded controls remain visible.
- Authorized changes: Create derived responses and an explicit retained-control mask; only controls meeting the declared QC procedure can be excluded. Do not rewrite raw readings or labels.
- Successful fulfillment: Produce normalization with supported anchor contrast and traceable eligibility, or explicit unsupported/inconclusive contrast/review outcome. Values outside zero to one remain valid observations.
- Exclusions: Acquiring or repeating physical measurements, changing assay labels, clamping responses and declaring biological activity.
- Input preservation and effects: Retain acquisition and mask snapshots. A review adds a signed/attributed record and derived mask; it cannot undo an original physical observation.

## 4. Applicability and limitations

- Common preconditions: Finite readings, declared low/high populations, contrast threshold, signal unit and acquisition provenance.
- Scope: Endpoint assays with meaningful low/high controls; plate/batch grouping is explicit and must not be silently pooled.
- Unsupported or excluded cases: Nonconvertible signals, fewer than declared eligible controls or inadequate high-minus-low contrast.
- Undetermined cases: A control instrument flag or reviewer finding may be unavailable; that missing fact cannot become an eligible-control pass.
- Limitations and uncertainty: Normalized response reflects declared controls and eligibility; normalization does not establish assay validity or mechanism.

## 5. Candidate Protocols, selection, and provider needs

| Procedure/reference | Proposed relationship to the contract | Definition and validation status | Implementation status and outstanding work |
| --- | --- | --- | --- |
| [Arithmetic control anchors from a preapproved mask](normalization_automatic_protocol.md) | Uses every control in the supplied verified eligibility mask; preserves raw readings and maps. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |
| [Reviewed control eligibility followed by arithmetic normalization](normalization_reviewed_protocol.md) | Adds an explicit human QC step before the same affine arithmetic, retaining all original controls and exclusion evidence. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |

- Selection between Protocols: Automatic normalization after an already verified mask, or normalization after explicit QC review. A policy cannot silently remove a control because an alternate Protocol gives a preferred response.
- Non-selection outcomes: Unknown QC authority/flag leads to hold/abstention; missing table-processing binding is operational unavailability.
- Selection record requirements: Preserve exact provisional definitions and eventual retained revisions, constraints, findings, actor/policy, selected Protocol and binding, and reasons for every excluded candidate.
- Scenario-dependent suitability: Automation is proposed for preapproved controls; review is proposed when documented instrument events require permitted judgment. Added reviewer effort is a hypothesis about workflow cost, not measured superiority.

## 6. Evaluation, maturity, and evidence

- Proposed maturity/validation status and scope: Experimental design fixture; admission and validation pending.
- Evidence already available: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Analytic anchors, outside-range responses, equal anchors, missing flags, unapproved exclusion and preserved raw data; controlled human-review traces.
- Acceptance criteria: Correct affine arithmetic and mappings, explicit masks/contrast, no clipping or erased exclusions; scientific suitability assessed separately.
- Outstanding questions: Human-step suspension and evidence authority (#5/#6); scoped control-choice comparability (#7/#8).

## 7. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Not scientifically reviewed; structural exercise uses local draft-1 on 2026-10-07.
- Outcome: Pending; the design walkthrough does not admit or validate a method.
- Rationale, scope, and conditions: Scientific substance, provider compatibility and measured utility require independent review.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
