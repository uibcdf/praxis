# Engineering adoption for experimental Praxis 0.1.0

Owner: [Praxis #9](https://github.com/uibcdf/praxis/issues/9).
Scope: the sequential local methodology package, not scientific admission or the
pending shared MOLI execution contract. MOLI registered `python-package` through
[PR #64](https://github.com/uibcdf/moli/pull/64); registry review states initially
remain pending. Proposed component decisions below require exact-candidate evidence.

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
(`llm` locally, `ci` in CI) and published gh-run-receptor 1.0.0 for inspection.
GitHub conclusions and downloaded JUnit/artifacts are independently checked.
These tools remain development dependencies. Proposed decision: **adopted** once
the new exact-head installed suite, including adoption regressions, passes.

## Operating systems

Proposed support for the experimental local package: **Linux x86_64 and macOS
arm64**, Python **3.11–3.14**. No Windows or Intel macOS claim. All eight lanes
install one shared noarch artifact with published runtime and optional providers;
macOS asserts arm64 at runtime. Each executes the full required suite, with only
the explicit optional MolSysMT example allowed to skip when absent.
The same matrix runs on pushes/PRs, weekly and manually. Proposed decision:
**adopted**, conditioned on the current candidate's successful installed matrix;
earlier exact-candidate receipts are historical after a source change.

## Coverage

The complete installed Conda suite is instrumented in each lane. Routine Linux
Python 3.14 coverage is uploaded on main using OIDC after all installed lanes pass.
The mapper verifies installed source/resource hashes before converting paths to
`src/praxis`; it preserves every line hit and aggregate statistic. It rejects an
unrelated artifact/package or changed source. No favorable flag, source exclusion
or minimum percentage is introduced. MolSysMT-specific behavior remains outside
this provider-free coverage scope.

Codecov acceptance must be observed separately from workflow configuration or
upload completion. Until a recent complete main report and live percentage are
observable, adoption is **partial** and the badge is withheld. Record the measured
source commit, scope, actual acceptance/upload time and cadence in #9 when adopting.

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
credentials remain CI secrets. No repository publication secret is currently listed. The hosted preflight records
only whether an effective CI credential is available, without exposing its value.
No package is advertised until independent public registry and clean channel-install
evidence exist. Source installation remains the development route. Proposed adoption:
**adopted for the reviewed pre-publication route** after its read-only hosted check;
the policy explicitly allows an incubating package with no publication claim.
Actual upload, poststate and clean public installation remain separate release work.

Tagging a technically accepted experimental source milestone does not upload a
package: the publication workflow is manual only. No Zenodo archival intent or
DOI claim is included in 0.1.0; revisit archival metadata when that route is adopted.

## Evidence and registry synchronization

Record candidate identities, artifact digests, resolved closures, authoritative
run/JUnit conclusions, Codecov acceptance and the read-only publication result in
#9. Keep the final source commit unchanged after qualification. Propose the decided
review states and supported OS/architecture in a MOLI PR for its owner's review;
do not silently modify MOLI main or report a pending merge as completed adoption.
