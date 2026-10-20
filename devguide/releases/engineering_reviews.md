# Engineering adoption for experimental Praxis 0.1.0

Owner: [Praxis #9](https://github.com/uibcdf/praxis/issues/9).
Scope: the sequential local methodology package, not scientific admission or the
pending shared MOLI execution contract. MOLI registered `python-package` through
[PR #64](https://github.com/uibcdf/moli/pull/64). All four component review decisions
below are **adopted** for the frozen source
`e253fe76db81b9cb6eaa4db4dc0b78bb60188d39`, supported by
[complete acceptance](https://github.com/uibcdf/praxis/issues/9#issuecomment-6067816955)
and the [release record](0.1.0.md). Their registry mirror remains pending owner
review in [MOLI PR #66](https://github.com/uibcdf/moli/pull/66).

## Python ecosystem applicability

All four governed support libraries have applicable, implemented boundaries:

| Boundary | Provider and implementation | Qualification |
| --- | --- | --- |
| Public request object/JSON normalization | ArgDigest 0.15.0, `_arguments.request_values`, lazily used by `MethodRequest` | Public invalid object/non-finite/non-JSON regressions and full installed suite |
| Optional operational providers and numerical bindings | DepDigest 0.13.0, lazy Recorda/Ackredit checks and binding dependency assessment | Catalog import without providers, missing-engine abstention, installed optional-provider checks |
| Checker errors and recording gaps | SMonitor 0.19.0, `_diagnostics.advise` and count-free provider codes | Checker/recording failure regressions preserve retained findings/native failures; diagnostic transport cannot replace the method record |
| Duration, input/parameter/output and metric quantities | PyUnitWizard 0.28.1 sealed `QuantityRecord`, explicit field/unit handshake | Non-default application policy before import/first use; fixed-unit conversion; tampering, dimension/field/bounds checks |

Praxis creates no separate Pint registry and never configures global units on import.
Its persisted quantity schema delegates sealing/decoding to PyUnitWizard; descriptions
do not substitute for executable checks. Runtime dependency floors/ceilings match
all maintained Conda routes; exact installed versions and public channels are recorded.
No support-library cycle or bounded applicability exception is needed.

Development uses Python 3.14, Ruff 0.16.5, published pytest-receptor 1.2.1
(`llm` locally, `ci` in CI) and published gh-run-receptor 1.2.0 for this review's inspection.
GitHub conclusions and downloaded JUnit/artifacts are independently checked.
These tools remain development dependencies. Decision: **adopted**. The complete
exact-source installed suite and support-library adoption regressions passed.

## Operating systems

Qualified support for the experimental local package: **Linux x86_64 and macOS
arm64**, Python **3.11–3.14**. No Windows or Intel macOS claim. All eight lanes
install one shared noarch artifact with published runtime and optional providers;
macOS asserts arm64 at runtime. Each executes the full required suite, with only
the explicit optional MolSysMT example allowed to skip when absent.
The same matrix runs on pushes/PRs, weekly and manually. Decision: **adopted**.
All eight exact-source lanes passed, each with 154 tests and one optional MolSysMT
skip; Recorda/Ackredit integrations did not skip. Earlier candidate receipts remain
historical after a source change and do not qualify a future candidate.

## Coverage

The complete installed Conda suite is instrumented in each lane. Routine Linux
Python 3.14 coverage is uploaded on main using OIDC after that complete installed
lane passes. Other platform queues do not delay this report; all eight installed
lanes remain mandatory for release qualification.
The mapper verifies installed source/resource hashes before converting paths to
`src/praxis`; it preserves every line hit and aggregate statistic. It rejects an
unrelated artifact/package or changed source. No favorable flag, source exclusion
or minimum percentage is introduced. MolSysMT-specific behavior remains outside
this provider-free coverage scope.

Codecov acceptance was independently observed for the tagged main source
`e253fe76db81b9cb6eaa4db4dc0b78bb60188d39`: the
[complete report](https://app.codecov.io/gh/uibcdf/praxis/commit/e253fe76db81b9cb6eaa4db4dc0b78bb60188d39)
measured 2,450 lines, with 2,088 hits (85.22%). The unflagged upload from
[run 37806795166](https://github.com/uibcdf/praxis/actions/runs/37806795166) was accepted
at 2026-10-08 16:16:48 UTC; the live main SVG independently displayed a percentage.
Decision: **adopted** for this complete installed Linux report, with main pushes,
manual runs and weekly cadence. The README uses the dynamic repository percentage.
This dated report does not certify a later source commit; new exact-candidate gates
and uploads remain required. #9 retains subsequent report identities and acceptance.

## Distribution and release route

Primary route: Conda `uibcdf` + `conda-forge`; no public PyPI claim. Wheel/sdist
are retained for private qualification. The pure Python package is noarch, with
six bundled JSON definitions and its Python code inventoried per archive.
Each route's runtime version and resource bytes are checked independently; the
source archive also retains matching tests, workflows, tooling and documentation.
Missing resources, stale versions, stale dependency floors and ambiguous installed
metadata have negative regressions. Tests verify representative bundled loading
and required runtime behavior from the installed artifact.

`build_and_upload_conda_packages.yaml` calls reviewed shared builder v2.3.0 without
upload. `publish_conda.yaml` is the separate exact-file route: manual dispatch is
read-only by default; it checks a successful exact-head producer and every required
job, downloads its original archive, checks source/version/resources/digest and
refuses an occupied file coordinate under any label. A writing dispatch also
requires the matching public `X.Y.Z` tag and `ANACONDA_UIBCDF_TOKEN`. The shared
exact-upload primitive writes once without rebuilding, converting or forcing;
independent bounded queries observe the exact public main-label file and digest,
including after an uncertain write. Tests reject occupied staging coordinates,
changed public bytes, missing platform lanes and skipped coverage.

The write client is published anaconda-client 1.15.0, used only when writing;
credentials remain CI secrets. The successful
[hosted read-only check](https://github.com/uibcdf/praxis/actions/runs/37833466411)
recorded effective CI credential availability without exposing its value. Presence
does not verify write authorization.
No package is advertised until independent public registry and clean channel-install
evidence exist. Source installation remains the development route. Decision:
**adopted for the reviewed pre-publication route**, with its hosted check passed;
the policy explicitly allows an incubating package with no publication claim.
Actual upload, poststate and clean public installation remain separate release work.

Tagging a technically accepted experimental source milestone does not upload a
package: the publication workflow is manual only. No Zenodo archival intent or
DOI claim is included in 0.1.0; revisit archival metadata when that route is adopted.

## Evidence and registry synchronization

The [release record](0.1.0.md) and #9 retain exact source/tag identities, original
artifact digests, resolved closures, authoritative run/JUnit conclusions, Codecov
acceptance and read-only publication readiness. The public tag remains unchanged.
PR #66 proposes the adopted component review states and supported OS/architecture
for MOLI owner review. As of 2026-10-08 its governance passes; its global guide
audit is blocked by Nextia/MOLI Agent canonical-copy drift tracked in
[MOLI #60](https://github.com/uibcdf/moli/issues/60). Registry synchronization is
not complete until that PR merges. Later documentation-only commits do not
change the qualified source, rebuild its files or supply release-gate evidence.
