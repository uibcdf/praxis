# Capability proposal: [name]

Template revision: 2 (draft). See [proposal guidance](README.md).
This proposes **what scientific task can be performed and what fulfilling it means**.

## 1. Proposal and responsibility

- Owning Praxis issue: [link]
- Proposer(s): [names]
- Proposed maintainer(s): [names, or pending with an explanation]
- Date and proposal revision: [date; reference identifying this revision]
- Proposed change: [new Capability, or revision of an existing Capability]
- Definition reference/version: [existing reference, or provisional designation]
- Related definitions and compatibility: [overlap, extension, or reason for a
  separate identity; explain any changed contract and affected Protocols]

## 2. Scientific intent and need — minimum content

[State the scientific task, why it is useful, and its intended consumers.
Give at least one concrete use case. Define the task independently of a
particular engine, project, or preferred Protocol.]

## 3. Common contract — minimum content

| Input | Scientific meaning | Required information and constraints |
| --- | --- | --- |
| [input] | [semantic meaning] | [requirements; units/dimensions where relevant] |

| Output | Scientific meaning | Expected guarantees |
| --- | --- | --- |
| [output] | [semantic meaning] | [guarantees and correspondence to inputs] |

- Invariants: [what every implementing Protocol must preserve, when each
  invariant must hold, and any justified tolerances; distinguish guarantees
  throughout execution from conditions required only at input or output]
- Authorized changes: [what may change; what must remain fixed; the report
  required to identify what was actually modified, including an unchanged outcome]
- Successful fulfillment: [what constitutes a correct outcome; whether an
  unchanged output can be valid]
- Exclusions: [operations or claims outside this contract]
- Input preservation and effects: [retained snapshots or historical references
  for live/mutable inputs; permitted mutation or external effects and their limits]

## 4. Applicability and limitations

- Common preconditions: [conditions applying to every Protocol]
- Scope: [systems, data, and situations considered]
- Unsupported or excluded cases: [known restrictions and reasons]
- Undetermined cases: [what is unknown and how it could be established]
- Limitations and uncertainty: [what fulfilling the contract cannot establish]

[Keep the common contract separate from a Protocol's additional requirements.
A missing engine or adapter concerns implementation availability; it does not,
by itself, establish scientific inapplicability.]

## 5. Candidate Protocols, selection, and provider needs

| Procedure/reference | Proposed relationship to the contract | Definition and validation status | Implementation status and outstanding work |
| --- | --- | --- | --- |
| [Protocol proposal or scientific reference] | [how it could fulfill the task; unresolved compatibility] | [background reference, candidate adaptation, or defined proposal; assessed validation scope or not assessed] | [available/pending/unknown; provider and issue links] |

- Selection between Protocols: [explicit user choice or proposed deterministic
  policy; criteria such as applicability, validation scope, fidelity, resources,
  or cost; identify where scientific judgment is needed, or state what is pending]
- Non-selection outcomes: [reasons a Protocol may be excluded or a choice may
  remain undetermined; distinguish scientific incompatibility from unavailable tools]
- Selection record requirements: [candidate versions considered, selected
  version, actor or policy/version, resolved criteria, and reasons for selection
  and non-selection]
- Scenario-dependent suitability: [favorable and discouraged choices for stated
  goals/constraints; supporting evidence or explicitly proposed hypotheses;
  distinguish inconvenience from scientific inapplicability]

[Identify references that are only background or candidates for adaptation.
They need not already be executable Protocols. Algorithms, adapters, and
authoritative domain Results remain with their scientific providers. Choosing
an alternative requires explicit selection or a recorded policy; missing
engines or parameters must not cause silent substitution.]

## 6. Evaluation, maturity, and evidence

- Proposed maturity/validation status and scope: [for example, experimental]
- Evidence already available: [references; exact method versions, conditions,
  findings, limitations, and assessor where applicable; or none]
- Evaluation planned: [reference cases, comparisons, checks, and their rationale]
- Acceptance criteria: [distinguish contract compliance from demonstrated
  scientific usefulness or improvement; identify predeclared criteria when relevant]
- Outstanding questions: [what remains to be established and by whom]

[Catalog admission, available implementation, executability for particular
inputs, and scientific validation are separate judgments. A successful
execution does not automatically validate or promote this Capability.]

## 7. Review record — completed during review

- Reviewer(s) and admission authority: [names and roles]
- Proposal revision reviewed and date: [exact reference; date]
- Outcome: [pending, clarification requested, admitted as experimental, or
  rejected with reasons; see guidance]
- Rationale, scope, and conditions: [what was accepted or remains unresolved]
- Follow-up and superseded definitions: [linked work and historical references]
