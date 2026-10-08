# Scientific proposal templates

These first drafts implement the template portion of [Praxis #4](https://github.com/uibcdf/praxis/issues/4).
They are editable proposal documents, not serialization schemas, public APIs,
or a finalized catalog lifecycle. Their sections should evolve through use.
Template revision numbers describe the forms, not Capability or Protocol versions.

- [Capability proposal](capability_proposal.md): scientific intent and common contract.
- [Protocol proposal](protocol_proposal.md): a reproducible procedure targeting that contract.
- [Benchmark proposal](benchmark_proposal.md): evaluation scope, controls, physical metrics and retained analyses.

These templates complement the development-report lifecycle. Completing a
proposal does not admit it to a catalog, supply its implementation, or validate it.
Nextia, an AI agent, and an execution framework are unnecessary for submission.

## Preparing and submitting a proposal

Copy the appropriate template, replace its bracketed prompts with substantive answers,
and link the owning Praxis issue. Use an existing issue when it already covers
the proposal; otherwise open a Praxis issue. Submit the filled Markdown in the
issue or link a repository document proposed through a pull request. A Protocol
proposal links the target Capability and its exact version or provisional revision.

During bootstrap, preserve a provisional definition as a document pinned to a
Git commit or an equivalent retained snapshot. Link the issue discussion as well;
an editable issue/comment or a moving branch link alone cannot preserve the exact
historical content. This does not prescribe the future scientific identifier format.

Keep confidential scientific content out of public submissions. Report missing
provider tools to their owner and cross-link their issues. Decisions affecting
shared execution ownership or contracts belong under [MOLI #28](https://github.com/uibcdf/moli/issues/28).

## Minimum content and pending information

A Capability needs an intelligible scientific purpose, semantic inputs/outputs,
and a contract with relevant constraints. A Protocol needs an identified target,
an intelligible procedure with steps, and scientific references or an explicit
proposed rationale. An all-`pending` proposal cannot be meaningfully reviewed.

Other answers may be `pending`, `unknown`, or `not applicable` with a reason.
Identify missing work and its owner where known. Implementation availability,
adapters, performance measurements, and validation can remain pending without
preventing review of an experimental definition. Unresolved scientific choices
remain visible and must be settled before that procedure is claimed executable.

Declare when invariants must hold and how they are enforced. Describe the
scientific model separately from its engine, including its scope and output
comparability. Selection among Protocols and choices inside one Protocol have
distinct criteria and records. For pending dependencies, identify verifiable
completion checks; also check the composition before claiming it executable.

## Review and responsibility

Praxis maintainers identify the reviewer(s) and admission authority for the
submission. Record who proposes and would maintain the definition, which exact
revision was reviewed, the outcome, rationale, conditions, and linked follow-up.
The forms leave this record pending until an actual review occurs.

Useful initial outcomes include clarification requested, rejection with reasons,
and admission as experimental. These are working review descriptions, not a
frozen state machine. Review scientific substance and evidence rather than
field completion. Evaluate these questions separately:

| Question | Meaning |
| --- | --- |
| Admission | Is the methodological definition meaningful enough to retain, under what status and conditions? |
| Implementation availability | Do its required tools and adapters exist? |
| Executability | Can a specific method version run with these inputs, configuration, and environment? |
| Scientific validation | What assessment supports this exact method version, for which conditions and limitations? |

Applicability is a scientific judgment about the method and inputs. A missing
engine is an availability problem; insufficient information can leave
applicability undetermined. Successful execution is not automatic validation.
Assessments record their scope, evidence, actor, and exact definition version.

Revision 2 adds explicit input preservation, scenario-dependent suitability,
Protocol advantages/disadvantages, step evidence/effects, alternative bindings,
and mandatory/advisory check handling. A Protocol may narrow its supported inputs
but must preserve the Capability's promised guarantees. Unknown mandatory checks
do not become passed checks; human evidence needs the permitted scope and authority.
Evaluate checks at their declared phase: a future output check is not a missing
launch precondition, and a pending human decision gates its dependent calculation.

For non-computational or human steps, name the responsible operation and retained
observations. Mark software-specific fields not applicable with a reason where
appropriate. Replaying a recorded decision does not repeat the human judgment
or a physical experiment.

## Changes, versions, and variants

For each change, explain whether it proposes a new identity, a new definition
version, or a permitted parameter variant. Contract, procedure, default, and
applicability changes require explicit consideration of scientific meaning and
compatibility; they must not silently alter a historically used definition.

A variant stays within the documented procedure and allowed parameter choices,
with its resolved configuration recorded. Editorial corrections should be
distinguished from scientific changes. Preserve historically used definitions
and validation records so their exact revisions remain identifiable and retrievable.
Concrete identifier syntax and versioning implementation remain open under
[Praxis #1](https://github.com/uibcdf/praxis/issues/1).

## First exercise and further work

[Praxis #3](https://github.com/uibcdf/praxis/issues/3) supplies the first scientific
exercise: one experimental hydrogen-refinement Capability and two distinct
Protocol proposals, initially Hydride orientation relaxation and restricted
OpenMM minimization. Check that the forms expose shared invariants, different
requirements, pending adapters, and actual evidence status.

The [filled hydrogen Capability](../proposals/hydrogen_refinement/capability.md),
[Hydride](../proposals/hydrogen_refinement/hydride.md) and
[OpenMM](../proposals/hydrogen_refinement/openmm.md) Protocols, and their
[technical review](../proposals/hydrogen_refinement/review.md) exercise revision 2.
Scientific maintainers, human admission and provider qualification remain explicit
pending decisions. The examples inform the programming design without freezing
it through Markdown section names.

The [four-Capability stress exercise](../stress_tests/design_stress_test.md) adds
filled revision-2 examples and design walkthroughs for geometric comparison,
time-series uncertainty, assay normalization and composed response inference.
These remain hypothetical proposals with explicit pending implementations and
scientific assessments. The filled hydrogen examples above now accompany this exercise.
