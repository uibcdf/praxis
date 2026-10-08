# Implementation checkpoint and remaining decisions

The local implementation now includes the contract, selection/composition,
assessment/suitability and benchmark/reanalysis increments from issues #5–#8,
plus explicit curation, resource profiles, catalog transfer, trace/replay preflight
and a real public MolSysMT workflow. See [the implemented API](devguide/FIRST_SLICE.md)
and [acceptance/remaining scope](devguide/IMPLEMENTATION_CHECKPOINT.md).

Remaining work has concrete owners:

- MolSysMT #323 / Praxis #3: qualify real hydrogen restriction, complete environment,
  model/parameters, original correspondence, precision and throughout enforcement.
  Filled Capability/Hydride/OpenMM submissions and technical review now exist under #4.
- MOLI #28 / Praxis #1/#5/#6: agree the shared invocation/Run/ExecutionPlan and
  semantic-persistence/Recorda partial-commit boundary. Local attempts remain provisional.
- [Praxis #9](https://github.com/uibcdf/praxis/issues/9), engineering/release review:
  MOLI has registered the experimental Python package, public version `0.1.0` is
  selected, and Codecov has accepted complete installed Linux coverage. Complete
  the current candidate's installed matrix and component review decisions, propose
  the matching registry states, then freeze the qualified source. The separate
  public Conda route still requires its effective credential, exact-file write,
  independent poststate and clean channel installation before distribution claims.
  Configured CI and an accepted older-source report do not qualify a changed candidate.

Human scientific admission/validation requires actual reviewers and provider evidence;
execution, favorable statistics and core interface fixtures never supply it automatically.
Future statistical methods, broader workflows, parallel backends and reference services
are extensions of the design, not claimed features of this bounded local increment.

The next milestone is the [0.1.0 candidate](devguide/releases/0.1.0.md).
Its CI builds one unpublished Conda artifact and tests the same bytes on the full
intended matrix, including published Recorda and Ackredit providers.
