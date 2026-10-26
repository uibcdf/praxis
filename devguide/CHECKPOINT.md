# Pause checkpoint — 2026-10-26

Development is paused at the user's request. This is the maintained handoff for
resuming work; [the 2026-10-08 checkpoint](IMPLEMENTATION_CHECKPOINT.md) remains
historical. [Next steps](../NEXT_STEPS.md) is the issue-backed remaining-work queue.

## Completed state

The public source tag [0.1.1](https://github.com/uibcdf/praxis/tree/0.1.1) identifies
`2a5149b4f7e9b19ed829c5744d24d176bc8491f7`, annotated tag object
`dc25f035b4cc90358a58cfe453f5540e558e0321`. The [release record](releases/0.1.1.md)
and [tracked evidence](evidence/release_0_1_1.json) preserve its accepted identity,
original hashes and native results. Tag 0.1.0 remains unchanged.

| Completed issue | Delivered behavior |
| --- | --- |
| [#15](https://github.com/uibcdf/praxis/issues/15) | Caught mandatory runtime-check exceptions cannot produce a supported terminal contract; failure, unresolved/waiting and advisory behavior retain their own outcomes. |
| [#16](https://github.com/uibcdf/praxis/issues/16) | Definition audit distinguishes a valid human-review declaration from a missing executable checker, preserving pending assessment/admission. |
| [#14](https://github.com/uibcdf/praxis/issues/14) | Reviewed bounds/public pins for ArgDigest 0.17, SMonitor 0.22 and PyUnitWizard 0.29; public Recorda 0.3.3 and Ackredit integrations execute; legacy floor coverage remains. |

The original exact-source qualification passed all 19 native jobs and independently
verified 17 JUnit reports (213 passed + only the optional absent-MolSysMT skip in
each). Installed Conda and latest-provider matrices cover Linux x86_64/macOS arm64
and Python 3.11–3.14; the original wheel passed on Linux 3.14. Accepted coverage is
86.27%. Governance and the read-only publication route passed. Full captures and
records are preserved with their checksums in [the evidence bundle](evidence/README.md).

The [tag-triggered run](https://github.com/uibcdf/praxis/actions/runs/40151305420)
and [subsequent scheduled run](https://github.com/uibcdf/praxis/actions/runs/40347697057)
also completed successfully for this source. Their rebuilt outputs do not replace
the original qualified producer files. These software checks do not establish
scientific validation or an executable hydrogen method.

## Open work and resumption conditions

There are five open Praxis issues, grouped into three fronts as checked at pause:

| Praxis issues | Owner/dependency | Condition for further work |
| --- | --- | --- |
| [#1](https://github.com/uibcdf/praxis/issues/1), [#5](https://github.com/uibcdf/praxis/issues/5), [#6](https://github.com/uibcdf/praxis/issues/6) | Shared agreement in [MOLI #28](https://github.com/uibcdf/moli/issues/28), then Praxis-local conformance | Agree authoritative invocation/Run/ExecutionPlan and semantic-write/Recorda partial-commit/recovery ownership before freezing or extending the shared bridge. Existing local interfaces are implemented; their records remain provisional. |
| [#3](https://github.com/uibcdf/praxis/issues/3) | Scientific provider [MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323), Praxis scientific maintainers/reviewers | Supply and qualify a real hydrogen binding, model/configuration, coverage and throughout-preservation evidence; appoint actual reviewers and record scoped scientific assessment. |
| [#9](https://github.com/uibcdf/praxis/issues/9) | Praxis distribution owner | Select public Conda publication separately, preserve the qualified original file, verify coordinate/write authorization, independently observe public poststate and qualify clean public-channel installations. |

MOLI PR #66 registry synchronization is complete. The
[Praxis receiving handoff](https://github.com/uibcdf/molsyssuite/issues/135#issuecomment-6392030639)
was delivered to MolSysSuite #135. The workspace operator still owns the actual
shared-environment refresh and whole-workspace origin/closure checks.

## Publication and resources

The source tag is public; no public Conda package, GitHub Release or Zenodo archive
was created by this work. Public distribution is not automatically selected on
resumption. APIs/storage remain experimental, and qualified platform claims remain
Linux x86_64/macOS arm64; Windows and Intel macOS are unclaimed.

Original binaries and local full records are retained in ignored
`dist/0.1.1-qualified/`, owner #9. They have remote Actions copies; the original
candidate artifact expires on `2026-11-24T00:55:44Z`. Review retention before that
date or at resumption/publication/replacement/retirement, whichever comes first.
The tracked receipt bundle preserves records rather than package binaries. Do not
rebuild or substitute a same-version file to replace the accepted original.
The publisher currently downloads the original producer artifact. If that Actions
copy expires, recover trusted availability of the same qualified bytes under #9
before publication; rerunning a build does not recover that recorded file.

Task-owned disposable receiving environments, temporary test workspaces, caches
and the temporary branch were retired. Caller outputs and the named shared
environment were preserved. No active local development session is needed to
resume from these records.

This pause closeout changes documentation and engineering records only. Its local
link/JSON/integrity/governance checks are separate from the accepted runtime
qualification above; it does not retag or certify newly built 0.1.1 files. A future
code/dependency/release change requires its applicable exact-source gates. The
manual recovery route remains `gh workflow run tests.yml --repo uibcdf/praxis --ref main`.
The documentation-only pause commit uses `[skip ci]` after these local checks;
this is not new runtime CI evidence, and does not defer any changed code tests.
