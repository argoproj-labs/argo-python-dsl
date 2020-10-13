"""Argo Workflows Python DSL."""

__all__ = [
    # modules
    "task",
    "templates",
    # decorators
    "tasks",
    "template",
    # main
    "CronWorkflow",
    "Workflow",
]

# modules
from . import tasks
from . import templates

# decorators
from .tasks import task
from .templates import template

# main
from ._cronworkflow import CronWorkflow
from ._workflow import Workflow
