"""Semantic snapshots plus an explicit optional Recorda boundary adapter."""

import hashlib
from contextlib import contextmanager
from dataclasses import replace

from .catalog.storage import FileStore
from .errors import RecordingError
from .execution.reports import AttemptRecord, PreparedInvocation


class MethodRecords:
    """Local method-specific snapshots; no project graph or operation-event system."""

    def __init__(self, directory):
        self.store = FileStore(directory)

    def save_prepared(self, prepared):
        return self.store.put({"kind": "prepared", "id": prepared.identifier}, prepared)

    def prepared(self, identifier):
        return PreparedInvocation.from_dict(self.store.get({"kind": "prepared", "id": identifier}))

    def save_attempt(self, attempt):
        stage = "started" if attempt.finished is None else "finished"
        return self.store.put(
            {"kind": "attempt", "id": attempt.identifier, "stage": stage}, attempt
        )

    def attempt(self, identifier):
        try:
            document = self.store.get({"kind": "attempt", "id": identifier, "stage": "finished"})
        except FileNotFoundError:
            document = self.store.get({"kind": "attempt", "id": identifier, "stage": "started"})
            return replace(
                AttemptRecord.from_dict(document),
                operational_status="incomplete",
                recording_status="incomplete",
                contract_status="unassessed",
            )
        return AttemptRecord.from_dict(document)


class Unrecorded:
    def output(self, name, value):
        pass

    def correlation(self):
        return None


class NoRecorder:
    """Method snapshots still persist; no claim of recorded operation coverage."""

    @contextmanager
    def operation(self, name, *, inputs=None, parameters=None, implementation=None):
        yield Unrecorded()


class RecordaRecorder:
    """Borrow an application-owned active session, without starting or stopping it."""

    def __init__(self, session):
        from depdigest import check_dependency

        check_dependency(
            "recorda", caller="Praxis operation recording", pypi_name=None, conda_channel="uibcdf"
        )
        self.session = session

    @contextmanager
    def operation(self, name, *, inputs=None, parameters=None, implementation=None):
        boundary = self.session.operation(
            name,
            inputs=inputs,
            parameters=parameters,
            implementation=implementation,
            profile="praxis.method",
        )
        try:
            operation = boundary.__enter__()
        except Exception as error:
            raise RecordingError("Recorda could not start the declared operation") from error
        try:
            yield _RecordaOperation(self.session, operation)
        except BaseException as error:
            # Recorda preserves the native exception if terminal persistence also fails.
            boundary.__exit__(type(error), error, error.__traceback__)
            raise
        else:
            try:
                boundary.__exit__(None, None, None)
            except Exception as error:
                raise RecordingError("Recorda could not finish the declared operation") from error

    def reference(self, path, identifier):
        from recorda import Reference

        return Reference(
            "praxis", identifier, "snapshot/0.1", hashlib.sha256(path.read_bytes()).hexdigest()
        )

    def coverage(self, correlations):
        from recorda import inspect

        if not correlations:
            return "omitted_by_policy"
        record = inspect(self.session.path)
        statuses = {item["id"]: item["status"] for item in record.operations}
        if record.problems or any(
            statuses.get(item["operation_id"]) not in {"succeeded", "failed"}
            for item in correlations
        ):
            return "gap"
        return "complete_declared_boundaries"


class _RecordaOperation:
    def __init__(self, session, operation):
        self.session = session
        self.operation = operation

    def output(self, name, value):
        try:
            self.operation.output(name, value)
        except Exception as error:
            raise RecordingError("Recorda could not retain a declared output") from error

    def correlation(self):
        # Excluded policies do not produce an operation ID: do not claim observation.
        identifier = getattr(self.operation, "id", None)
        if identifier is None:
            return None
        return {
            "session_id": self.session.id,
            "operation_id": identifier,
            "scope": "declared boundary only",
        }
