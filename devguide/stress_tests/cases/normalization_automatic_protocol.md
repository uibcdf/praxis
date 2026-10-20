# Protocol proposal: Arithmetic control anchors from a preapproved mask

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:assay-control-normalization@draft-1](normalization_capability.md)
- Protocol reference/version: stress:assay-mean-anchors@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Uses every control in the supplied verified eligibility mask; preserves raw readings and maps.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed transparent affine normalization using arithmetic means of declared eligible low/high controls.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: L and H are arithmetic means of retained low/high controls separately per declared batch; normalize each assay reading using their contrast.
- Model assumptions and coverage: Declared control populations and eligibility are scientifically meaningful; no implicit plate pooling.
- Comparability of outputs: Compare downstream responses only with identical raw acquisition, control population, retained mask and grouping. Different anchor choices must be reported as differing normalization.

## 3. Contract compatibility and applicability

- Additional input/output requirements: At least three eligible low and three eligible high controls per batch; all flags are resolved in the preapproved input mask.
- Additional preconditions and scope: Finite signal readings; H minus L exceeds a strictly positive predeclared threshold in the signal unit.
- Invariant enforcement: Read retained snapshots; derive anchors/mapped outputs without changing raw data. Independent arithmetic, count, threshold and identity checks.
- Applicable: Verified mask, counts, units and contrast pass for every reported batch.
- Inapplicable: Insufficient controls or contrast not above threshold; no fabricated normalization denominator.
- Undetermined: Mask approval, batch labels or acquisition flags unresolved; hold preparation.
- Limitations: Mean anchors remain sensitive to eligible control values; no post hoc exclusions or clipping.
- Advantages and disadvantages: Proposed advantage versus reviewed-mask workflow: no new review step for already approved controls. Disadvantage: cannot resolve a new QC ambiguity inside this procedure. Costs/quality are unmeasured.
- Favorable and discouraged scenarios: Favorable hypothesis for routine preapproved batches; discouraged where eligibility still needs human adjudication.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| N1 | Verify acquisition, grouping and preapproved mask | Retained raw/mask snapshots | Eligibility, counts and units findings | Assay data provider/checker pending |
| N2 | Compute separate L/H means and threshold finding | N1 retained controls | Anchors and contrast | Assay normalization provider pending |
| N3 | Normalize retained assay rows and verify mapping | N2-supported contrast and original rows | Derived dimensionless table and evidence | Table/quantity checker pending |

- Internal branches and selection rules: One independent normalization per declared batch; no pooling, clipping or alternate anchor method.
- Human judgment, if required: Mask approval occurred upstream; preserve that approval reference. No new discretionary decision inside this Protocol.
- Step evidence and effects: Read-only source processing; outputs and recording are derived effects. Physical measurement is not replayed.
- Termination and convergence: Finite batch processing; retain each batch status if a later batch fails.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| contrast threshold | Signal-unit minimum H minus L | Mandatory explicit input; analytic fixture uses 1 signal unit | Strictly positive and retained |
| minimum controls | Count per low/high group | Fixed 3 in this procedure | Changing the minimum needs method-version review |

- Reproducibility controls: Acquisition, labels, grouping, mask/approval, arithmetic binding, units and threshold retained.
- Variant boundary: Threshold within documented scientific context is a declared parameter; median anchors or automated outlier deletion changes the procedure.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Acquisition snapshots and normalization operation | Assay scientific provider, owner pending | No verified fixture binding | #5/#6 | Raw-data preservation, anchor arithmetic, counts and unit/mapping checks |

- Software environment: Resolved assay-table/quantity binding at launch; instrument acquisition metadata retained without requiring a live instrument to render.
- Resources: Retained table and per-batch arithmetic; measured costs unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Control labels/mask and batch boundaries survive composition; analytic denominator and outside-range fixtures retain expected arithmetic.
- Implementations and binding choice: External table-processing binding pending; equivalent implementations need mapping, unit and numerical evidence.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Control eligibility/counts/units | Mandatory | Approved-mask reference and table checker | Hold on unknown; block inadequate controls |
| Contrast before division | Mandatory | Anchor/threshold measurement | Unsupported contrast; no division |
| Raw preservation and output IDs/values | Mandatory | Independent snapshot/mapping/arithmetic checks | Violation prevents compliant completion |

- Input and pre-execution checks: N1 including approval and grouping; no live-table changes after preparation.
- Output checks: Every retained assay row has matching identity and units; raw/control exclusions remain accessible.
- Actual changes: Create derived responses and an explicit retained-control mask; only controls meeting the declared QC procedure can be excluded. Do not rewrite raw readings or labels.
- Outcome distinctions: Completed normalization, unsupported contrast, undetermined eligibility, partial multi-batch result, failed/cancelled.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Retain acquisition/grouping, approved mask, low/high membership, L/H, contrast threshold and any upstream approval.
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
