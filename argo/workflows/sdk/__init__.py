"""Argo Workflows Python SDK."""

__all__ = [
    # modules
    "task",
    "templates",

    # decorators
    "tasks",
    "template",

    # main
    "Workflow"
]

# modules
from . import tasks
from . import templates

# decorators
from .tasks import task
from .templates import template

# main
from ._workflow import Workflow
