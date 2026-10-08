"""Closed, provisional JSON schemas. No engine, callable or arbitrary repr serialization."""

import hashlib
import json
import types
from dataclasses import fields, is_dataclass
from typing import Any, ClassVar, Union, get_args, get_origin, get_type_hints

from .errors import DefinitionError


def plain(value):
    if is_dataclass(value) and not isinstance(value, type):
        result = {field.name: plain(getattr(value, field.name)) for field in fields(value)}
        if isinstance(value, Model):
            result = {"schema": value.schema, **result}
        return result
    if type(value) in (tuple, list):
        return [plain(item) for item in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise DefinitionError("JSON object keys must be strings")
        return {key: plain(item) for key, item in value.items()}
    if value is None or type(value) in (str, bool, int, float):
        return value
    raise DefinitionError("Only declared models and JSON values can be preserved")


def encode(value):
    try:
        return json.dumps(plain(value), sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (ValueError, TypeError) as error:
        raise DefinitionError("Records must contain finite JSON values") from error


def snapshot(value):
    return json.loads(encode(value))


def digest(value):
    return hashlib.sha256(encode(value).encode("utf-8")).hexdigest()


def _decode(annotation, value):
    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        for member in get_args(annotation):
            try:
                return _decode(member, value)
            except DefinitionError:
                pass
        raise DefinitionError("Value does not match any permitted field type")
    if annotation in (Any, object):
        return snapshot(value)
    if origin is tuple:
        if type(value) is not list:
            raise DefinitionError("Tuple fields are stored as JSON arrays")
        return tuple(_decode(get_args(annotation)[0], item) for item in value)
    if origin is dict:
        if type(value) is not dict:
            raise DefinitionError("Expected a JSON object")
        key_type, value_type = get_args(annotation)
        return {_decode(key_type, key): _decode(value_type, item) for key, item in value.items()}
    if isinstance(annotation, type) and issubclass(annotation, Model):
        return annotation.from_dict(value)
    if annotation is type(None) and value is None:
        return None
    if annotation in (str, bool, int, float) and type(value) is annotation:
        return value
    raise DefinitionError("Value does not match its declared field type")


class Model:
    schema: ClassVar[str]

    def to_dict(self):
        return snapshot(self)

    @classmethod
    def from_dict(cls, value):
        if type(value) is not dict or value.get("schema") != cls.schema:
            raise DefinitionError(f"Expected schema {cls.schema}")
        names = {field.name for field in fields(cls)}
        if set(value) - names - {"schema"}:
            raise DefinitionError("Unknown schema fields are not silently discarded")
        hints = get_type_hints(cls)
        try:
            return cls(
                **{key: _decode(hints[key], item) for key, item in value.items() if key != "schema"}
            )
        except (TypeError, ValueError) as error:
            raise DefinitionError(f"Invalid {cls.schema} record") from error

    def validate(self):
        """Validate nested types for direct Python construction too."""
        for field in fields(self):
            _decode(get_type_hints(type(self))[field.name], plain(getattr(self, field.name)))


def text(value, field):
    if type(value) is not str or not value.strip() or len(value) > 4096:
        raise DefinitionError(f"{field} must be a nonempty bounded string")


def unique(values, field):
    if len(values) != len(set(values)):
        raise DefinitionError(f"Duplicate {field}")
