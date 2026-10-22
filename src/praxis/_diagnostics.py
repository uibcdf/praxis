"""Diagnostics are presentation; retained findings remain the methodological authority."""

from pathlib import Path


def advise(code):
    try:
        from smonitor import diagnostic_scope, emit
        from smonitor.integrations import register_provider

        # Fixed advice must not inherit scientific arguments or enclosing frames.
        # Start before provider registration and event construction, not at a sink.
        with diagnostic_scope():
            register_provider(Path(__file__).resolve().parent, provider="praxis")
            emit("WARNING", "", code=code, source="praxis", category="methodology")
    except Exception:
        # A presentation failure must not replace a native scientific exception
        # or the authoritative retained finding.
        return
