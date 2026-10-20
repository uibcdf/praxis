# Protocol proposal: [name]

Template revision: 2 (draft). See [proposal guidance](README.md).
This proposes **how to reproducibly fulfill a Capability under declared conditions**.

## 1. Proposal, target, and responsibility — minimum content

- Owning Praxis issue: [link]
- Proposer(s) and proposed maintainer(s): [names; explain pending responsibility]
- Date and proposal revision: [date; reference identifying this revision]
- Target Capability: [identity/version or exact provisional definition reference]
- Protocol reference/version: [existing reference, or provisional designation]
- Proposed change: [new Protocol, new version, or permitted parameter variant]
- Scientific reason and compatibility: [what changes, why, and which historical
  definitions or consumers are affected]

## 2. Scientific basis and origin — minimum content

- Origin: [reproduction, restricted adaptation, or new procedure/composition]
- Scientific references or proposed rationale: [basis for the procedure]
- Differences from the referenced method: [restrictions, adaptations, and their
  consequences; do not imply the original validation covers these changes]
- Scientific model: [energy model, scoring function, or other scientific model;
  definition/version and parameterization where relevant; identify unresolved choices]
- Model assumptions and coverage: [declared physical environment or data scope,
  approximations, boundary conventions, and supported cases; justify exclusions
  or truncation explicitly]
- Comparability of outputs: [conditions under which scores, energies, or other
  outputs may be compared; required common model or explicit conversions and
  limitations where relevant]

[Naming an engine does not fully specify its scientific model. Do not infer
the evaluation environment or silently reduce its declared scope.]

## 3. Contract compatibility and applicability

[Reference the Capability's common contract rather than copying it. Explain
how this procedure preserves its invariants and fulfills its outputs.]

- Additional input/output requirements: [representation, selection, mappings,
  units/dimensions, coverage, and correspondence to the original inputs]
- Additional preconditions and scope: [conditions specific to this procedure]
- Invariant enforcement: [how each required invariant is maintained at the
  stages specified by the Capability, including during execution where required;
  guarantees provided by tools/adapters and effects of working representations]
- Applicable: [conditions and evidence sufficient to establish applicability]
- Inapplicable: [known scientific incompatibilities and reasons]
- Undetermined: [missing information; checks needed to reach a conclusion]
- Limitations: [unsupported cases, uncertainty, and claims the method cannot make]
- Advantages and disadvantages: [conditions, alternatives, criteria, and exact
  supporting references; label measurements, estimates, proposals, and unknowns]
- Favorable and discouraged scenarios: [when this applicable procedure is more
  or less convenient; keep hard exclusions and unknown coverage separate]

[Describe missing implementations separately in section 6.]

## 4. Procedure — minimum content

| Step | Scientific action | Inputs/dependencies | Output or check | Provider/tool or outstanding need |
| --- | --- | --- | --- | --- |
| [step] | [intelligible operation] | [references or prior steps] | [expected outcome] | [owner; tool/version requirement or linked pending work] |

- Internal branches and selection rules: [explicit criteria for choices within
  this procedure, including comparisons between alternatives and their
  scientific basis; distinguish them from selecting among Protocols]
- Human judgment, if required: [where it is needed and how it is recorded]
- Step evidence and effects: [declared, instrumented, or independently checked
  guarantees; scope of opaque/external operations, authorized effects, and limits
  of cancellation or replay]
- Termination and convergence: [stopping criteria and search budgets]

[A methodological proposal can identify pending tools. Resolve every unknown
that determines scientific behavior before claiming reproducible execution.
No missing step or engine may be silently replaced by another method.]

## 5. Parameters and permitted variants

| Parameter | Meaning and unit/dimension | Required value or default and rationale | Allowed range/variants |
| --- | --- | --- | --- |
| [parameter] | [scientific meaning; unit or explicitly dimensionless] | [value/default or pending] | [constraints] |

- Reproducibility controls: [seeds, initialization, tolerances, and deterministic
  or stochastic behavior where relevant]
- Variant boundary: [which choices stay within this Protocol; which changes
  require a definition/version or identity decision]

