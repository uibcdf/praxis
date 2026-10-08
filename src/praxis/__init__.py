"""Experimental local methodology API. Importing Praxis does not activate providers."""

from .applicability import ApplicabilityReport, assess_applicability
from .audit import AuditIssue, AuditReport, audit_benchmark, audit_definition, audit_execution
from .benchmarks import (
    BenchmarkCase,
    BenchmarkMethod,
    BenchmarkResult,
    BenchmarkSpec,
    MetricDefinition,
    load_benchmark,
    reanalyze_benchmark,
    run_benchmark,
    summarize_benchmark,
)
from .catalog import Catalog
from .definitions import (
    AdmissionReview,
    Assessment,
    Capability,
    CheckFinding,
    EvidenceRecord,
    Field,
    MethodRef,
    MethodStatus,
    Parameter,
    Protocol,
    Requirement,
    ResourceProfile,
    Step,
    SuitabilityStatement,
    Tradeoff,
)
from .execution.context import ExecutionContext
from .execution.reports import AttemptRecord, MethodRequest, PreparedInvocation, SelectionRecord
from .execution.runner import execute, prepare
from .extensions import CheckResult, Extensions, ImplementationBinding
from .recording import MethodRecords, RecordaRecorder
from .replay import ReplayPreflight, replay_execution, replay_preflight, trace_execution
from .reporting import (
    Document,
    audit_document,
    benchmark_document,
    comparison_document,
    describe_method,
    execution_document,
    render,
)
from .selection import SelectionPolicy

__version__ = "0.1.0.dev0"

__all__ = [
    "ReplayPreflight",
    "replay_execution",
    "replay_preflight",
    "trace_execution",
    "ApplicabilityReport",
    "Assessment",
    "AdmissionReview",
    "MethodStatus",
    "ResourceProfile",
    "SuitabilityStatement",
    "AttemptRecord",
    "AuditIssue",
    "AuditReport",
    "Capability",
    "Catalog",
    "CheckFinding",
    "CheckResult",
    "ExecutionContext",
    "Extensions",
    "Field",
    "EvidenceRecord",
    "ImplementationBinding",
    "MethodRecords",
    "MethodRef",
    "MethodRequest",
    "Parameter",
    "PreparedInvocation",
    "Protocol",
    "RecordaRecorder",
    "Requirement",
    "SelectionRecord",
    "SelectionPolicy",
    "Step",
    "Tradeoff",
    "assess_applicability",
    "audit_execution",
    "audit_definition",
    "audit_benchmark",
    "audit_document",
    "comparison_document",
    "execute",
    "prepare",
    "BenchmarkCase",
    "BenchmarkMethod",
    "BenchmarkResult",
    "BenchmarkSpec",
    "MetricDefinition",
    "reanalyze_benchmark",
    "summarize_benchmark",
    "load_benchmark",
    "run_benchmark",
    "Document",
    "benchmark_document",
    "describe_method",
    "execution_document",
    "render",
]
