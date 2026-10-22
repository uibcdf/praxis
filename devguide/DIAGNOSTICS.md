# Diagnostic ownership and bounded advice

Owner: [Praxis #13](https://github.com/uibcdf/praxis/issues/13).
Coordination: [MolI #62](https://github.com/uibcdf/moli/issues/62).

Plain `import praxis` does not import the diagnostic or argument providers.
The first `MethodRequest` loads its explicit ArgDigest JSON pipelines inside a
metadata-only scope and calls `ensure_configured`. This safe first-use baseline
is retained: Praxis disables global logging, warning and exception capture when
no application policy exists. An application configuration already selected
through SMonitor, or a project `_smonitor.py`, takes precedence. Repeated request
construction, provider registration and advice preserve that selected policy.

Checker-error and recording-gap advice now adopts a local `diagnostic_scope()`
before registering the catalog and constructing an event. Both codes use fixed
messages and explicit `metadata_hint` text. Advice excludes enclosing breadcrumb
frames, arguments, ordinary extras and tags. Explicitly approved bounded
`safe_extra` facts from the caller remain available; this is deliberate metadata
selection, not classification of the contents of strings. A scope cannot erase
data collected by the application before entering Praxis advice. The scope ends
on success or diagnostic failure and does not change the caller's capture policy.

SMonitor still chooses handlers, audience, thresholds and routing. A filtered or
failed presentation, including an import or registration failure, leaves the
authoritative methodological finding or retained attempt and native exception
unchanged. Checker exceptions remain unresolved findings; a recording failure
remains a recording gap. Neither becomes a scientific success through an absent
warning. Recorded scientific inputs and results keep their existing contracts.

Pure registration-only execution is **deferred**. Direct advice in an otherwise
unconfigured process retains SMonitor's compatibility console bootstrap, without
configuring global capture hooks. A first request still explicitly chooses its
safe baseline. Adopting `bootstrap_policy=False` only at emission would not remove
that request bootstrap, and the option is unavailable at the supported SMonitor
0.19 floor. Revisit when a concrete embedding application requires no implicit
handler or first-use configuration, with an explicit setup API and receiving
tests for both boundaries. No dependency-floor change is selected here.

Per-audience safe template maps and nonemitting identity export are **not
applicable to this slice**: both current codes already have fixed safe prose and
a shared hint, and Praxis has no diagnostic-bundle export API. Revisit for a
concrete audience or export use case rather than introducing a new adapter now.

`tests/test_diagnostics.py` runs fresh processes for unconfigured, configured and
project-configured first use, repeated registration, both real advice sites,
all four audiences, filtering and emission/registration/import failure. Existing
execution tests additionally protect native scientific errors and retained
methodological outcomes. Qualification uses both admitted public provider
cohorts; [the dated evidence receipt](evidence/diagnostics_13_20261022.json)
records exact installed identities, file verification, results and exclusions.
