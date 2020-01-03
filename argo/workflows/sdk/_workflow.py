from abc import ABCMeta

import logging
import six
import types

import json
import yaml

import pprint
import requests

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from inflection import camelize
from inflection import dasherize
from inflection import underscore

from pathlib import Path

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from argo.workflows import client

from argo.workflows.client.models import V1alpha1Arguments
from argo.workflows.client.models import V1alpha1Artifact
from argo.workflows.client.models import V1alpha1DAGTask
from argo.workflows.client.models import V1alpha1DAGTemplate
from argo.workflows.client.models import V1alpha1Parameter
from argo.workflows.client.models import V1alpha1Template
from argo.workflows.client.models import V1alpha1TemplateRef
from argo.workflows.client.models import V1alpha1Workflow
from argo.workflows.client.models import V1alpha1WorkflowSpec
from argo.workflows.client.models import V1alpha1WorkflowStatus
from argo.workflows.client.models import V1ObjectMeta

from . import _utils

__all__ = ["Workflow"]


_LOGGER = logging.getLogger(__name__)


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
        props["spec"] = {
            k: props.get(k) for k in V1alpha1WorkflowSpec.attribute_map if props.get(k)
        }
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
                template = prop
                templates.append(template)

            # V1alpha1DAGTask
            elif issubclass(model, V1alpha1DAGTask):
                task = prop
                tasks.append(task)

        if tasks:
            main_template = V1alpha1Template(name="main")
            main_template.dag = V1alpha1DAGTemplate(tasks=tasks)

            templates.insert(0, main_template)

        spec_dict: dict = klass.spec
        spec_dict["entrypoint"] = props.get("entrypoint", "main")
        spec_dict["templates"] = templates

        klass.spec: V1alpha1WorkflowSpec = V1alpha1WorkflowSpec(**spec_dict)


