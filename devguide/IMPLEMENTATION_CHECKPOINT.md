# Implementation checkpoint, 2026-10-08

Historical checkpoint before the 0.1.0 candidate was committed and qualified.
Current release work and engineering adoption are tracked in
[the candidate plan](releases/0.1.0.md) and Praxis #9. The counts and unpublished
working-tree statements below describe that earlier development state.

[Praxis #1](https://github.com/uibcdf/praxis/issues/1) owns this local implementation
checkpoint. Changes are in the working tree; no published commit, remote CI result,
public package or scientific admission is implied. The
[implementation guide](FIRST_SLICE.md) describes the precise API and limits.

## Acceptance coverage

| Review finding / issue | Implemented local response | Verification |
| --- | --- | --- |
| Contract guarantees, #5 | Typed/quantity fields and parameters; pre/runtime/post gates; scoped human/provider evidence; throughout enforcement requirements; cancellation/waiting | Native-failure regressions plus human review, temporal coverage, bounds/units and cancellation acceptance |
| Requests/composition, #6 | Capability or Protocol entry; recorded policy/criteria; separate exact binding; pinned descendant implementations; bounded repeat/branch; parent/child correlation; recursion rejection | Selection/abstention, historical preparation, nested children, changed grandchild and ordered-boundary regressions |
| Assessments/suitability, #7 | Exact scenario queries; conflicting/superseded/withdrawn history; explicit status/admission review; evidence-based promotion gate; resource/fidelity profiles | Scoped conflict/revision, admission digest/evidence, withdrawal and comparative-document acceptance |
| Benchmarks/reporting, #8 | Named physical metrics; evaluator config/implementation/environment; seeds; full checkpoints/denominators; new analysis on retained outputs; descriptive statistics/resources; offline audit/rendering | Two-method fixtures, incompatible cases, evaluator/recording failures, interrupted process/reanalysis and prohibited method rerun |
| Original methodological learning | Explicit proposer/maintainer/reviewer/authority, source-workflow and assessment links; no execution-driven promotion | Admission/promotion regression and preserved definition |
| Catalog portability | Closed digest-checked bundles and explicit incoming schema adapters | Roundtrip/history, conflicts before admission and migration identity tests |
| Trace/replay | Offline intent/child reconstruction; historical implementations/environment/status and provider availability checks; new linked attempt; explicit equivalence comparator | Changed environment/reference rejection, preserved original, comparator evidence without validation |
| Filled templates, #4 | [Capability @2](proposals/hydrogen_refinement/capability.md), [Hydride @2](proposals/hydrogen_refinement/hydride.md), [OpenMM @2](proposals/hydrogen_refinement/openmm.md), [technical review](proposals/hydrogen_refinement/review.md); benchmark template | Source review; machine definitions roundtrip and @1/@2 historical acceptance |
| Real provider workflow | Public MolSysMT PDB selection/RMSD/least-RMSD; physical quantities, digest/correspondence, two conventions and reports | Packaged 1vii PDB; same geometry, controlled 1 nm translation, incompatible quantity input; provider-owned numerical work |
| Package/governance readiness, #9 | Restored existing governance surface and canonical guide; Conda development/test routes/private recipe; dependency preflight/negative tests; reproducible source contents and runtime archive check | Local route/governance/quality checks and private artifact qualification; remote/public closure still pending |

The current complete source suite has **129 passing tests** under local Python
3.14. This includes the optional actual MolSysMT qualification case with its local
PDB. Ruff lint/format and the dependency/governance preflights pass. A result from
local sibling sources does not qualify the public dependency closure or other platforms.
Private wheel/source artifact qualification is recorded alongside this checkpoint
in `verification.json`; it identifies bytes and scope rather than a public release.

The real provider exercise retains four available measurements across six planned
invocations. Fixed-frame RMSD for a controlled translation is 1 nm; optimal-superposition
RMSD is approximately zero. They answer different scientific questions. A successful
case here validates this limited interface exercise, not a general protein methodology.
Core fictional fixtures remain explicitly dimensionless and unvalidated.

## Remaining owned work

1. **MolSysMT #323 / Praxis #3:** hydrogen public adapters, exact scientific model and
   nested configuration schema, environmental/motion coverage, unit/precision/mapping
   qualification, actual throughout enforcement and independent scientific evaluation.
   Proposals can be cataloged experimentally; neither hydrogen binding is executable.
   Scientific maintainer/reviewer and admission authority still require actual humans.
2. **MOLI #28 / Praxis #1/#5/#6:** shared invocation, authoritative Run/ExecutionPlan,
   application semantic-persistence versus Recorda partial-commit behavior and recovery.
   Local prepared/attempt records expose outcomes and correlation; no shared backend,
   project Evidence/Decision or cross-component wire contract was invented.
3. **[Praxis #9](https://github.com/uibcdf/praxis/issues/9):** reviewable published commit,
   exact-head remote installed-package matrix and published dependency closure, MOLI
   Python-package registry/review activation, release candidate/version/resources,
   Conda artifact/platform qualification and authorized publication. Configured lanes,
   a private development recipe or a local wheel do not complete these gates.

These remain open until their evidence/owner decisions exist. No issue requiring
provider, human or platform acceptance is closed by local interface tests.

## Intentional limits of this increment

The local runner is sequential with bounded declared branches/repetitions. It does
not offer adaptive/unbounded workflows, parallel/distributed scheduling, suspension/
resume, rollback or general provider-reference resolution. The resource manifest
captures the observed platform/packages plus application declarations, not every native
binary, hardware counter or credential. Timing includes declared preparation/recording
costs, with no warm-up removal or cache guarantee. Arithmetic sample summaries do not
supply inferential confidence intervals; domain-specific uncertainty and equivalence
belong to exact evaluator/checker extensions. Evidence scope is checked, identity and
provider internals are not authenticated. The programming design remains extensible;
these broader mechanisms are not falsely presented as completed interfaces.
