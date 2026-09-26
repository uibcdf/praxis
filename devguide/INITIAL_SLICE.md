# Initial methodological slice

**Status:** implementation design proposal for [Praxis #1](https://github.com/uibcdf/praxis/issues/1). The shared Praxis–Nextia boundary belongs to [MOLI #28](https://github.com/uibcdf/moli/issues/28). This document does not freeze a public API, schema, or registry technology.

## Architectural job

Praxis owns **reusable scientific know-how**. A Capability describes **what** scientific task can be performed, with semantic inputs/outputs, applicability, limitations, and validation state. A Protocol describes **how** to perform it reproducibly, including versioned implementation references, parameters, preconditions, checks, outputs, and provenance requirements. Neither object is a Nextia Strategy, Campaign, Decision, Evidence, or the MolSysSuite API it may invoke.

Praxis must also work directly from Python/Jupyter, outside a MOLI project and without an LLM. One successful project Run never certifies a Capability or automatically promotes a local workflow into shared methodology.

## First slice: inspectable method definitions

The first local implementation should support:

1. Stable identity and explicit version for a Capability and a Protocol. An old version remains retrievable and has the same meaning after a new version is published.
2. A semantic Capability contract: scientific intent, required/optional input kinds, output kinds, applicability/preconditions, limitations, and validation/maturity state. Validation must cite actual review or benchmark records where asserted; `experimental` is an honest initial state.
3. A Protocol definition bound to an intended Capability: required inputs, implementation/version references, parameters with units where physical quantities occur, ordered/dependent steps as needed, checks, expected outputs, environment/resource requirements, and provenance requirements. Do not copy a modeling API into Praxis.
4. Explicit applicability outcomes: applicable, inapplicable with reason, or undetermined/needs judgment. An unknown condition must not silently select a Protocol. A deterministic selection policy may choose among eligible versions; otherwise the caller records a human/agent selection.
5. A local catalog/repository boundary for create, inspect, retrieve by exact version, and list eligible definitions. Catalog entries can later be public, organization-specific, or project-private without changing what Capability/Protocol mean.

The first public fixture may describe an **experimental method for comparing two fictional protein structures**. Synthetic inputs and a fake execution adapter can test method metadata, selection, and versioning; they do not establish scientific validation. A real MolSysSuite or external-engine adapter should be introduced only when a concrete workflow requires it.

## Proposed internal seams

These are responsibilities, not fixed package names:

| Seam | Owns |
| --- | --- |
| Method definitions | Capability/Protocol semantics, versions, applicability, limitations, and validation references. |
| Catalog | Local persistence and lookup of immutable versions; an interface that can later support shared/private registries. |
| Applicability/selection | Deterministic eligibility and reasoned non-selection; no opaque scientific judgment or automatic certification. |
| Execution adapter | Binding a selected Protocol to the normal scientific API/engine through an explicit invocation contract. The producing component owns its Result/Artifact. |
| Provenance boundary | Method version, inputs, parameter/quantity meanings, implementation/environment requirements, and checks exposed for a future ExecutionPlan/Run/Recorda record. |

Praxis does not require a Nextia import. Nextia or a human may call Praxis; MOLI may supply project context and recording. Compute provider selection belongs to the execution infrastructure rather than the scientific method definition.

## Candidate methodology and validation

Architecture 1.0 distinguishes formalizing a workflow from validating/generalizing it. The conceptual schema shows a Protocol with a `capability_ref`, while the learning path allows a candidate Protocol before a validated Capability. The first design should make this tension explicit: an **experimental Capability** may name the intended scientific ability, and a Protocol may implement it provisionally. The association is not a validation claim. Whether standalone candidate Protocols are later needed remains open for evidence from real workflows.

Promoting a workflow requires a separate, authorized validation record with scope, test conditions, limitations, and method version. Deprecation or replacement creates a new historical state; old Runs continue to cite the version they used.

## Generic acceptance journeys

1. Store experimental Capability `C1` and Protocol `M1` for comparing two fictional protein structures. Reopen and inspect their intent, applicability, limitations, checks, and exact versions.
2. An applicability check rejects one incompatible input with a reason and marks one underspecified input as undetermined. Neither is silently executed.
3. Select `M1` explicitly for eligible inputs and provide its exact reference and requirements to a prospective ExecutionPlan. If `M2` is added later, a historical Run still names `M1`.
4. A failed attempt and a successful attempt do not change `C1` to validated. Evidence for validation must enter through an explicit review/promotion operation.

A separate controlled exercise should use an authorized real scientific workflow to expose missing method semantics. Only generalized findings belong in public issues and fixtures.

## Decisions to prove before a stable API

- Minimal semantics of `Capability` versus `Protocol`, including whether a standalone candidate Protocol is necessary.
- Version/revision rules and validation records; whether validation status belongs to a version or a separate assessment.
- Applicability representation and deterministic selection outcomes.
- Method invocation, ExecutionPlan/Run handoff, and owner of domain Results/Artifacts (MOLI #28).
- Local catalog persistence and private/public visibility without binding identity to storage paths.

Composition, automatic multi-Protocol optimization, broad registries, and remote services should follow actual scientific pressure rather than define this first slice.
