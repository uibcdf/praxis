# Latest public support-provider receiving

Accepted receiving decision: [Praxis #14](https://github.com/uibcdf/praxis/issues/14)
(closed). Qualification/artifact retention: [Praxis #9](https://github.com/uibcdf/praxis/issues/9).
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
The [0.1.1 source acceptance](releases/0.1.1.md) passed all eight latest-provider
cells and all eight installed Conda cells on Linux x86_64/macOS arm64 and Python
3.11–3.14, plus the original Linux 3.14 wheel. All 17 JUnit reports retain 213
passes and only the optional absent-MolSysMT skip. Recorda/Ackredit tests execute.
The [tracked receipt](evidence/release_0_1_1.json) and compressed records preserve
identities and full scope. The receiving handoff was delivered to MolSysSuite #135.
This decision admits these versions without automatically admitting later providers,
refreshing the shared environment, publishing a package or supplying scientific validation.

## Historical receiving cohort — 2026-10-20

On 2026-10-20 Liliana requested compatibility with the latest published support
providers: ArgDigest 0.16.0, SMonitor 0.21.0 and DepDigest 0.15.1. Preserve the
previous runtime floors and admit these qualified minors through bounded upper
limits. Current receiving must execute existing contracts against public provider
files and verify their identities; widened metadata alone is not evidence.

At that checkpoint, the public Recorda 0.3.0 archive retained its original provider
ceilings. Source compatibility did not rewrite that archive or claim a new public
release. A later Recorda release was required before a public-only joint install
could select that new cohort. The subsequent public Recorda 0.3.3/current cohort
above resolves the receiving limitation; the original 0.3.0 files remain unchanged.

No provider scientific implementation, component version, existing release plan,
tag or public file is changed. Joint editable-source receiving does not claim
an installed consumer Conda release or broader scientific qualification.

The qualified historical cohort used these original public files:

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

At that checkpoint, the original installed lanes retained the legacy provider cohort
and public Recorda 0.3.0. The separate latest lane tested mandatory providers and
Ackredit while omitting incompatible public Recorda 0.3.0. Its omitted recording
tests remain explicit in the historical receipt, without replacing joint editable
recording evidence. The current lane includes compatible public Recorda 0.3.3.

## Current matrix policy

Internal pushes run the latest Linux/Python 3.14
cell; PR, scheduled and manual workflows run all eight Linux/macOS arm64 ×
Python 3.11–3.14 cells. The release preflight requires all eight latest cells
as well as the existing installed artifact/coverage gates. Run an exact-head
manual workflow before release if a routine push provides only one latest cell.
Regression tests in `tests/test_release_route.py` reject both legacy-only
receiving and a lone routine latest cell as release qualification.
