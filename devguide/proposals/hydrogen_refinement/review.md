# Technical review of hydrogen submissions, revision 2

Date: 2026-10-08. Reviewer: Codex, automated technical/design review, without human
scientific admission authority. Reviewed: Capability @2 and Hydride/OpenMM @2 above,
using proposal templates revision 2. Outcome: complete candidate submissions for
discussion; clarification and provider qualification required before execution.
This is not scientific validation, a human admission or a promotion.

The common contract preserves the assigned chemical state and permits only explicit
H coordinate changes. Full environment, units, periodic convention, original
correspondence, actual changes, reports and stopping cause are present. The two
procedures remain scientifically distinct, their tradeoffs are proposals, and
model-specific energies are not ranked against one another.

Version 2 corrects a machine-model gap: throughout preservation now has a mandatory
runtime requirement with instrumented/independent, invocation/attempt-scoped evidence.
Final restoration and endpoint equality cannot pass it. Report/correspondence outputs
are mandatory. Version 1 is unchanged; `load_bundled(version="2")` selects new drafts.

Hydride restriction must resolve the actual API/version and protected H sharing a
rotatable group. OpenMM requires exact model coverage and minimization-specific
freezing qualification. Both need precision budgets and provider-owned checkers.
Existing preparation examples and core Praxis tests establish neither guarantee.
See [MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323) for provider work.

Acceptance to request from providers: exact configuration/model schema; immutable
input/output references; mappings/units; permitted motion and full environment;
throughout evidence for every declared step; native failure and nonconvergence
records; measured reference-case checks. Praxis will then register a new exact binding
and scoped assessments without automatically promoting the definitions.

Remaining human decisions: appoint scientific maintainers/admission authority,
review candidate scientific restrictions, choose qualification cases/criteria and
approve a compatible model/parameterization. This document records those needs rather
than inventing their answers.
