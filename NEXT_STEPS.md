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
- [Praxis #9](https://github.com/uibcdf/praxis/issues/9), governance/publication review: activate the Python-package inventory, obtain
  actual remote installed-package evidence, qualify published dependency closure,
  choose a stable first release and authorize publication. Local/private artifacts
  and configured CI do not establish these outcomes.

Human scientific admission/validation requires actual reviewers and provider evidence;
execution, favorable statistics and core interface fixtures never supply it automatically.
Future statistical methods, broader workflows, parallel backends and reference services
are extensions of the design, not claimed features of this bounded local increment.
