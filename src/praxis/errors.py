"""Local methodological errors; provider exceptions retain their original types."""


class PraxisError(Exception):
    """Base for Praxis-owned failures."""


class DefinitionError(PraxisError, ValueError):
    """A definition or serialized record violates its local schema."""


class ConflictError(PraxisError):
    """Different content was supplied under an existing exact identity."""


class IntegrityError(PraxisError):
    """A stored record does not match its retained identity or digest."""


class NotReadyError(PraxisError):
    """Execution is blocked by unresolved or violated requirements."""


class ContractError(PraxisError):
    """A recipe's observed boundaries violate the declared local contract."""


class RecordingError(PraxisError):
    """A requested operation boundary could not be retained."""


class WaitingForReview(PraxisError):
    """A declared human gate awaits an explicit permitted review."""


class CancelledError(PraxisError):
    """Application cancellation observed at a declared recipe boundary."""
