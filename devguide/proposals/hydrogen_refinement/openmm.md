# Protocol proposal: restricted OpenMM hydrogen minimization

Template revision: 2. Proposal revision: 2, 2026-10-08.

## 1. Proposal, target and responsibility

Praxis [#3](https://github.com/uibcdf/praxis/issues/3)/[#4](https://github.com/uibcdf/praxis/issues/4).
Codex assembled this draft; scientific maintainer/admission authority await
designation. Exact Protocol: `praxis:protocol:molecular.openmm_restricted_hydrogen_minimization@2`,
targeting [Capability @2](capability.md). [Machine definition](../../../src/praxis/data/hydrogen_refinement/openmm_protocol_v2.json).
This revises the candidate contract; it does not select a force field implicitly.

## 2. Scientific basis and origin

Restricted continuous local minimization with an explicitly authored OpenMM
System. [LocalEnergyMinimizer documentation](https://docs.openmm.org/latest/api-python/generated/openmm.openmm.LocalEnergyMinimizer.html)
describes L-BFGS minimization, included force groups and convergence tolerance.
The molecular energy model still requires exact parameter/force definitions,
water/ion/cofactor coverage, nonbonded conventions and constraints. Naming OpenMM
alone specifies none of these. Compare energies only under the same declared model;
Hydride energy and this model's energy do not share a universal scale.

## 3. Contract compatibility and applicability

Resolve original-to-System particle correspondence and a complete model covering
all declared surroundings. The provider must freeze every nonauthorized coordinate
throughout minimization, including protected H, constraints, virtual-site updates
and working conversions. Positional restraints allow displacement and therefore do
not establish the invariant. A final restoration also fails it. A freezing mechanism
must be qualified against the exact engine/platform; historical
[OpenMM #3884](https://github.com/openmm/openmm/issues/3884) is a reason to test actual
minimization behavior rather than extrapolate from integration behavior.

Applicable only with explicit coverage and verified restriction. Missing parameters
or a method demonstrably moving frozen atoms are exclusions; missing coverage data
is undetermined. Favorable (proposed): model-compatible continuous H relaxation.
Disadvantages (proposed): parameterization and convergence overhead; local minima
and model dependence. Performance and superiority are unmeasured. This does not
relax heavy atoms or infer the chemical state.

## 4. Procedure

| Step | Action | Dependency | Output/check | Provider need |
| --- | --- | --- | --- | --- |
| parameterize | Resolve references, map particles, instantiate exact covered model and restriction | Common inputs and configuration | Explicit coverage, parameter and enforcement manifest | MolSysMT public adapter pending |
| minimize | Restricted local H-only minimization | Qualified System/context | Candidate geometry, stopping cause and scoped runtime evidence | MolSysMT restricted operation pending |
| evaluate | Compare original/result identities, chemical state, changes and convergence | Retained inputs/candidate | Authoritative result/report/correspondence | MolSysMT checkers pending |

No automatic engine/model switch. Explicit force groups, initialization, budgets
and platform are retained. Runtime gates consume provider enforcement evidence.
Human scientific model/admission review is pending. Cancellation is at declared
boundaries; stopping an opaque solver requires provider support. Replay is a new
calculation and cannot promise identical floating-point trajectories.

## 5. Parameters and permitted variants

| Parameter | Meaning/unit | Required setting | Permitted scope |
| --- | --- | --- | --- |
| provider_configuration | Exact provider configuration object | Required; no implicit defaults | Validated nested provider schema pending |
| model and parameter sources | Molecular potential and coverage | Exact IDs/digests | A changed scientific model needs an explicit definition decision |
| force tolerance | Force convergence quantity | Explicit positive quantity, e.g. kJ/mol/nm | Exact unit/field handshake and provider check |
| iteration limit | Dimensionless bounded search budget | Positive finite integer | Budget exhaustion distinguished from convergence |
| platform/precision/force groups | Actual solver settings | Explicit and pinned | Qualified compatible implementation only |

Physical quantities use the shared codec. No numeric defaults are proposed before
model/provider review. Seeds are recorded where a selected provider algorithm uses
randomness; a deterministic solver does not need an invented seed.

## 6. Implementation and execution requirements

| Requirement | Owner | Availability/work | Required verification |
| --- | --- | --- | --- |
| Model coverage/particle mapping | MolSysMT, [#323](https://github.com/uibcdf/molsysmt/issues/323) | Pending | All environment components, chemical state and stable original mapping |
| Frozen-coordinate minimization | MolSysMT/OpenMM | Pending qualification | Actual selected engine/platform leaves all protected coordinates fixed throughout |
| Result and scientific termination | MolSysMT/provider | Pending | Resolved model, force criterion, convergence/budget cause and scoped evidence |

Pin OpenMM version/platform, model files/digests and license information at
qualification. CPU is a possible qualification target; GPU is not assumed or
required. Memory, setup cost and minimization time are unknown. No executable
binding is registered; available OpenMM does not qualify this composition.

## 7. Checks, outcomes and provenance

Mandatory pre/runtime/post guarantees are inherited from Capability @2. Retain
attempt-scoped instrumented/independent throughout evidence for each declared step.
Endpoint preservation remains an additional output check. Failed/unknown checks are
not passes. Partial, cancelled, nonconverged and valid unchanged results retain their
actual status and original-to-result changes. Input snapshots are immutable. Record
model parameterization, sources, scientific/solver settings with units, environment,
iterations, native failures, actual enforcement, checks and provider-owned results.
Praxis records this methodology; it creates no Nextia Evidence or project Decision.

## 8. Scientific evaluation and validation

Experimental; no completed scientific validation. Plan exact-freezing stress cases,
protected H, bonded/constraint/virtual-site coupling, representation precision,
full environmental coverage, missing parameters and nonconvergence, then independently
assessed receptor cases. Scientific evaluation uses predeclared model-specific and
independent common criteria. Lower local energy alone is not biological validation.

## 9. Review record

Codex technical review of revision 2, 2026-10-08: [record](review.md).
Outcome: provider qualification/model clarification needed; human admission pending.
Version 1 remains available historically. Execution remains blocked by explicit needs.
