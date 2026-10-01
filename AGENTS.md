# MOLI component coordination

This repository is directly governed by the MOLI platform for shared cross-component contracts.

Before cross-component or architectural work, read `MOLI_GUIDE.md`. Its canonical source is `uibcdf/moli/MOLI_GUIDE.md`; do not intentionally diverge the local copy.

This repository remains authoritative for its own implementation, tests, local API, scientific behavior, releases, and component-specific development decisions.

Use `uibcdf/moli` when a change affects a shared MOLI contract, terminology, architecture boundary, or coordination policy. Report provider-specific limitations to the provider repository and cross-link consumer work.

Do not expose confidential vertical-pilot content in public issues or documentation.

When an incident reveals a reusable development rule, assess its scope. Put an
accepted repository-wide rule here and a directory-specific rule in the
appropriate nested `AGENTS.md` in the same change; otherwise track adoption
in an owned issue. Follow `MOLI_GUIDE.md#durable-instructions-for-development-agents`.
Report a potentially shared lesson to the owning governance issue. For work
in the developer guide, also read `devguide/AGENTS.md`.
