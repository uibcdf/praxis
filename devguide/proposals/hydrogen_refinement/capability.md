# Capability proposal: environmental hydrogen-coordinate refinement

Template revision: 2. Proposal revision: 2, 2026-10-08.

## 1. Proposal and responsibility

Owning issues: [Praxis #3](https://github.com/uibcdf/praxis/issues/3) and
[filled submissions, #4](https://github.com/uibcdf/praxis/issues/4).
Draft assembled by Codex from the repository design and owner requests. Scientific
maintainer and admission authority await designation by the Praxis maintainer;
this text does not appoint either role. New exact scientific reference:
`praxis:capability:molecular.environmental_hydrogen_refinement@2`.
[Machine-readable revision](../../../src/praxis/data/hydrogen_refinement/capability_v2.json).
Version 1 remains available unchanged. Revision 2 adds mandatory report/correspondence
outputs and an explicit runtime, attempt-scoped, throughout-execution guarantee.
Both candidate Protocols target revision 2; old Protocols still target revision 1.

## 2. Scientific intent and need

Refine positions of already assigned hydrogens in their declared molecular
surroundings without changing the chemical state. Initial consumers include
hydrogen-complete receptor preparation for DockingMT and PharmacophoreMT. Geometry
preparation, hydrogen addition and protonation search precede this task and do
not become implicit steps of it.

## 3. Common contract

| Input | Scientific meaning | Required constraints |
| --- | --- | --- |
| system | Original topology and coordinates | Immutable provider snapshot; exact atom identities and coordinate units |
| structures | Frames to refine | Explicit original structure identities; no silent first-frame selection |
| chemical_state | Bonding, charges, protonation, tautomer and H inventory | Already assigned and immutable; source/model revisions retained |
| movable_hydrogens | Authorized H identities | H only; unambiguous selection in original correspondence |
| frozen_atoms | Complement of movable atoms | Complete disjoint partition including protected H and heavy atoms |
| environment | All declared interacting partners | Explicit selected waters, ions, ligands/cofactors and coverage; no implicit cropping |
| periodic_convention | Spatial convention | Explicit nonperiodic choice or box/reconstruction; lengths and angles carry units |

| Output | Scientific meaning | Required guarantees |
| --- | --- | --- |
| geometry | Refined provider-owned geometry | Same chemical state, inventory, atom/frame correspondence and units |
| modified_atoms | Actual changes, possibly empty | Original identities and before/after coordinate references |
| termination | Declared scientific termination | Converged, valid unchanged, budget exhausted or inconclusive distinguished |
| correspondence | Original-to-result mapping | Bijection for unchanged atom/frame inventory |
| report | Model, coverage, checks and changes | Exact parameters/units, convergence evidence and frozen enforcement scope |

Only authorized H coordinates may change. Every other coordinate must remain
fixed **throughout** computation, including intermediate conversion and scoring
steps. Numerical representation tolerances require an explicit provider-reviewed
budget; an unspecified tolerance is undetermined. Checking the endpoint or
restoring it is insufficient. Inputs remain retained and unmodified; any external
effect belongs in the provider report. An unchanged geometry can fulfill the task
if its declared termination and mandatory checks support that conclusion; it
alone proves neither convergence nor optimality. Excluded: atom addition/removal,
chemical-state search, heavy-atom relaxation and unconditional improvement claims.

## 4. Applicability and limitations

Common preconditions are resolvable references, finite coordinates, complete
chemical state, valid selections, environmental and periodic coverage. Known
incompatibilities fail; missing assignments or unverified coverage stay undetermined.
Implementation absence is recorded separately. No universal support for metals,
noncanonical molecules, alternate locations, periodic images or water orientations
is claimed. Fulfillment establishes declared coordinate handling, not biological
correctness, binding affinity or the best protonation state.

## 5. Candidate Protocols, selection and provider needs

| Proposal | Relationship | Definition/validation | Implementation |
| --- | --- | --- | --- |
| [Hydride restricted orientation @2](hydride.md) | Orientation-only candidate | Restricted adaptation; unassessed | MolSysMT adapter and arbitrary protected-H handling pending |
| [OpenMM restricted minimization @2](openmm.md) | Continuous local-relaxation candidate | Model-specific candidate; unassessed | Complete parameterization and fixed-coordinate evidence pending |

Explicit choice is the initial policy; ambiguity abstains. Record exact candidates,
actor/policy, scenario, configuration, implementation, selection and exclusions.
A covered terminal-H orientation problem may favor orientation search; a fully
parameterized continuous-refinement problem may favor minimization. These are
proposals, without performance measurements. Neither candidate substitutes for the
other automatically. Provider algorithm/adapters and authoritative molecular
results remain with [MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323).

## 6. Evaluation, maturity and evidence

Maturity: experimental; no scientific assessment yet. The issue's preparation
examples establish a consumer need, not refinement validation. Plan: simple
rotatable groups, protected H sharing an anchor, water/ion/cofactor cases, unchanged
and nonconverged cases, excluded chemistry, periodic boundary and conversion
precision cases, then independently assessed receptor examples. Predeclare change
scope and enforcement criteria. Evaluate geometry/contact/energy measures under
each declared model; H-bond count alone cannot establish improvement and energies
from different models cannot be ranked. Provider qualification and scientific
judgment remain separate from core Praxis acceptance tests.

## 7. Review record

Codex technical review of revision 2 on 2026-10-08:
[review record](review.md). Human scientific reviewer and admission authority:
pending. Outcome: candidate ready for discussion, execution blocked by explicit
provider/checker needs. No human admission or promotion is recorded.
