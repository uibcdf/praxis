# Consolidation after Praxis 0.1.0

The experimental source milestone [0.1.0](devguide/releases/0.1.0.md) is frozen
at `e253fe76db81b9cb6eaa4db4dc0b78bb60188d39`. All eight installed Conda lanes
passed on Linux x86_64/macOS arm64 and Python 3.11–3.14; complete installed Linux
coverage was accepted at 85.22%. The original artifacts and acceptance receipt
are retained under [Praxis #9](https://github.com/uibcdf/praxis/issues/9).
No public Conda package has been uploaded.

The [implemented API](devguide/FIRST_SLICE.md) includes the local increments from
#5–#8, curation, resource profiles, catalog transfer, trace/replay preflight and
the public MolSysMT RMSD exercise. The template (#4), scoped assessment/suitability
(#7) and benchmark/reporting (#8) acceptance criteria are fulfilled for this
experimental local scope; see the [issue acceptance record](devguide/releases/0.1.0.md#issue-acceptance-and-remaining-work).
The [earlier checkpoint](devguide/IMPLEMENTATION_CHECKPOINT.md) and its development
receipt remain historical evidence, not the current release status.

Remaining work has concrete owners and completion conditions:

- [MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323) /
  [Praxis #3](https://github.com/uibcdf/praxis/issues/3): supply and qualify real
  hydrogen adapters, exact model/configuration, environment coverage, original
  correspondence, units/precision and throughout enforcement. Appoint actual
  scientific reviewers and record scoped assessments. Filled proposals and their
  technical review already exist; no hydrogen binding is executable.
- [MOLI #28](https://github.com/uibcdf/moli/issues/28) /
  Praxis [#1](https://github.com/uibcdf/praxis/issues/1),
  [#5](https://github.com/uibcdf/praxis/issues/5),
  [#6](https://github.com/uibcdf/praxis/issues/6): agree invocation, authoritative
  Run/ExecutionPlan and semantic-persistence/Recorda partial-commit and recovery
  ownership, then check the local interfaces against that shared contract.
  Existing method attempts remain provisional local records.
- [Praxis #9](https://github.com/uibcdf/praxis/issues/9): obtain owner-reviewed
  registry synchronization in [MOLI PR #66](https://github.com/uibcdf/moli/pull/66).
  As of 2026-10-08, its governance passes and its global guide audit is blocked
  by Nextia/MOLI Agent canonical-copy drift under
  [MOLI #60](https://github.com/uibcdf/moli/issues/60). Component review decisions
  are adopted; their registry mirror remains pending merge.
- If public Conda distribution is requested, use only the qualified original file,
  verify coordinate availability and write authentication, independently observe
  public poststate and qualify clean public-channel installations before advertising
  installation. The successful read-only hosted check observed an available CI
  credential; it did not exercise write authorization or publish anything.

The next functional milestone should be an end-to-end scientific Capability:
registration, selection, provider execution, retained checks, audit, comparison
and reporting. The hydrogen case is the candidate once its provider and review
requirements are ready. New abstractions should follow findings from that use.

Human scientific admission/validation requires actual reviewers and provider
evidence; execution, favorable statistics and interface fixtures never supply it
automatically. Statistical inference, broader workflows, parallel/distributed
backends, durable suspension/resume, rollback and general reference services remain
future extensions, with no claim that the bounded local runner implements them.
