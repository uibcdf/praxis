from dataclasses import replace

import pytest
from local_comparison import CAPABILITY, RMSD, RMSD_BINDING

import praxis
from praxis.errors import ContractError


def test_caught_step_failure_cannot_be_relabelled_success(workspace, inputs):
    catalog, context = workspace
    original = context.extensions.bindings[RMSD_BINDING]

    def recipe(inputs, configuration, steps):
        try:
            with steps.step("measure"):
                raise ValueError("provider failed but recipe swallowed it")
        except ValueError:
            pass
        return {"score": 0, "metric": "fictional"}

    reference = replace(RMSD_BINDING, identifier="fixture.caught_failure")
    context.extensions.register_binding(replace(original, ref=reference, recipe=recipe))
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=RMSD, binding_ref=reference),
        catalog=catalog,
        context=context,
    )
    with pytest.raises(ContractError):
        praxis.execute(prepared, catalog=catalog, context=context, identifier="swallowed-failure")
    assert context.records.attempt("swallowed-failure").contract_status == "violated"


def test_defaults_are_frozen_before_later_protocol_revision(workspace, inputs):
    catalog, context = workspace
    original = catalog.get(RMSD)
    reference = replace(RMSD, version="with-default")
    protocol = replace(
        original,
        ref=reference,
        parameters=(praxis.Parameter("fixture_option", "Fictional option", False, {"limit": 3}),),
    )
    catalog.register(protocol)
    binding = replace(
        context.extensions.bindings[RMSD_BINDING],
        ref=replace(RMSD_BINDING, version="with-default"),
        protocol_ref=reference,
    )
    context.extensions.register_binding(binding)
    prepared = praxis.prepare(
        praxis.MethodRequest(CAPABILITY, inputs, protocol_ref=reference, binding_ref=binding.ref),
        catalog=catalog,
        context=context,
    )
    catalog.register(
        replace(
            protocol,
            ref=replace(reference, version="next"),
            parameters=(
                praxis.Parameter("fixture_option", "Changed option", False, {"limit": 99}),
            ),
        )
    )
    assert context.records.prepared(prepared.identifier).configuration == {
        "fixture_option": {"limit": 3}
    }
    _, attempt = praxis.execute(prepared, catalog=catalog, context=context)
    assert attempt.operational_status == "completed"
