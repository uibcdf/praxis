"""Observed callable identities. No closures, scientific objects or source text retained."""

import functools
import types
from importlib.metadata import PackageNotFoundError, version

from ._serialization import digest


def _constant(value):
    if isinstance(value, types.CodeType):
        return _code(value)
    if type(value) in (tuple, frozenset):
        values = [_constant(item) for item in value]
        if type(value) is frozenset:
            values.sort(key=digest)
        return {"type": type(value).__name__, "values": values}
    if type(value) is bytes:
        return {"type": "bytes", "value": value.hex()}
    if type(value) is float:
        return {"type": "float", "value": value.hex()}
    if type(value) is complex:
        return {"type": "complex", "real": value.real.hex(), "imag": value.imag.hex()}
    if value is None or type(value) in (str, bool, int):
        return {"type": type(value).__name__, "value": value}
    return {"type": type(value).__name__}


def _code(code):
    return {
        "bytecode": code.co_code.hex(),
        "constants": [_constant(item) for item in code.co_consts],
        "names": code.co_names,
        "variables": code.co_varnames,
        "freevars": code.co_freevars,
        "cellvars": code.co_cellvars,
        "argcount": code.co_argcount,
        "posonlyargcount": code.co_posonlyargcount,
        "kwonlyargcount": code.co_kwonlyargcount,
        "flags": code.co_flags,
        "exceptions": code.co_exceptiontable.hex(),
    }


def callable_identity(function):
    """Fingerprint loaded Python code, ignoring install path and line numbers.

    This is change detection, not authentication or capture of hidden mutable state.
    Partial arguments must be JSON values; opaque runtime state belongs in declared
    inputs/configuration rather than a partially bound scientific argument.
    """
    partial = None
    if isinstance(function, functools.partial):
        partial = {"args": function.args, "keywords": function.keywords}
        function = function.func
    target = function.__func__ if isinstance(function, types.MethodType) else function
    if not isinstance(target, (types.FunctionType, types.BuiltinFunctionType)):
        target = type(function).__call__
    module = getattr(target, "__module__", None) or type(function).__module__
    qualname = getattr(target, "__qualname__", type(function).__qualname__)
    try:
        package_version = version(module.split(".")[0])
    except PackageNotFoundError:
        package_version = None
    code = getattr(target, "__code__", None)
    defaults = getattr(target, "__defaults__", None)
    keywords = getattr(target, "__kwdefaults__", None)
    return {
        "module": module,
        "qualname": qualname,
        "callable_name": getattr(function, "__qualname__", None)
        or getattr(function, "__name__", None)
        or type(function).__qualname__,
        "package_version": package_version,
        "code_digest": digest(_code(code)) if code is not None else None,
        "defaults_digest": digest({"defaults": defaults, "keywords": keywords, "partial": partial}),
    }
