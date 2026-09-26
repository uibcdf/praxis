# Praxis

**Praxis is the Methodological Context / Know-how component of the MOLI Platform.**

Praxis represents reusable scientific know-how independently of any single DiscoveryProject or modeling implementation.

Its central distinction is:

> **Capability = WHAT we know how to do.**  
> **Protocol = HOW we reproducibly do it.**

## Role in MOLI

```text
Scientific Context
       │
       ├── Sabueso  — Knowledge
       ├── Praxis   — Know-how
       └── Nextia   — Discovery
```

A Capability describes a semantic scientific ability, its applicability, contracts, validation, limitations, and available implementations.

A Protocol is a reproducible implementation of a Capability and may orchestrate MolSysSuite components and external scientific engines.

Praxis does not replace scientific APIs and must not hide expert access to them.

## Methodological learning

```text
scientific need
      ↓
APIs / tools
      ↓
ad-hoc workflow
      ↓
formalized Protocol
      ↓
validation / generalization
      ↓
Capability
```

Successful project execution does not automatically create validated methodology. Promotion into reusable Praxis know-how is explicit and gated.

## Status

This repository establishes the implementation home for Praxis. APIs and storage formats are intentionally not frozen yet.

The normative conceptual definition is maintained in [MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/tree/main/architecture_1.0).

## Initial design

See the [Initial methodological slice](devguide/INITIAL_SLICE.md) proposal and [implementation issue](https://github.com/uibcdf/praxis/issues/1).
