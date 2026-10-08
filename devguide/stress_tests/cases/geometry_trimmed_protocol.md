# Protocol proposal: Deterministic trimmed proper rigid fit

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:paired-rigid-comparison@draft-1](geometry_capability.md)
- Protocol reference/version: stress:rigid-trimmed@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Changes the fit objective to a retained subset while preserving full-pair outputs and rigid/input invariants.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed repeated trimming to examine a stable subset under a fixed correspondence; robustness is a hypothesis to evaluate.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: At each iteration fit the retained k pairs by weighted rigid least squares; choose the next k by smallest unweighted residual distance. Always report both subset and full weighted RMSD.
- Model assumptions and coverage: Declared correspondence is scientifically appropriate. Nonperiodic coordinates; no atom rematching.
- Comparability of outputs: Same original mapping, weights and full-pair metric required. Trimmed subset loss cannot be treated as the full-fit loss or proof of global improvement.

## 3. Contract compatibility and applicability

- Additional input/output requirements: N and a declared fraction f define k = max(3, ceiling(f times N)); each selected subset must be noncollinear. Original weights remain fixed.
- Additional preconditions and scope: f between 0.5 and 1 inclusive; at least three noncollinear pairs; unique-fit checks apply at every subset fit.
- Invariant enforcement: Provider operates on retained snapshots and returns derived coordinates. Independent checks verify proper motion, map preservation and original snapshot integrity.
- Applicable: Input and identifiability checks pass; scientific appropriateness of the supplied correspondence is explicitly declared.
- Inapplicable: Collinear or coincident fitting pairs when a unique transform is requested. A request to allow reflection contradicts this contract; mirrored input sets can still be compared by proper motion with reported residuals.
- Undetermined: Rank near tolerance or scientific correspondence not established; preparation holds pending a finding.
- Limitations: Stable subset can hide meaningful movements; cycling or iteration exhaustion does not establish optimality.
- Advantages and disadvantages: Proposed advantage versus all-pair fit: isolates a subset under the declared trimming criterion. Disadvantages: subset sensitivity and additional fits; measured benefit and cost unknown.
- Favorable and discouraged scenarios: Proposed for a stable-core question with explicit f; discouraged for a purely global fit objective. Collinear retained subsets are unsupported.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| T1 | Verify inputs and initialize retained subset to all pairs | Original snapshots, weights, f | Initial scope and checks | Geometry provider pending |
| T2 | Fit current subset and measure all original residuals | T1 or previous T3 subset | Transform and full residuals | Rigid-fit and measurement provider pending |
| T3 | Choose k smallest distances with original-pair-order tie break | T2 residuals | New subset and rank findings | Deterministic recipe selection |
| T4 | Stop on unchanged subset or a recorded limit; verify outputs | Subset history and latest transform | Full/subset metrics and termination basis | Recipe/checker integration pending |

- Internal branches and selection rules: Sort by residual then original index; reject a rank-deficient selected subset. Repeated subset detects a cycle; no silent switch to all-pair Protocol.
- Human judgment, if required: Input correspondence declaration may need a scientist; the fit itself has no manual branch.
- Step evidence and effects: Pure derived outputs. Solver internals are provider-declared; independent geometric checks do not establish unrelated engine guarantees.
- Termination and convergence: Stop when retained subset is unchanged; a nontrivial cycle or 20 fits yields unconverged status. Preserve the last actually fitted subset/transform, not an unfitted next subset.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| f | Dimensionless retained fraction | Explicit 0.75 for this fixture | 0.5 through 1; requested value retained |
| maximum fits | Integer search budget | Explicit 20 | Positive |
| rank/rigid tolerances | As in full-fit fixture | 1e-10 and 1e-8 | Positive and recorded |

- Reproducibility controls: Deterministic pair ordering/tie handling and complete subset history; solver revision/tolerances recorded.
- Variant boundary: f and maximum fits are declared variants; changing trimming distance, tie rule or fit objective revises the procedure.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Rigid solve and geometry measurement | Scientific geometry provider, ownership pending | No verified fixture binding | #5/#6 | Unique-fit checks and analytic transform/residual cases |

- Software environment: Numerical-library/solver revision, floating-point mode and units codec must be resolved for execution; no engine availability claim.
- Resources: Coordinate storage and at most the declared number of fits, with full residual checks per fit; measured costs unknown.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Trace every subset, rank check and fitted transform; verify full residuals remain present and cycling is not reported as convergence.
- Implementations and binding choice: External geometry binding plus trimming recipe revision pending; selection cannot change the tie or termination rules.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Mapping/units/rank before solve | Mandatory | Named provider/checker revision, complete pair set | Block on failed/unknown/error |
| Proper transform and snapshot integrity after solve | Mandatory | Independent geometry and integrity findings | Flag contract violation; no compliant completion |

- Input and pre-execution checks: T1 findings and each T3-selected subset rank must pass before its fit; retain any post-preparation input change explicitly.
- Output checks: T4 verifies the last actually fitted subset, every original residual and proper-motion/snapshot invariants.
- Actual changes: Only derived transformed coordinates and measurements may be produced. Identity transform/zero residual can be valid; original coordinate objects are not edited.
- Outcome distinctions: Completed stable-subset/identity comparison; blocked degenerate subset; unconverged cycle/budget; failed/cancelled with latest fitted state.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Record f, all selected/fitted subsets, cycles, actual fit count and both metric scopes.
- Output ownership: Geometry provider owns transformation/residual Results; Praxis owns method definitions and scoped interpretation of compliance.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Analytic identical/translated point sets, reflected and collinear cases, and one-outlier cases; independent orthogonality, immutability and full-residual checks.
- Evaluation criteria and comparison basis: Analytic transform correctness and all-pair coverage first; stable-core usefulness and subset sensitivity require their own scenario-specific assessment.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
