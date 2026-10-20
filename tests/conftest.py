import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING, build_fixture

import praxis


@pytest.fixture
def workspace(tmp_path):
    return build_fixture(tmp_path)


@pytest.fixture
def inputs():
    return {"left": [[0, 0, 0], [1, 0, 0]], "right": [[0, 0, 0], [1, 1, 0]]}


@pytest.fixture
def prepared(workspace, inputs):
    catalog, context = workspace
    request = praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=RMSD_BINDING)
    return praxis.prepare(request, catalog=catalog, context=context)


@pytest.fixture
def configure_extensions(workspace):
    """Construct a distinct registry before preparation, using public registration."""
    _, context = workspace

    def configure(checkers=None, omitted=()):
        checkers = checkers or {}
        registry = praxis.Extensions()
        for binding in context.extensions.bindings.values():
            registry.register_binding(binding)
        for ref, checker in context.extensions.checkers.items():
            if ref not in omitted:
                registry.register_checker(ref, checkers.get(ref, checker))
        context.extensions = registry

    return configure


@pytest.fixture
def prepare_recipe(workspace, prepared):
    from dataclasses import replace

    catalog, context = workspace

    def configure(recipe):
        original = context.extensions.bindings[prepared.selection.binding_ref]
        reference = replace(original.ref, version="test-recipe")
        context.extensions.register_binding(replace(original, ref=reference, recipe=recipe))
        return praxis.prepare(
            praxis.MethodRequest(
                prepared.capability_ref,
                prepared.inputs,
                prepared.configuration,
                prepared.selection.protocol_ref,
                reference,
            ),
            catalog=catalog,
            context=context,
        )

    return configure
