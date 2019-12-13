from abc import ABCMeta

import six
import types

import pprint
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from inflection import dasherize
from inflection import underscore

from typing import Any
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from argo.workflows.client.models import V1alpha1DAGTask
from argo.workflows.client.models import V1alpha1DAGTemplate
from argo.workflows.client.models import V1alpha1Template
from argo.workflows.client.models import V1alpha1TemplateRef
from argo.workflows.client.models import V1alpha1Workflow
from argo.workflows.client.models import V1alpha1WorkflowSpec
from argo.workflows.client.models import V1alpha1WorkflowStatus
from argo.workflows.client.models import V1ObjectMeta

from . import _utils

__all__ = ["Workflow"]


class WorkflowMeta(ABCMeta):

    __model__ = V1alpha1Workflow

    def __new__(
        cls,
        name: Union[str, Type["Workflow"]],
        bases: Tuple[Type["Workflow"], ...],
        props: Dict[str, Any],
        **kwargs,
    ):
        workflow_name = dasherize(underscore(name))

        props["kind"] = "Workflow"
        props["api_version"] = "argoproj.io/v1alpha1"

        metadata_dict = dict(name=workflow_name, generate_name=f"{workflow_name}-")
        metadata_dict.update(props.get("__metadata__", {}))

        # Required fields
        props["metadata"]: V1ObjectMeta = V1ObjectMeta(**metadata_dict)
        props["spec"] = {}
        props["status"] = {}

        bases = (*bases, cls.__model__)
        klass = super().__new__(cls, name, bases, props)

        if name == "Workflow":
            # No need to initialize any further
            return klass

        cls.__compile(klass, name, bases, props)

        return klass

    @classmethod
    def __compile(
        cls,
        klass: "Workflow",
        name: str,
        bases: Tuple[Type["Workflow"], ...],
        props: Dict[str, Any],
        **kwargs,
    ):
        tasks: List[V1alpha1DAGTask] = []
        templates: List[V1alpha1Template] = []

        for key, prop in props.items():
            model = getattr(prop, "__model__", None)
            if model is None:
                continue

            template: Optional[V1alpha1Template] = None

            # V1alpha1Template
            if issubclass(model, V1alpha1Template):
                template = prop.__get__(klass)
                templates.append(template)

            # V1alpha1DAGTask
            elif issubclass(model, V1alpha1DAGTask):
                task = prop.__get__(klass)
                tasks.append(task)

        if tasks:
            main_template = V1alpha1Template(name="main")
            main_template.dag = V1alpha1DAGTemplate(tasks=tasks)
            templates.insert(0, main_template)

        spec_dict: dict = klass.spec
        spec_dict["entrypoint"] = props.get("entrypoint", "")
        spec_dict["templates"] = templates

        klass.spec: V1alpha1WorkflowSpec = V1alpha1WorkflowSpec(**spec_dict)


class Workflow(metaclass=WorkflowMeta):
    """"""

    __model__ = V1alpha1Workflow

    def __init__(self):
        """Workflow is the definition of a workflow resource.

        This class is a base class for Argo Workflows. It is not meant
        to be instantiated directly.
        """
        self.__compiled = False
        self.compile()

    @property
    def compiled(self) -> bool:
        return self.__compiled

    @compiled.setter
    def compiled(self, is_compiled: bool):
        if not isinstance(is_compiled, bool):
            raise TypeError(f"Expected type {bool}, got: {type(is_compiled)}")

        self.__compiled = is_compiled

    def compile(self) -> V1alpha1Workflow:
        """Compile the Workflow class to V1alpha1Workflow model."""
        if self.compiled:
            return Workflow.__model__(**self.to_dict(omitempty=False))

        spec: V1alpha1WorkflowSpec = self.spec

        templates: Dict[str, V1alpha1Template] = {}
        for template in spec.templates:
            if getattr(template, "__model__", None):
                template: V1alpha1Template = template.__call__()
                continue

            tasks: List[Union[V1alpha1DAGTask, Callable]] = getattr(
                template.dag, "tasks", []
            )
            for i in range(len(tasks)):
                task: Union[V1alpha1DAGTask, Callable] = tasks[i]
                if getattr(task, "__model__", None):
                    task: V1alpha1DAGTask
                    template: Union[V1alpha1DAGTemplate, V1alpha1TemplateRef]
                    task, task_template = task.__call__()

                    if task_template is not None:
                        # TODO: Recurse here to allow nested templates
                        templates[task_template.name] = task_template

                    tasks[i] = task

                template.dag.tasks[i] = task

            templates[template.name] = template

        self.spec.templates = list(templates.values())
        model: V1alpha1Workflow = Workflow.__model__(**self.to_dict(omitempty=False))

        self.compiled = True
        return model

    def to_yaml(self, **kwargs) -> str:
        """Returns the Workflow manifest as a YAML."""
        d: dict = self.to_dict(omitempty=True)

        opts = dict(default_flow_style=False)
        opts.update(kwargs)

        serialized = yaml.dump(d, Dumper=Dumper, **opts)

        return serialized

    def to_dict(self, omitempty=True) -> Dict[str, Any]:
        """Returns the Workflow manifest as a dict.

        :param omitempty: bool, whether to omit empty values
        """
        result = V1alpha1Workflow.to_dict(self)

        if omitempty:
            return _utils.omitempty(result)

        return result
