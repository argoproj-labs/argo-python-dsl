"""Argo Workflow Python SDK utilities."""

from typing import Any
from typing import Dict

from uuid import uuid4

__mark = "___%s" % uuid4()


def _omitempty_rec(obj: Dict[str, Any]):
    obj[__mark] = True
    result: Dict[str, Any] = {}

    for k, v in obj.items():
        if k == __mark:
            continue

        if not v:  # empty
            continue

        if isinstance(v, dict) and __mark not in v:
            result[k] = _omitempty_rec(v)
        elif isinstance(v, list):
            result[k] = list(
                map(lambda d: _omitempty_rec(d) if isinstance(d, dict) else d, v)
            )
        else:
            result[k] = v

    return result


def _remove_marks(obj: Dict[str, Any]):
    if __mark not in obj:
        return
    del obj[__mark]
    for v in obj.values():
        if isinstance(v, dict):
            _remove_marks(v)


def omitempty(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Return copy of the object with empty values omitted."""
    try:
        result = _omitempty_rec(obj)
    finally:
        _remove_marks(obj)

    return result


def sanitize_for_serialization(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Return object sanitized for serialization.

    May be used with a V1alpha1Workflow to sanitize it
    back to the original state (i.e. per manifest).
    """
    from argo.workflows.client import ApiClient

    cl = ApiClient()
    return cl.sanitize_for_serialization(obj)
