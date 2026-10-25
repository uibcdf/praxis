# Latest public support-provider receiving

Current owner: [Praxis #14](https://github.com/uibcdf/praxis/issues/14).
Workspace coordination: [MolSysSuite #135](https://github.com/uibcdf/molsyssuite/issues/135).
The completed earlier cohort stays under Praxis #10 / MolSysSuite #82 / MOLI #40.

## Current receiving cohort — 2026-10-24

Praxis admits ArgDigest 0.17, SMonitor 0.22 and PyUnitWizard 0.29, preserving
the previous floors with bounds `<0.18`, `<0.23` and `<0.30`, respectively.
DepDigest remains `>=0.13,<0.16`. Metadata and the candidate Conda recipe agree.

Development and latest-support environments select original public files:

| Provider | File | SHA-256 |
| --- | --- | --- |
| ArgDigest | `argdigest-0.17.0-py_0.tar.bz2` | `9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1` |
| SMonitor | `smonitor-0.22.0-py_0.tar.bz2` | `bbf5890bed4ea657044b904f07d3cef137d474f0862ef5f35b063db9c8f0c949` |
| DepDigest | `depdigest-0.15.1-py_0.tar.bz2` | `2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850` |
| PyUnitWizard | `pyunitwizard-0.29.0-py_0.tar.bz2` | `9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34` |
| Recorda | `recorda-0.3.3-py_0.tar.bz2` | `fcee216130bca444e92e195fc38f8ef24fb501439cd123638bc11fa8e5df76ea` |

Public Recorda 0.3.3 permits this cohort, so latest-support now runs recording
as well as Ackredit 0.12.0 attribution tests. CI verifies all five public Conda
identities and runtime import origins. Legacy build/installed-test environments
retain their older pins and published Recorda 0.3.0 to protect floor coverage.
The current cohort is a receiving decision for these versions, not automatic
admission of later providers. It does not select a release or publish Praxis.

## Historical receiving cohort — 2026-10-20

On 2026-10-20 Liliana requested compatibility with the latest published support
providers: ArgDigest 0.16.0, SMonitor 0.21.0 and DepDigest 0.15.1. Preserve the
previous runtime floors and admit these qualified minors through bounded upper
limits. Current receiving must execute existing contracts against public provider
files and verify their identities; widened metadata alone is not evidence.

At that checkpoint, the public Recorda 0.3.0 archive retained its original provider ceilings. Source
compatibility does not rewrite that archive or claim a new public release. A
future separately authorized Recorda release is required before a public-only
joint install can select the new cohort. Praxis's old-cohort recording tests and
the latest mandatory-provider tests therefore have distinct scopes.

No provider scientific implementation, component version, existing release plan,
tag or public file is changed. Joint editable-source receiving does not claim
an installed consumer Conda release or broader scientific qualification.

The qualified current cohort uses original public files:

| Provider | File | SHA-256 |
| --- | --- | --- |
| ArgDigest | `argdigest-0.16.0-py_0.tar.bz2` | `e82d82680d79ae3d5df9917b1662d2855ed8485128943b72ddec87a5769a467d` |
| SMonitor | `smonitor-0.21.0-py_2.tar.bz2` | `62b6cbae37f7fa06374af87923792f00253020955d000294b1a7d37eb9d04e56` |
| DepDigest | `depdigest-0.15.1-py_0.tar.bz2` | `2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850` |

Joint editable receiving on Linux/Python 3.14.8 passed 345 Recorda tests
(including explicitly enabled SMonitor recovery) and 154 Praxis tests. Praxis
skipped its optional real-MolSysMT scenario because that provider is absent; this
is not scientific receiving of MolSysMT. All optional Recorda/Ackredit scenarios
ran in that joint editable receipt. `pip check` passed without exceptions.
Recorda's exact installed-provider checker verified 39 ArgDigest, 40 SMonitor
and 17 DepDigest Python files, all managed by their original public Conda
records; provider imports came from that disposable environment.

Provider selection is a dated, reviewed cohort, not a claim about unreleased
future minors. Preserve receiving evidence when reviewing a later public provider.

At that checkpoint, the original installed lanes retained their legacy provider cohort and published
Recorda 0.3.0, protecting optional recording. A separate `latest_support` lane
installs current Praxis with the exact latest public mandatory providers and
Ackredit; it omits the incompatible public Recorda 0.3.0. Omitted optional
Recorda tests must remain explicit in its receipt and do not replace joint
editable recording evidence. Internal pushes run the latest Linux/Python 3.14
cell; PR, scheduled and manual workflows run all eight Linux/macOS arm64 ×
Python 3.11–3.14 cells. The release preflight requires all eight latest cells
as well as the existing installed artifact/coverage gates. Run an exact-head
manual workflow before release if a routine push provides only one latest cell.
Regression tests in `tests/test_release_route.py` reject both legacy-only
receiving and a lone routine latest cell as release qualification.
