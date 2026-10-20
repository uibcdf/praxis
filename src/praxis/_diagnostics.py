"""Diagnostics are presentation; retained findings remain the methodological authority."""

from pathlib import Path


def advise(code):
    from smonitor import emit
    from smonitor.integrations import register_provider

    try:
        register_provider(Path(__file__).resolve().parent, provider="praxis")
        emit("WARNING", "", code=code, source="praxis", category="methodology")
    except Exception:
        # A presentation failure must not replace a native scientific exception
        # or the authoritative retained finding.
        return
