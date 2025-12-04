"""Core retrieval logic (secure stub).

This module provides a small, safe, deterministic stub for retrieval logic.
Replace the internals of `fetch` with real, secure retrieval code as needed.
"""

import re
import time
from typing import Any, Dict


class FetchError(Exception):
    """Raised when a fetch request is invalid or fails."""


_ALLOWED_QUERY_RE = re.compile(r"^[\w\s\-\']{1,200}$")


def _sanitize(query: str) -> str:
    q = (query or "").strip()
    if not q:
        raise FetchError("empty query")
    if not _ALLOWED_QUERY_RE.match(q):
        raise FetchError("query contains invalid characters")
    return q


def fetch(query: str, timeout: float = 5.0) -> Dict[str, Any]:
    """Return a deterministic, local stubbed result for `query`.

    - Validates input to avoid shell/injection-like content.
    - Is synchronous and CPU-bound; keeps work minimal for tests.

    Parameters
    - query: search string
    - timeout: maximum allowed time in seconds (soft limit)

    Returns a dictionary with `query`, `result`, and `source` keys.
    """
    start = time.time()
    q = _sanitize(query)

    # Soft timeout check - this is a stub, so we don't do real I/O.
    if timeout is not None and timeout <= 0:
        raise FetchError("timeout must be > 0")

    # Simulate a tiny amount of processing time, but don't block long.
    elapsed = time.time() - start
    if elapsed < 0.001:
        time.sleep(0.001)

    # Deterministic pseudo-result suitable for tests/examples.
    result_text = f"Simulated answer for: {q}"

    return {"query": q, "result": result_text, "source": "local-stub"}
