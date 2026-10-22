"""Fresh-process receiving of application policy and bounded methodological advice."""

import os
import subprocess
import sys
import textwrap

import pytest


def run_fresh(code, tmp_path, *arguments):
    completed = subprocess.run(
        [sys.executable, "-B", "-c", textwrap.dedent(code), *arguments],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


@pytest.mark.parametrize("setup", ["unconfigured", "application", "project"])
def test_import_first_request_and_repeated_advice_preserve_setup(tmp_path, setup):
    run_fresh(
        """
        import logging, sys, warnings
        from pathlib import Path
        import praxis
        assert "smonitor" not in sys.modules
        import smonitor
        from praxis._diagnostics import advise
        from smonitor.integrations import register_provider
        manager = smonitor.get_manager()
        setup = sys.argv[1]
        assert not manager._policy_configured and not manager._handlers
        if setup == "application":
            smonitor.configure(level="CRITICAL", profile="qa", handlers=[],
                capture_logging=False, capture_warnings=False, capture_exceptions=False,
                run_id="application-run", session_id="application-session")
            # The compatibility emitter may add a console even after explicit handlers=[].
            # Give the configured application its own sink, which must be preserved.
            class Sink:
                name = "application"
                def handle(self, event, **kwargs):
                    pass
            manager.add_handler(Sink())
        elif setup == "project":
            Path("_smonitor.py").write_text(
                'SMONITOR = {"level": "CRITICAL", "profile": "qa", '
                '"capture_logging": False, "capture_warnings": False, '
                '"capture_exceptions": False}\\n')
        hooks = (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        before = manager.config, manager._policy, tuple(manager._handlers)
        if setup == "unconfigured":
            advise("PRAXIS-CHECKER-ERROR")
            assert not manager._policy_configured
            assert manager._handlers  # Retained compatibility console, not pure registration.
            assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        for _ in range(2):
            request = praxis.MethodRequest(praxis.MethodRef("capability", "fixture", "1"),
                                          {"number": 1})
            assert request.inputs == {"number": 1}
            root = Path(praxis.__file__).resolve().parent
            register_provider(root, provider="praxis")
            advise("PRAXIS-CHECKER-ERROR")
            advise("PRAXIS-RECORDING-GAP")
        assert manager._policy_configured
        assert not manager.config.capture_logging
        assert not manager.config.capture_warnings
        assert not manager.config.capture_exceptions
        assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        if setup == "application":
            assert manager.config is before[0] and manager._policy is before[1]
            assert tuple(manager._handlers) == before[2]
            assert manager._run_id == "application-run"
            assert manager._session_id == "application-session"
        if setup != "unconfigured":
            assert manager.config.level == "CRITICAL" and manager.config.profile == "qa"
        """,
        tmp_path,
        setup,
    )


@pytest.mark.parametrize("profile", ["user", "dev", "qa", "agent"])
@pytest.mark.parametrize("boundary", ["checker", "recording"])
@pytest.mark.parametrize(
    "delivery", ["normal", "filtered", "emit_failure", "registration_failure", "import_failure"]
)
def test_real_advice_excludes_enclosing_payload_and_keeps_safe_hint(
    tmp_path, profile, boundary, delivery
):
    run_fresh(
        """
        import builtins, sys
        from contextlib import contextmanager
        import praxis, smonitor
        from local_comparison import build_fixture, CAPABILITY, INPUT_CHECK, RMSD, RMSD_BINDING
        from praxis.errors import RecordingError
        from praxis.recording import NoRecorder
        class Sink:
            name = "application"
            def __init__(self):
                self.events = []
            def handle(self, event, **kwargs):
                self.events.append(event)
        sink = Sink()
        manager = smonitor.configure(profile=sys.argv[1], handlers=[sink], event_buffer_size=20, args_summary=True,
            capture_logging=False, capture_warnings=False, capture_exceptions=False)
        if sys.argv[3] == "filtered":
            manager.configure(level="CRITICAL")
        before = manager.config, manager._policy, tuple(manager._handlers)
        catalog, context = build_fixture("fixture")
        inputs = {"left": [[0, 0, 0]], "right": [[1, 0, 0]]}
        class NativeError(ValueError):
            def __str__(self):
                raise AssertionError("native exception text was collected")
        native = NativeError()
        def fails(*args):
            raise native
        if sys.argv[2] == "checker":
            registry = praxis.Extensions()
            for ref, checker in context.extensions.checkers.items():
                registry.register_checker(ref, fails if ref == INPUT_CHECK else checker)
            context.extensions = registry
        else:
            recording_failure = RecordingError("synthetic private recording content")
            class FailedRecorder(NoRecorder):
                def reference(self, path, identifier):
                    return {"id": identifier}
                @contextmanager
                def operation(self, name, **kwargs):
                    raise recording_failure
                    yield
            context.recorder = FailedRecorder()
            prepared = praxis.prepare(praxis.MethodRequest(CAPABILITY, inputs,
                protocol_ref=RMSD, binding_ref=RMSD_BINDING), catalog=catalog, context=context)
        def broken(*args, **kwargs):
            raise OSError("synthetic diagnostic failure")
        if sys.argv[3] == "emit_failure":
            smonitor.emit = broken
        elif sys.argv[3] == "registration_failure":
            smonitor.integrations.register_provider = broken
        elif sys.argv[3] == "import_failure":
            original_import = builtins.__import__
            def failed_import(name, globals=None, locals=None, fromlist=(), level=0):
                if name == "smonitor" and "emit" in fromlist:
                    raise ImportError("synthetic presentation import failure")
                return original_import(name, globals, locals, fromlist, level)
            builtins.__import__ = failed_import
        @smonitor.signal(tags=["private-tag"],
            extra_factory=lambda args, kwargs: {"private": "enclosing-scientific-content"})
        def application_call(scientific_argument):
            if sys.argv[2] == "checker":
                result = praxis.assess_applicability(catalog.get(CAPABILITY), catalog.get(RMSD),
                    inputs, {}, context.extensions)
                assert result.outcome == "undetermined"
                assert any(f.outcome == "checker_error" for f in result.findings)
                assert "enclosing-scientific-content" not in str(result.to_dict())
            else:
                try:
                    praxis.execute(prepared, catalog=catalog, context=context, identifier="gap")
                except RecordingError as error:
                    assert error is recording_failure
                else:
                    raise AssertionError("native RecordingError was replaced")
                attempt = context.records.attempt("gap")
                assert attempt.recording_status == "gap" and attempt.operational_status == "failed"
                assert "synthetic private recording content" not in str(attempt.to_dict())
        policy_before = smonitor.get_capture_policy()
        with smonitor.diagnostic_scope(smonitor.CapturePolicy(), safe_extra={"operation_id": "op-13"}):
            application_call("enclosing-scientific-content")
        assert smonitor.get_capture_policy() == policy_before
        assert manager.config is before[0] and manager._policy is before[1]
        assert tuple(manager._handlers) == before[2]
        if sys.argv[3] != "normal":
            assert not sink.events
            sys.exit(0)
        events = [e for e in sink.events if (e.get("code") or "").startswith("PRAXIS-")]
        assert len(events) == 1, sink.events
        event = events[0]
        assert event["context"] is None, event
        assert event["tags"] is None
        assert event["extra"]["operation_id"] == "op-13"
        assert event["extra"]["hint"].startswith("Inspect the retained")
        assert event["message"]
        assert "enclosing-scientific-content" not in str(event)
        assert "private-tag" not in str(event)
        assert manager.config is before[0] and manager._policy is before[1]
        assert tuple(manager._handlers) == before[2]
        """,
        tmp_path,
        profile,
        boundary,
        delivery,
    )
