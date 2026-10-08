# Protocol proposal: Reviewed control eligibility followed by arithmetic normalization

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:assay-control-normalization@draft-1](normalization_capability.md)
- Protocol reference/version: stress:assay-reviewed-anchors@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Adds an explicit human QC step before the same affine arithmetic, retaining all original controls and exclusion evidence.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed workflow for documented acquisition/QC events that require permitted human adjudication.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: Same affine control-mean model as automatic normalization, applied to the explicitly approved revised mask; eligibility is a recorded methodological decision.
- Model assumptions and coverage: Declared control populations and eligibility are scientifically meaningful; no implicit plate pooling.
- Comparability of outputs: Compare downstream responses only with identical raw acquisition, control population, retained mask and grouping. Different anchor choices must be reported as differing normalization.

## 3. Contract compatibility and applicability

- Additional input/output requirements: Reviewer can only exclude an initially eligible control with a retained instrument invalid/saturation flag or a documented acquisition incident. No numeric outlier-only or desired-response exclusion.
- Additional preconditions and scope: Review scope/authority declared; at least three retained controls per group after review; threshold rule unchanged.
- Invariant enforcement: Read retained snapshots; derive anchors/mapped outputs without changing raw data. Independent arithmetic, count, threshold and identity checks.
- Applicable: Verified mask, counts, units and contrast pass for every reported batch.
- Inapplicable: Insufficient controls or contrast not above threshold; no fabricated normalization denominator.
- Undetermined: Missing instrument evidence, reviewer authority or response leaves the review step pending. A timeout is not consent.
- Limitations: Human QC judgment is not automatically replayable; different masks imply different normalization bases.
- Advantages and disadvantages: Proposed advantage: records adjudication of permitted acquisition incidents. Disadvantages: reviewer availability/effort and dependence on retained evidence; comparative benefit unknown.
- Favorable and discouraged scenarios: Proposed when a supported incident needs adjudication; discouraged for already approved unambiguous batches where added review supplies no declared benefit.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| H1 | Preserve raw acquisition and present permitted QC evidence | Original mask, incident/flag references and reviewer role | Review request | Assay provider plus Praxis human-step interface pending |
| H2 | Record reviewer decision and revised eligible-control mask | H1 evidence and explicit authorized response | Accepted exclusions or pending/rejected decision | Responsible scientist; no automatic consent |
| H3 | Compute anchors, contrast and normalization on reviewed mask | H2-approved retained controls | Normalized table and checks under the same arithmetic rule | Assay normalization/checker provider pending |

- Internal branches and selection rules: Hold H2 without a response; reject unsupported or unapproved exclusions. Reviewer may retain all controls with reasons. No post hoc mask changes after H3 without a new linked revision/attempt.
- Human judgment, if required: H2 explicitly requires a named reviewer/authority, evidence, reasons and time. A synthetic reviewer in the walkthrough is not actual approval.
- Step evidence and effects: Review creates a retained decision/mask record. Computational replay can reuse that decision but must not pretend to repeat the review or physical assay.
- Termination and convergence: Wait or explicitly cancel pending review; arithmetic runs only after supported approval. Resumption semantics await #6.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| contrast threshold | Signal-unit minimum H minus L | Mandatory explicit input; analytic fixture uses 1 signal unit | Strictly positive and retained |
| minimum controls | Count per low/high group | Fixed 3 in this procedure | Changing the minimum needs method-version review |
| permitted exclusion criteria and reviewer role | Methodological authorization | Recorded instrument flag/incident rule and explicit role | Changing criteria or authority requires method-version review |

- Reproducibility controls: Retain both original and revised masks, human outcome/evidence and exact normalization binding. Replay preserves the historical decision; a fresh review is a new trajectory.
- Variant boundary: A supported different review outcome is retained invocation data; changing allowed QC criteria changes the procedure.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| QC evidence and review recording | Assay provider and authorized scientist | Human-step interface/evidence unresolved until scenario preparation | #5/#6 | Authority, incident references, exclusion criteria and retained decisions |
| Normalization after reviewed mask | Assay scientific provider, owner pending | No verified fixture binding | #5/#6 | Retained-mask count, contrast, units, arithmetic and mapping |

- Software environment: Resolved assay-table/quantity binding at launch; instrument acquisition metadata retained without requiring a live instrument to render.
- Resources: Retained table and per-batch arithmetic; measured costs unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Test pending review, unauthorized exclusion and accepted incident; verify masks and raw rows remain distinct, and equal reviewed masks reproduce the same arithmetic.
- Implementations and binding choice: Human-step interface and table-processing implementation pending; substituting automatic control removal would change the Protocol.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Evidence and reviewer authority before H2 | Mandatory | Named actor/role and retained instrument/incident references | Hold unresolved evidence or authority |
| Explicit permitted review before H3 | Mandatory | Attributed review result with accepted/rejected mask | Wait without response; reject unsupported exclusion |
| Counts, contrast and raw/output preservation | Mandatory | Versioned independent table/arithmetic checks | Unsupported contrast or violation; no compliant completion |

- Input and pre-execution checks: Acquisition/grouping plus review authority and evidence before H2; reviewed counts/contrast before H3.
- Output checks: Every retained assay row has matching identity and units; raw/control exclusions remain accessible.
- Actual changes: Create derived responses and an explicit retained-control mask; only controls meeting the declared QC procedure can be excluded. Do not rewrite raw readings or labels.
- Outcome distinctions: Pending human review; completed after supported decision; rejected exclusion; unsupported contrast; failed/cancelled preserving any completed review record.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Retain requested/permitted judgment, actor/authority, evidence, accepted/rejected exclusions and parent/child review correlation.
- Output ownership: Assay provider owns raw acquisition and normalized Results; Praxis records normalization methodology and check/assessment references.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Analytic anchors, outside-range responses, equal anchors, missing flags, unapproved exclusion and preserved raw data; controlled human-review traces.
- Evaluation criteria and comparison basis: Anchor arithmetic, response agreement under equal inputs/masks and documented effects of alternate eligibility; no automatic biological-activity conclusion.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
