import re
import yaml

from typing import Any
from typing import Dict

from uuid import uuid4

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

"""Argo Workflow Python DSL utilities."""

__mark = "___%s" % uuid4()


class BlockDumper(Dumper):
    def represent_scalar(self, tag, value, style=None):
        if re.search("\n", value):
            style = "|"
            # remove trailing spaces and newlines which are not allowed in YAML blocks
            value = re.sub(" +\n", "\n", value).strip()

        return super().represent_scalar(tag, value, style)


def _omitempty_rec(obj: Dict[str, Any]):
    obj[__mark] = True
    result: Dict[str, Any] = {}

    for k, v in obj.items():
        if k == __mark:
            continue

        if v is None:  # empty
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
