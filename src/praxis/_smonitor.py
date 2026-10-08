"""Count-free methodological diagnostics; no scientific inputs or exception messages."""

SMONITOR = {"capture_logging": False, "capture_warnings": False, "capture_exceptions": False}
SIGNALS = {}
CODES = {
    "PRAXIS-CHECKER-ERROR": {
        "level": "WARNING",
        "category": "methodology",
        "user_message": "A methodological checker failed; its requirement remains unresolved.",
        "dev_message": "A methodological checker failed; its requirement remains unresolved.",
        "metadata_hint": "Inspect the retained check finding and the registered checker.",
    },
    "PRAXIS-RECORDING-GAP": {
        "level": "WARNING",
        "category": "recording",
        "user_message": "Required operation recording could not be completed.",
        "dev_message": "Required operation recording could not be completed.",
        "metadata_hint": "Inspect the retained method attempt and the recorder's journal.",
    },
}
