# Protocol proposal: restricted Hydride hydrogen orientation

Template revision: 2. Proposal revision: 2, 2026-10-08.

## 1. Proposal, target and responsibility

Praxis [#3](https://github.com/uibcdf/praxis/issues/3)/[#4](https://github.com/uibcdf/praxis/issues/4).
Codex assembled this draft; scientific maintainer and admission authority remain
pending. Exact Protocol: `praxis:protocol:molecular.hydride_terminal_orientation@2`, targeting
[Capability @2](capability.md). New version adds the explicit runtime-enforcement
contract. [Machine definition](../../../src/praxis/data/hydrogen_refinement/hydride_protocol_v2.json).

## 2. Scientific basis and origin

Restricted adaptation of [Hydride's documented relaxation](https://hydride.biotite-python.org/api.html):
terminal-bond rotations, hill climbing, electrostatic/nonbonded potential, explicit
charges and periodic box. This is not a general force-field minimization. Source
validation does not validate this adapter. Scores are comparable only within the
same potential/charge assignment and environment; cross-model comparison needs
an independent common evaluator.

## 3. Contract compatibility and applicability

Use the common contract without adding/removing H. Full original correspondence
must survive the working representation. Supported movement subset, protected H,
chemical coverage, periodic handling and precision require provider qualification.
Partially authorized H sharing one rotatable group are particularly important:
rotation may otherwise move protected H. Such cases are inapplicable unless the
adapter demonstrates an admissible operation; unspecified support is undetermined.
The declared environment must participate in scoring, without silent cropping.
Favorable (proposed): covered orientation searches with a fixed environment.
Discouraged (proposed): problems needing continuous bond/angle relaxation or an
energy model not represented here. Arbitrary frozen-H preservation is not assumed.

## 4. Procedure

| Step | Action | Inputs/dependencies | Output/check | Provider need |
| --- | --- | --- | --- | --- |
| inspect | Resolve working representation and verify covered admissible motions | Retained common inputs and exact configuration | Original mapping and coverage manifest | MolSysMT public adapter pending |
| relax | Perform restricted orientation | Qualified representation/model | Scoped enforcement report, actual changes and candidate geometry | MolSysMT public adapter pending |
| evaluate | Verify correspondence, chemical state, preservation and termination | Candidate and original snapshot | Provider report and checked results | MolSysMT versioned checkers pending |

Before use, verify the actual installed callable and supported restriction API:
rendered documentation lists a mask but its displayed signature omits it. Do not
infer a supported signature or treat anchor-group restriction as arbitrary atom
restriction. No fallback hydrogen addition is allowed. There are no implicit
scientific branches; any later candidate comparison needs a declared criterion.
Human review is required before admission, not fabricated as runtime authorization.
Record all selected steps and coverage. Cancellation occurs at declared boundaries;
it cannot interrupt an opaque native calculation safely without provider support.

## 5. Parameters and permitted variants

| Parameter | Meaning/units | Required value | Allowed variants |
| --- | --- | --- | --- |
| provider_configuration | Immutable provider configuration object | Required; no implicit library default | Exact Hydride/Biotite versions, charges source, angle increment, iteration budget, box and movement mask |
| angle increment within configuration | Rotation resolution, angle quantity | Explicit positive value | Provider-supported range verified before execution |
| iteration budget within configuration | Bounded search, dimensionless integer | Explicit positive finite limit | Record budget exhaustion separately from convergence |

The configuration's nested scientific schema/checker is provider-owned and pending;
core object validation does not verify it. Fixed initialization and resolved
settings are recorded. Changing the potential, charge rules or admissible motions
requires a methodological compatibility/version decision, not silent defaults.

## 6. Implementation and execution requirements

| Requirement | Owner | Availability/work | Verification before use |
| --- | --- | --- | --- |
| Restricted public relaxation and conversion | MolSysMT, [#323](https://github.com/uibcdf/molsysmt/issues/323) | Pending; Hydride API alone is insufficient | Exact mask behavior, original mapping, units and complete environment |
| Frozen-coordinate enforcement | MolSysMT/provider | Pending | Attempt-scoped evidence for every declared step, including protected H |
| Model/termination evaluator | MolSysMT/provider | Pending | Exact scientific settings and distinguish nonconvergence |

Hydride/Biotite versions and applicable licenses must be pinned at qualification.
CPU/memory requirement and runtime cost are unmeasured. No executable binding is
registered. Composite executability and scientific validation are both unassessed.

## 7. Checks, outcomes and provenance

Mandatory common preconditions, runtime enforcement and output checks are those
of Capability @2. Runtime proof accepts instrumented or independent evidence,
bound to the exact invocation, attempt and declared steps. Provider declaration
alone is insufficient. Failed checks block/support a violated outcome as appropriate;
missing checks remain unresolved. The provider report retains units, source/working
precision, charges, box, iterations, energy history if available, stopping cause,
changes and authoritative result references. Final equality cannot prove throughout
preservation. Failed/cancelled attempts preserve available records and never mutate
retained inputs; a retry creates a linked attempt, not a continuation guarantee.

## 8. Scientific evaluation and validation

Experimental; no completed scientific evaluation. Test the Capability reference
cases plus unsupported rotations, protected H on the same anchor and representation
roundtrips. Evaluate scientific utility with a separate declared evaluator and
reference cases; keep potential-specific energies scoped. Core runtime regressions
exercise enforcement evidence, not Hydride itself.

## 9. Review record

Technical review: Codex, revision 2, 2026-10-08, [record](review.md).
Outcome: clarification/provider qualification required; human admission pending.
Version 1 remains historical. No compatible implementation or scientific promotion
is implied by catalog registration.
