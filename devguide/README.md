# Praxis development guide

[Architecture](ARCHITECTURE.md) and [design boundaries](BOUNDARIES.md) describe
Praxis's conceptual responsibilities within MOLI.

The [first local implementation](FIRST_SLICE.md) documents the experimental Python
API, storage, contracts, composition, real MolSysMT exercise, Recorda/Ackredit adapters,
benchmarks/reanalysis and replay. The [0.1.0 release record](releases/0.1.0.md)
connects exact-source installed acceptance to completed issue criteria and remaining
provider/shared/publication decisions. [Next steps](../NEXT_STEPS.md) is the current
work queue. The [implementation checkpoint](IMPLEMENTATION_CHECKPOINT.md) preserves
the earlier, pre-release development state.

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
concern the proposed design; implementation and scientific validation remain pending.

[Filled hydrogen submissions and technical review](proposals/hydrogen_refinement/capability.md)
complement the hypothetical stress cases; their provider adapters and scientific
qualification remain pending.
