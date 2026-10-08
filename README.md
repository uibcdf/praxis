# Praxis

[![Tests](https://github.com/uibcdf/praxis/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/uibcdf/praxis/actions/workflows/tests.yml)
[![Coverage](https://codecov.io/gh/uibcdf/praxis/branch/main/graph/badge.svg)](https://app.codecov.io/gh/uibcdf/praxis)

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

Version **0.1.0** identifies the first experimental local-methodology milestone.
The [release plan](devguide/releases/0.1.0.md) defines its acceptance gates and
known limitations. Exact-source qualification and tag status are recorded in
[Praxis #9](https://github.com/uibcdf/praxis/issues/9); configured CI alone is not
passing evidence. No public Conda package or archival claim is made.

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
noarch Conda recipe and dependency preflight are provided for qualification;
no public installation or release is claimed.

Python metadata admits 3.11–3.14. Local development uses Python 3.14. Qualified releases
of the experimental local package support Linux x86_64 and macOS arm64; their
same-artifact installed matrix and [engineering adoption](devguide/releases/engineering_reviews.md) are recorded in
[Praxis #9](https://github.com/uibcdf/praxis/issues/9). Windows is unclaimed.
macOS support is currently limited to Apple Silicon (arm64).
Intel-based macOS (x86_64) is not part of the supported platform matrix.
Support may be reconsidered if there is demonstrated user demand.
Praxis has no published installation route yet.

Coverage measures the full installed Conda suite on Linux Python 3.14 with published
Recorda/Ackredit providers; the optional MolSysMT example is outside this scope.
Reports upload on main pushes, manual runs and weekly. The first accepted report
measured `fc51272` on 2026-10-08; subsequent report identities are recorded in #9.
The live percentage describes this test scope, not scientific validation.

The package is released under the [MIT license](LICENSE).

First drafts of the [Capability and Protocol proposal templates](devguide/templates/README.md)
provide a starting point for describing and reviewing experimental methodology.

The [initial programming design](devguide/pending_proposals/initial_implementation_design.md)
records the proposed package structure and open decisions for discussion.

The normative conceptual definition is maintained in [MOLI Platform Architecture 1.0](https://github.com/uibcdf/moli/tree/main/architecture_1.0).

## Initial design

See the [Initial methodological slice](devguide/INITIAL_SLICE.md) proposal and [implementation issue](https://github.com/uibcdf/praxis/issues/1).
