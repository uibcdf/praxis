# Protocol proposal: Full weighted proper rigid fit

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s) and proposed maintainer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Target Capability: [stress:paired-rigid-comparison@draft-1](geometry_capability.md)
- Protocol reference/version: stress:rigid-all-pairs@draft-1
- Proposed change: New hypothetical experimental Protocol.
- Scientific reason and compatibility: Fits every supplied pair, retaining the common proper-motion and full-report contract.

## 2. Scientific basis and origin — minimum content

- Origin: Proposed procedure for design stress testing.
- Scientific references or proposed rationale: Proposed objective: minimize the sum of w_i times squared distance between R a_i + t and b_i, with a proper rigid R.
- Differences from the referenced method: A proposed fixture, not a reproduction claiming published validation.
- Scientific model: Weighted Euclidean rigid least squares, all supplied pairs; dimensionless positive weights.
- Model assumptions and coverage: Declared correspondence is scientifically appropriate. Nonperiodic coordinates; no atom rematching.
- Comparability of outputs: Compare full residuals only with the same pair mapping, weights and units. Optimal all-pair loss does not rank biological relevance.

## 3. Contract compatibility and applicability

- Additional input/output requirements: The full fitting geometry must support a unique proper transform within the declared rank tolerance.
- Additional preconditions and scope: At least three noncollinear correspondences and explicit finite weights.
- Invariant enforcement: Provider operates on retained snapshots and returns derived coordinates. Independent checks verify proper motion, map preservation and original snapshot integrity.
- Applicable: Input and identifiability checks pass; scientific appropriateness of the supplied correspondence is explicitly declared.
- Inapplicable: Collinear or coincident fitting pairs when a unique transform is requested. A request to allow reflection contradicts this contract; mirrored input sets can still be compared by proper motion with reported residuals.
- Undetermined: Rank near tolerance or scientific correspondence not established; preparation holds pending a finding.
- Limitations: Outliers influence the declared global least-squares objective; no robustness or functional-equivalence claim.
- Advantages and disadvantages: Proposed advantage versus trimming: uses every pair with one stated global objective. Proposed disadvantage: an outlier can influence the transformation. Neither is a measured performance result.
- Favorable and discouraged scenarios: Favorable when global geometry is the goal and correspondence is trusted; discouraged when an explicitly local stable-core fit is required. Degenerate inputs are excluded, not merely inconvenient.

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| G1 | Verify snapshots, mapping, weights, units and rank | Input pair and tolerances | Check findings and supported input | Geometry provider/checker roles pending |
| G2 | Solve the declared proper rigid objective | G1-supported inputs | R, t and solver evidence | Reusable rigid-fit provider operation pending |
| G3 | Measure every paired residual and verify invariants | G2 transform and original snapshots | Full residual table, RMSD and integrity/proper-motion checks | Independent measurement/checker role pending |

- Internal branches and selection rules: No method fallback. Rank ambiguity stops; solver ambiguity returns inconclusive.
- Human judgment, if required: Input correspondence declaration may need a scientist; the fit itself has no manual branch.
- Step evidence and effects: Pure derived outputs. Solver internals are provider-declared; independent geometric checks do not establish unrelated engine guarantees.
- Termination and convergence: One declared solve followed by checks; no automatic iterative refitting.

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| rank tolerance | Dimensionless rank threshold relative to largest singular value | Explicit 1e-10 in this fixture | Positive; recorded change remains a documented parameter variant |
| rigid tolerance | Dimensionless orthogonality/determinant tolerance | Explicit 1e-8 in this fixture | Positive; exact value retained |

- Reproducibility controls: Retain numerical solver/binding revision, mapping order, weights and tolerances; no stochastic seed.
- Variant boundary: Declared weight/tolerance choices stay within the procedure; changing mapping policy or adding reflection/scaling changes the method.

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| Rigid solve and geometry measurement | Scientific geometry provider, ownership pending | No verified fixture binding | #5/#6 | Unique-fit checks and analytic transform/residual cases |

- Software environment: Numerical-library/solver revision, floating-point mode and units codec must be resolved for execution; no engine availability claim.
- Resources: Coordinate storage and one rigid fit; CPU binding proposed. Capacity limits remain to be measured.
- Cost/performance: Measured performance unknown. Stated convenience/cost differences are hypotheses for the declared scenarios.
- Executability assessment: Not executable in Praxis today; no scientific provider binding has been registered or verified for this fixture.
- Composition verification: Analytic translation/rotation, zero residual, degeneracy, no reflection, stable mapping and unchanged snapshots.
- Implementations and binding choice: Reference CPU and accelerated implementations could target this Protocol; both need exact versions and compatibility evidence. Explicit binding required; accelerator availability must not change scientific objective.

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| Mapping/units/rank before solve | Mandatory | Named provider/checker revision, complete pair set | Block on failed/unknown/error |
| Proper transform and snapshot integrity after solve | Mandatory | Independent geometry and integrity findings | Flag contract violation; no compliant completion |

- Input and pre-execution checks: G1 findings must pass; mutable inputs changed after preparation require new snapshots/preparation.
- Output checks: G3 must verify every pair and proper motion at recorded tolerances.
- Actual changes: Only derived transformed coordinates and measurements may be produced. Identity transform/zero residual can be valid; original coordinate objects are not edited.
- Outcome distinctions: Completed/identity comparison; blocked degeneracy; inconclusive numerical ambiguity; failed/cancelled with retained partial outputs.
- Failure handling: Retain original inputs and any partial derived outputs with incomplete status. Record failure/cancellation and any already completed effects; a retry receives a separate attempt identity.
- Execution record requirements: Definition and binding revisions, selection, input snapshots and units, resolved parameters, actual environment, ordered steps, check findings/evidence, termination and provider output references. Record the common all-pair objective, rank diagnostics and evidence from the actual binding.
- Output ownership: Geometry provider owns transformation/residual Results; Praxis owns method definitions and scoped interpretation of compliance.
- Unresolved mandatory checks: Mandatory unknown/error/skipped checks block the dependent phase when required there. A future output check is not an already failed launch prerequisite. An explicitly authorized exploratory operation retains its unresolved guarantees and cannot claim compliant completion.

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: Experimental fixture; no scientific validation.
- Evaluation performed: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Analytic identical/translated point sets, reflected and collinear cases, and one-outlier cases; independent orthogonality, immutability and full-residual checks.
- Evaluation criteria and comparison basis: Common full-residual metrics and analytic transform checks; outlier sensitivity is a separately declared comparison criterion.
- Supporting evidence and open questions: Future benchmark and expert assessment are pending; current expectations are scoped proposals.

## 9. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Local draft-1, 2026-10-07; no scientific admission review.
- Outcome: Pending.
- Rationale, scope, and conditions: Template completion demonstrates expressibility only; implementation, executability and scientific validation remain distinct.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
