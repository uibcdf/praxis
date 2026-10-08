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

Praxis now includes an experimental local Python implementation: a versioned
catalog with explicit admission/assessment/suitability history, recorded selection
policies, typed quantity contracts, bounded composition and human gates, method
records, physical benchmarks/reanalysis, audit, replay preflight and Markdown/HTML
reports. APIs and storage formats are not frozen.

The [first implementation guide](devguide/FIRST_SLICE.md) explains the boundaries
and the optional Recorda and Ackredit integrations. Bundled hydrogen-refinement
definitions retain their pending adapters and checks; no executable hydrogen engine
or scientific validation is claimed.

For development, provision `devtools/conda-envs/development_env.yaml` and install this
checkout with `python -m pip install --no-deps --no-build-isolation --editable .`.
Run `python examples/local_comparison.py /tmp/praxis-example` for the fictional
paired-coordinate fixture. With MolSysMT provisioned, run
`python examples/molsysmt_comparison.py /tmp/praxis-molecular LOCAL_PDB` for a real
C-alpha RMSD exercise, physical metrics and reports. These do not certify methods
or rank fitted and fixed-frame observables as interchangeable.

The [implementation checkpoint](devguide/IMPLEMENTATION_CHECKPOINT.md) records
remaining shared-boundary, hydrogen-provider and publication work. A private
noarch Conda recipe and dependency preflight are provided for development;
no public installation or release is claimed.

Python metadata admits 3.11–3.14. Local development uses Python 3.14; Linux and
macOS CI lanes are configured, with support qualification still pending.
Praxis has no published installation route yet.

First drafts of the [Capability and Protocol proposal templates](devguide/templates/README.md)
provide a starting point for describing and reviewing experimental methodology.

The [initial programming design](devguide/pending_proposals/initial_implementation_design.md)
records the proposed package structure and open decisions for discussion.

The normative conceptual definition is maintained in [MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/tree/main/architecture_1.0).

## Initial design

See the [Initial methodological slice](devguide/INITIAL_SLICE.md) proposal and [implementation issue](https://github.com/uibcdf/praxis/issues/1).
