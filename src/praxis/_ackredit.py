"""Lazy borrowed-session capture; providers explicitly credit the branches they use."""

from contextlib import contextmanager


@contextmanager
def capture_attempt(identifier, enabled):
    if not enabled:
        yield None
        return
    from depdigest import check_dependency

    check_dependency(
        "ackredit", caller="Praxis attribution capture", pypi_name=None, conda_channel="uibcdf"
    )
    import ackredit

    # Ackredit always has a current session (including its default session).
    # Applications should activate their own scope; Praxis never replaces it.
    with ackredit.capture("praxis.method", context={"praxis_attempt_id": identifier}) as captured:
        yield captured
