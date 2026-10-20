# Capability proposal: Compare paired coordinate sets by a proper rigid transformation

Form source: template revision 2. Example revision: draft-1. See [proposal guidance](../../templates/README.md).
This proposes **what scientific task can be performed and what fulfilling it means**.

## 1. Proposal and responsibility

- Owning Praxis issue: https://github.com/uibcdf/praxis/issues/1 (design fixture; template exercise also relates to #4)
- Proposer(s): Hypothetical design fixture requested by the repository owner; scientific maintainer pending.
- Proposed maintainer(s): Pending scientific review and provider ownership agreement.
- Date and proposal revision: 2026-10-07; local draft-1. Labels are provisional, not registered immutable method references.
- Proposed change: New hypothetical experimental Capability.
- Definition reference/version: stress:paired-rigid-comparison@draft-1
- Related definitions and compatibility: A geometric comparison fixture for #1. Atom correspondence is supplied; matching atoms is a separate scientific task.

## 2. Scientific intent and need — minimum content

Characterize residual geometric differences between two paired point sets after a declared proper rigid fit. For example, compare a receptor subset across conformations without editing either structure.

## 3. Common contract — minimum content

| Input | Scientific meaning | Required information and constraints |
| --- | --- | --- |
| Coordinate pair | Two N by 3 point sets in one declared length unit | Finite values and retained snapshots; input A and B identify their coordinate frame |
| Correspondence and weights | Ordered one-to-one point identities and fitting weights | N at least 3, same atom/point mapping; positive finite dimensionless weights |

| Output | Scientific meaning | Expected guarantees |
| --- | --- | --- |
| Transform and fitting scope | Proper rotation R, translation t and selected fit-pair IDs | R transpose times R equals identity and determinant equals +1 within recorded tolerance |
| Residual measurements | Per-pair distances and all-pair weighted RMSD after that transform | All input pairs remain represented; units and subset-versus-full metrics are distinct |
| Identifiability report | Supported transformation or ambiguity/degeneracy finding | No unique-fit claim when the geometric constraints are insufficient |

- Invariants: Point identities, mappings and input coordinates remain unchanged throughout; transformations are proper rigid motions, never reflections or scaling.
- Authorized changes: Only derived transformed coordinates and measurements may be produced. Identity transform/zero residual can be valid; original coordinate objects are not edited.
- Successful fulfillment: Produce a supported fit and full residual report, or an explicit ambiguous/unsupported outcome with its basis. Zero residual is a valid unchanged comparison, not proof of biological equivalence.
- Exclusions: Atom rematching, deformation, energetic comparison and inference of common molecular function.
- Input preservation and effects: Provider-owned coordinate snapshots and retained mapping/weight table before use. No permitted in-place mutation or external physical effects.

## 4. Applicability and limitations

- Common preconditions: Finite paired coordinates in convertible units, explicit correspondence and positive weights.
- Scope: Nonperiodic, paired point sets. Periodic unwrapping would require a separate explicitly defined preprocessing method.
- Unsupported or excluded cases: Missing correspondence, nonconvertible units or an undeclared request to unwrap periodic coordinates.
- Undetermined cases: Identifiability of a proposed fit subset until its geometry is checked; provider/binding coverage remains pending.
- Limitations and uncertainty: A low residual only characterizes this mapping and fit objective. The transform can conceal movements outside the declared subset.

## 5. Candidate Protocols, selection, and provider needs

| Procedure/reference | Proposed relationship to the contract | Definition and validation status | Implementation status and outstanding work |
| --- | --- | --- | --- |
| [Full weighted proper rigid fit](geometry_full_protocol.md) | Fits every supplied pair, retaining the common proper-motion and full-report contract. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |
| [Deterministic trimmed proper rigid fit](geometry_trimmed_protocol.md) | Changes the fit objective to a retained subset while preserving full-pair outputs and rigid/input invariants. | Defined hypothetical procedure; no scientific assessment | Provider bindings pending; #5 and #6 |

- Selection between Protocols: Explicit choice: full weighted fit for global agreement; trimmed fit for a stated subset-oriented objective. A policy must identify that objective and may abstain.
- Non-selection outcomes: Degenerate candidate subsets are scientifically unsupported; an absent solver is operational unavailability. Different fit objectives are not silently substituted.
- Selection record requirements: Preserve exact provisional definitions and eventual retained revisions, constraints, findings, actor/policy, selected Protocol and binding, and reasons for every excluded candidate.
- Scenario-dependent suitability: Full fit is proposed for global discrepancies; trimming is proposed for local outliers but can obscure genuine distributed motion. No measured superiority is claimed.

## 6. Evaluation, maturity, and evidence

- Proposed maturity/validation status and scope: Experimental design fixture; admission and validation pending.
- Evidence already available: No executed provider benchmark or scientific validation. Analytic examples in the stress report only exercise the proposed contracts.
- Evaluation planned: Analytic identical/translated point sets, reflected and collinear cases, and one-outlier cases; independent orthogonality, immutability and full-residual checks.
- Acceptance criteria: Predeclared numerical tolerances and complete mapping/metric reporting; scientific usefulness requires a separate domain assessment.
- Outstanding questions: Provider binding verification and scoped comparison claims under #5–#7.

## 7. Review record — completed during review

- Reviewer(s) and admission authority: Pending scientific reviewer and admission authority.
- Proposal revision reviewed and date: Not scientifically reviewed; structural exercise uses local draft-1 on 2026-10-07.
- Outcome: Pending; the design walkthrough does not admit or validate a method.
- Rationale, scope, and conditions: Scientific substance, provider compatibility and measured utility require independent review.
- Follow-up and superseded definitions: Praxis #5 (contracts/evidence), #6 (requests/bindings), #7 (scoped assessments), #8 (benchmarks/reports). No superseded scientific definition.
