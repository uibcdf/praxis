# Praxis development guide

Development is paused as of 2026-10-26. Start with the maintained
[pause checkpoint](CHECKPOINT.md) for the accepted source, five open issues,
owners, resumption conditions and retained artifacts.

[Diagnostic ownership and bounded advice](DIAGNOSTICS.md) records the first-use
baseline, application policy precedence and scoped methodological presentation.

[Architecture](ARCHITECTURE.md) and [design boundaries](BOUNDARIES.md) describe
Praxis's conceptual responsibilities within MOLI.

The [first local implementation](FIRST_SLICE.md) documents the experimental Python
API, storage, contracts, composition, real MolSysMT exercise, Recorda/Ackredit adapters,
benchmarks/reanalysis and replay. The [accepted 0.1.1 record](releases/0.1.1.md)
identifies the public source tag, exact-source installed qualification and original
artifact hashes. The [evidence index](evidence/README.md) links tracked receipts and
full native records. [Next steps](../NEXT_STEPS.md) is the current work queue.
The [0.1.0 release record](releases/0.1.0.md) and
[earlier implementation checkpoint](IMPLEMENTATION_CHECKPOINT.md) preserve their
historical scope; they do not replace the current pause checkpoint.

For any future public GitHub Release, check that the visible title is exactly
the `X.Y.Z` version, matching the tag and project/package version. Keep
descriptions in the release notes. Public source tags 0.1.0/0.1.1 do not claim
that a GitHub Release, public Conda package or archive was published.

At task and release closeout, review temporary test environments, build trees
and downloaded copies. Remove owned disposable resources after their last
needed use; retain exact candidate artifacts and useful evidence with an
owner and review trigger. Follow
`../MOLI_GUIDE.md#temporary-development-resources`.

The [initial programming design](pending_proposals/initial_implementation_design.md)
is a draft for discussing the Python package, catalog, execution, extensions,
audit, benchmarks, reporting, and methodological documentation, including Protocol
tradeoffs and suitable scenarios. It uses hydrogen refinement as a scientific
case and proposes incremental acceptance criteria. Its decisions remain open under
[Praxis #1](https://github.com/uibcdf/praxis/issues/1).

[Capability and Protocol proposal templates](templates/README.md) support
scientific submissions and review, with experimental status and pending work
made explicit.

The [four-Capability stress exercise](stress_tests/design_stress_test.md) contains
four filled Capability proposals, eight Protocol proposals and scenario reviews
covering deterministic, stochastic, human and composed methods. Its conclusions
concern the proposed design. Those eight scientific methods have not been executed
or scientifically validated; later local runner qualification has its separate scope.

[Filled hydrogen submissions and technical review](proposals/hydrogen_refinement/capability.md)
complement the hypothetical stress cases; their provider adapters and scientific
qualification remain pending.
