# MOLI component coordination

This repository is directly governed by the MOLI platform for shared cross-component contracts.

Before cross-component or architectural work, read `MOLI_GUIDE.md`. Its canonical source is `uibcdf/moli/MOLI_GUIDE.md`; do not intentionally diverge the local copy.

This repository remains authoritative for its own implementation, tests, local API, scientific behavior, releases, and component-specific development decisions.

Use `uibcdf/moli` when a change affects a shared MOLI contract, terminology, architecture boundary, or coordination policy. Report provider-specific limitations to the provider repository and cross-link consumer work.

For a needed fix in another repository, use its issue when no fix is ready or
submit a ready fix as a pull request for owner review. If urgent work is done
by or directly with Diego or Liliana, ask them whether to use a direct push,
pull request or issue; direct push needs explicit permission. Follow
`MOLI_GUIDE.md#cross-component-feedback`.

Do not expose confidential vertical-pilot content in public issues or documentation.

Report defects and needs in their owning issues; put source behavior, edge
cases and workarounds in code, regression tests and technical documentation,
not in `AGENTS.md`. Add an instruction here or in a nested `AGENTS.md` only
when normal repository review accepts a lasting rule about how contributors
or agents should work across future tasks and existing guidance is insufficient.
Use an adoption issue only if that accepted working instruction cannot be
placed with the fix or decision. Do not ask for a separate `AGENTS.md` decision
for every defect. Propose cross-component adoption only for an accepted
working instruction with shared evidence. Follow
`MOLI_GUIDE.md#durable-instructions-for-development-agents`. For work in the
developer guide, also read `devguide/AGENTS.md`.