class Workflow(metaclass=WorkflowMeta):
    """"""

    __model__ = V1alpha1Workflow

    def __init__(self, compile=True):
        """Workflow is the definition of a workflow resource.

        This class is a base class for Argo Workflows. It is not meant
        to be instantiated directly.

        :para compile: bool, whether to compile during initialization [True]
        """
        self.__compiled_model: Union[V1alpha1Workflow, None] = None
        self.__validated = False

        if compile:
            self.compile()

    @property
    def model(self) -> Union[V1alpha1Workflow, None]:
        """Return the Workflow specification.

        :returns: V1alpha1Workflow if compiled, otherwise None
        """
        return self.__compiled_model

    @model.setter
    def model(self, spec: V1alpha1Workflow):
        if not isinstance(spec, self.__model__):
            raise TypeError(f"Expected type {self.__model__}, got: {type(spec)}")

        self.__compiled_model = spec

    @property
    def name(self) -> Union[str, None]:
        """Return Workflow name."""
        return self.metadata.name

    @name.setter
    def name(self, name: str):
        """Return Workflow name."""
        self.metadata.name = name

    @property
    def validated(self) -> bool:
        """Return whether this workflow has been validated."""
        return self.__validated

    @classmethod
    def from_file(cls, fp: Union[str, Path], validate: bool = True) -> "Workflow":
        """Create a Workflow from a file."""
        wf_path = Path(fp)

        wf: Dict[str, Any] = yaml.safe_load(wf_path.read_text())
        return cls.from_dict(wf, validate=validate)

    @classmethod
    def from_url(cls, url: str, validate: bool = True) -> "Workflow":
        """Create a Workflow from a remote file."""
        resp = requests.get(
            "https://raw.githubusercontent.com/argoproj/argo/master/examples/hello-world.yaml"
        )
        resp.raise_for_status()

        wf: Dict[str, Any] = yaml.safe_load(resp.text)
        return cls.from_dict(wf, validate=validate)

    @classmethod
    def from_dict(cls, wf: Dict[str, Any], validate: bool = True) -> "Workflow":
        """Create a Workflow from a dict."""
        # work around validation issues and allow empty status
        wf["status"] = wf.get("status", {}) or {}

        return cls.from_string(json.dumps(wf), validate=validate)

    @classmethod
    def from_string(cls, wf: str, validate: bool = True) -> "Workflow":
        """Create a Workflow from a YAML string."""
        body = {"data": wf}

        return cls.__deserialize(body, validate=validate)

    @classmethod
    def __deserialize(cls, body: Dict[str, str], *, validate: bool) -> "Workflow":
        """Deserialize given object into a Workflow instance."""
        wf: Union[V1alpha1Workflow, Dict[str, Any]]
        if validate:
            attr = type("Response", (), body)

            wf = client.ApiClient().deserialize(attr, cls.__model__)
        else:
            _LOGGER.warning(
                "Validation is turned off. This may result in missing or invalid attributes."
            )
            wf = json.loads(body["data"])

        self = cls(compile=False)

        if isinstance(wf, V1alpha1Workflow):
            self.__dict__.update(
                api_version=wf.api_version,
                kind=wf.kind,
                metadata=wf.metadata,
                spec=wf.spec,
                status=wf.status,  # a small hack to overcome validation
            )
        else:
            self.__dict__.update(**wf)

        self.__validated = validate

        return self

    def compile(self) -> V1alpha1Workflow:
        """Compile the Workflow class to V1alpha1Workflow model."""
        model: V1alpha1Workflow = self.model
        if model is not None:
            return model

        def _compile(obj: Any):
            if hasattr(obj, "__model__"):
                if obj.model is not None:
                    # prevents referenced templates from being compiled again
                    return obj.model

                args: Dict[str, Any] = {}
                props: Dict[str, Any] = getattr(obj.fget, "__props__", {})

                arguments: V1alpha1Arguments = props.get("arguments")
                if arguments:
                    for artifact in getattr(arguments, "artifacts", []) or []:
                        if hasattr(artifact, "to_dict"):
                            artifact = V1alpha1Artifact(**artifact.to_dict())
                        else:
                            artifact = V1alpha1Artifact(**artifact)
                        args[artifact.name] = artifact

                    for param in getattr(arguments, "parameters", []) or []:
                        if hasattr(param, "to_dict"):
                            param = V1alpha1Parameter(**param.to_dict())
                        else:
                            param = V1alpha1Parameter(**param)
                        args[param.name] = param

                return obj.__get__(self).__call__(**args)
            if isinstance(obj, list):
                return list(map(_compile, obj))
            if hasattr(obj, "attribute_map"):
                for attr in obj.attribute_map:
                    value: Any = _compile(getattr(obj, attr))
                    setattr(obj, attr, value)

            return obj

        self.spec: V1alpha1WorkflowSpec = _compile(self.spec)

        model: V1alpha1Workflow = Workflow.__model__(**self.to_dict(omitempty=False))
        self.model = model

        self.__validated = True

        return model

    def submit(
        self,
        client: client.V1alpha1Api,
        namespace: str,
        *,
        parameters: Optional[Dict[str, str]] = None,
    ) -> str:
        """Submit an Argo Workflow to a given namespace.

        :returns: str, Workflow name
        """
        parameters = parameters or {}

        new_parameters: List[V1alpha1Parameter] = []
        for name, value in parameters.items():
            param = V1alpha1Parameter(name=name, value=value)
            new_parameters.append(param)

        if hasattr(self.spec, "arguments"):
            for p in getattr(self.spec.arguments, "parameters", []):
                if p.name in parameters:
                    continue  # overridden
                elif not getattr(p, "value") and not getattr(p, "default"):
                    raise Exception(f"Missing required workflow parameter {p.name}")

                new_parameters.append(p)

            self.spec.arguments.parameters = new_parameters

        body: Dict[str, Any]
        if not getattr(self, "validated", True):
            _LOGGER.debug(
                "The Workflow has not been previously validated."
                "Sanitizing for serialization."
            )
            body = camelize(self.to_dict())
        else:
            body = client.api_client.sanitize_for_serialization(self)

        # submit the workflow
        created: models.V1alpha1Workflow = client.create_namespaced_workflow(
            namespace, body
        )

        # return the computed Workflow ID
        return self.name

    def to_yaml(self, omitempty=True, **kwargs) -> str:
        """Returns the Workflow manifest as a YAML."""
        d: dict = self.to_dict(omitempty=omitempty)

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
