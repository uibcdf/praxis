"""ArgDigest owns normalization at the request's JSON boundary, loaded on first use."""

from pathlib import Path

from smonitor import diagnostic_scope
from smonitor.integrations import ensure_configured

from ._serialization import snapshot
from .errors import DefinitionError

with diagnostic_scope():
    ensure_configured(Path(__file__).resolve().parent)
    from argdigest import DigestConfig, arg_digest, register_pipeline

    @register_pipeline(kind="praxis.request", name="json_object")
    def _json_object(value, ctx):
        if type(value) is not dict:
            raise DefinitionError("Invocation inputs and configuration must be JSON objects")
        return snapshot(value)

    @arg_digest.map(
        config=DigestConfig(
            capture_policy="metadata_only",
            argument_digestion=False,
            strictness="error",
            unknown_argument="error",
        ),
        inputs={"kind": "praxis.request", "rules": [_json_object]},
        configuration={"kind": "praxis.request", "rules": [_json_object]},
    )
    def request_values(inputs, configuration):
        return _json_object(inputs, None), _json_object(configuration, None)
