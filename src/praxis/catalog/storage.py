"""Immutable local snapshots, atomic admission and content-conflict detection."""

import json
import os
import tempfile
from pathlib import Path

from .._serialization import digest, encode, snapshot
from ..errors import ConflictError, IntegrityError


class FileStore:
    """Local JSON objects indexed by a digest of identity, never by user path fragments."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def path(self, identity):
        return self.directory / f"{digest(identity)}.json"

    def put(self, identity, document):
        envelope = {
            "schema": "praxis.snapshot/0.1",
            "identity": snapshot(identity),
            "digest": digest(document),
            "document": snapshot(document),
        }
        destination = self.path(identity)
        descriptor, temporary = tempfile.mkstemp(prefix=".praxis-", dir=self.directory)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(encode(envelope))
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, destination)
            except FileExistsError:
                if self.get(identity) != envelope["document"]:
                    raise ConflictError("An exact identity already has different content") from None
        finally:
            Path(temporary).unlink(missing_ok=True)
        return destination

    def get(self, identity):
        path = self.path(identity)
        envelope = self._read(path)
        if envelope["identity"] != snapshot(identity):
            raise IntegrityError("Stored identity does not match the requested identity")
        return envelope["document"]

    def _read(self, path):
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
            if type(envelope) is not dict or set(envelope) != {
                "schema",
                "identity",
                "digest",
                "document",
            }:
                raise IntegrityError("Invalid snapshot envelope")
            if envelope["schema"] != "praxis.snapshot/0.1":
                raise IntegrityError("Unsupported snapshot schema")
            if envelope["digest"] != digest(envelope["document"]):
                raise IntegrityError("Stored document content has changed")
            return envelope
        except (ValueError, TypeError, KeyError) as error:
            raise IntegrityError("Unreadable snapshot envelope") from error

    def documents(self):
        for path in sorted(self.directory.glob("*.json")):
            envelope = self._read(path)
            if path != self.path(envelope["identity"]):
                raise IntegrityError("Snapshot path does not match its identity")
            yield envelope["document"]
