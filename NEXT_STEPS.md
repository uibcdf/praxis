# Initial Implementation Questions

This is a temporary implementation checkpoint, not frozen architecture.

Before committing to a public API, decide and prototype:

- minimal serializable Capability representation;
- minimal serializable Protocol representation;
- stable identity/version semantics;
- validation-record representation;
- applicability/precondition model;
- Protocol registry/discovery;
- Protocol selection policy interface;
- execution adapter boundary to MolSysSuite/external engines;
- provenance requirements;
- first end-to-end Capability/Protocol examples.

Prefer one or two real scientific workflows over a broad abstract framework. Keep implementation local-first and avoid premature service decomposition.