[Physical quantities retain value, unit, and meaning together. Defaults must
not be inferred from session settings; actual resolved values are recorded.]

## 6. Implementation and execution requirements

| Requirement | Provider/owner | Current availability | Missing work and issue/reference | Verification needed before use |
| --- | --- | --- | --- | --- |
| [tool, adapter, engine, or reference data] | [owner] | [available/pending/unknown; evidence] | [needed work and link] | [specific check, expected result, and verification responsibility; or pending] |

- Software environment: [engine/library versions, compatibility, licenses, and
  environment requirements; explicitly identify unresolved version requirements]
- Resources: [required hardware, memory, storage, and other constraints;
  distinguish optional acceleration from required capacity]
- Cost/performance: [measurements with conditions, estimates with basis, or unknown]
- Executability assessment: [which inputs and environment were checked;
  requirements still preventing execution; or not yet assessed]
- Composition verification: [checks and expected outcomes needed to establish
  that the tools work together for the declared inputs/environment; include
  mappings, units, invariant enforcement, outputs, and failure behavior as relevant;
  identify who will verify them and retain the findings]
- Implementations and binding choice: [distinct compatible implementations of
  this procedure, their exact revisions and compatibility evidence; explicit
  binding or selection policy, or pending]

[Describe provider-independent requirements. Project execution backends and
Nextia integration remain subject to the shared MOLI execution contract.
Available tools do not by themselves establish executability of their
composition. Passing these checks does not establish scientific validation.]

## 7. Checks, outcomes, and provenance

| Requirement and phase | Mandatory or advisory | Checker or human and evidence scope | Failure or indeterminate handling |
| --- | --- | --- | --- |
| [contract/preparation/runtime/output requirement] | [role] | [identity/version, authority where relevant, expected evidence and coverage] | [block, inconclusive outcome, or justified exception; checker error/skipping remain visible] |

- Input and pre-execution checks: [contract, applicability, coverage, and configuration]
- Output checks: [invariants, input/output mappings, and completion criteria]
- Actual changes: [how the report identifies modified and preserved elements
  against the authorized scope, including cases with no modifications]
- Outcome distinctions: [completed, completed unchanged where meaningful,
  incompatible/unsupported, undetermined, unconverged, inconclusive, partial,
  failed, or cancelled;
  state the conditions and what can legitimately be returned for each]
- Failure handling: [input mutation guarantees, partial outputs, and retry linkage]
- Execution record requirements: [exact Capability/Protocol definition references,
  method-selection record, actual inputs and environment, scientific
  model/parameterization, tools/versions, resolved parameters and units,
  seeds, branches, actual changes, checks, termination, and output references]
- Output ownership: [providers of authoritative Results/Artifacts; how this
  recipe links to them without duplicating their authority]
- Unresolved mandatory checks: [readiness remains unresolved; any authorized
  exploratory operation and its pending guarantees must be identified explicitly]

[The recipe's checks and internal selection do not automatically create project
Observations, Evidence, or Decisions, or establish scientific validation.]

[A final check or restoration cannot demonstrate an invariant required
throughout execution. Describe the enforcement mechanism and its verification.]

## 8. Scientific evaluation and validation

- Proposed maturity/validation status and scope: [for example, experimental]
- Evaluation performed: [exact definition/version, cases, environment, criteria,
  findings, limitations, and assessor; or none]
- Evaluation planned: [contract checks and independent scientific assessment]
- Evaluation criteria and comparison basis: [reference cases/data, baselines,
  metrics, tolerances, and rationale where relevant; distinguish correct execution
  from scientific improvement; explain what remains pending]
- Supporting evidence and open questions: [references; missing evidence]

## 9. Review record — completed during review

- Reviewer(s) and admission authority: [names and roles]
- Proposal revision reviewed and date: [exact reference; date]
- Outcome: [pending, clarification requested, admitted as experimental, or
  rejected with reasons; see guidance]
- Rationale, scope, and conditions: [admission, execution, and validation claims
  assessed separately; outstanding work]
- Follow-up and superseded definitions: [linked work and historical references]
