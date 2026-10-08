"""Bounded sequential benchmarks with explicit cases and evaluator identity."""

from dataclasses import dataclass, field

from .._serialization import Model, text, unique
from ..definitions import MethodRef
from ..errors import DefinitionError


@dataclass(frozen=True)
class BenchmarkCase(Model):
    schema = "praxis.benchmark-case/0.1"
    identifier: str
    inputs: dict[str, object]
    scenario: str

    def __post_init__(self):
        self.validate()
        text(self.identifier, "case identifier")
        text(self.scenario, "case scenario")


@dataclass(frozen=True)
class BenchmarkMethod(Model):
    schema = "praxis.benchmark-method/0.1"
    protocol_ref: MethodRef
    binding_ref: MethodRef
    configuration: dict[str, object] = field(default_factory=dict)

    def __post_init__(self):
        self.validate()
        if self.protocol_ref.kind != "protocol" or self.binding_ref.kind != "extension":
            raise DefinitionError("Benchmark methods require exact Protocol and binding references")


@dataclass(frozen=True)
class MetricDefinition(Model):
    schema = "praxis.metric/0.1"
    name: str
    meaning: str
    unit: str | None = None
    quantity_field: str | None = None
    direction: str = "descriptive"

    def __post_init__(self):
        self.validate()
        text(self.name, "metric name")
        text(self.meaning, "metric meaning")
        if bool(self.unit) != bool(self.quantity_field):
            raise DefinitionError("Physical metrics require both unit and semantic quantity field")
        if self.direction not in {"descriptive", "minimize", "maximize"}:
            raise DefinitionError("Unknown metric direction")


@dataclass(frozen=True)
class BenchmarkSpec(Model):
    schema = "praxis.benchmark/0.1"
    ref: MethodRef
    purpose: str
    capability_ref: MethodRef
    cases: tuple[BenchmarkCase, ...]
    methods: tuple[BenchmarkMethod, ...]
    evaluator_ref: MethodRef
    metric: str
    comparison_basis: str
    replicates: int = 1
    limitations: tuple[str, ...] = ()
    metrics: tuple[MetricDefinition, ...] = ()
    evaluator_configuration: dict[str, object] = field(default_factory=dict)
    seeds: tuple[int, ...] = ()
    seed_parameter: str | None = None

    def __post_init__(self):
        self.validate()
        if self.ref.kind != "benchmark" or self.capability_ref.kind != "capability":
            raise DefinitionError("Benchmark requires exact benchmark and Capability references")
        if self.evaluator_ref.kind != "extension":
            raise DefinitionError("Evaluator must have an exact extension identity")
        for name in ("purpose", "metric", "comparison_basis"):
            text(getattr(self, name), name)
        if not self.cases or not self.methods or self.replicates < 1:
            raise DefinitionError("Benchmark requires cases, methods and positive replicates")
        if type(self.replicates) is not int:
            raise DefinitionError("Replicates must be an integer")
        unique([item.name for item in self.metrics], "benchmark metrics")
        if self.seeds:
            if (
                not self.seed_parameter
                or len(self.seeds) != self.replicates
                or any(type(seed) is not int for seed in self.seeds)
            ):
                raise DefinitionError(
                    "Seed controls require a named parameter and one integer per replicate"
                )
            if any(self.seed_parameter in method.configuration for method in self.methods):
                raise DefinitionError("Seed controls cannot overwrite method configuration")
        elif self.seed_parameter is not None:
            raise DefinitionError("A seed parameter requires explicit replicate seeds")
        unique([item.identifier for item in self.cases], "benchmark cases")
        unique(
            [(item.protocol_ref, item.binding_ref) for item in self.methods], "benchmark methods"
        )


@dataclass(frozen=True)
class BenchmarkResult(Model):
    schema = "praxis.benchmark-result/0.1"
    identifier: str
    spec: BenchmarkSpec
    started: str
    finished: str | None
    rows: tuple[dict[str, object], ...]
    status: str = "completed"
    evaluator: dict[str, object] | None = None
    environment: dict[str, object] = field(default_factory=dict)
    analysis_of: str | None = None
