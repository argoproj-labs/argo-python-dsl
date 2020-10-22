from abc import ABCMeta

import logging

import inspect
import json
import yaml

import requests


from inflection import dasherize
from inflection import underscore

from pathlib import Path

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
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
from argo.workflows.client.models import V1alpha1ClusterWorkflowTemplate
from argo.workflows.client.models import V1alpha1WorkflowTemplate
from argo.workflows.client.models import V1alpha1WorkflowTemplateSpec
from argo.workflows.client.models import V1ObjectMeta


from . import _utils

__all__ = ["WorkflowTemplate"]


_LOGGER = logging.getLogger(__name__)


class WorkflowTemplateMeta(ABCMeta):

    __model__ = V1alpha1WorkflowTemplate
    __kind__ = "WorkflowTemplate"

    def __new__(
        cls,
        name: Union[str, Type["WorkflowTemplate"]],
        bases: Tuple[Type["WorkflowTemplate"], ...],
        props: Dict[str, Any],
        **kwargs,
    ):
        workflow_name = dasherize(underscore(name))

        props["kind"] = cls.__kind__
        props["api_version"] = "argoproj.io/v1alpha1"

        metadata_dict = {"name": workflow_name}
        metadata_dict.update(props.get("__metadata__", {}))

        # Required fields
        props["metadata"]: V1ObjectMeta = V1ObjectMeta(**metadata_dict)
        props["spec"] = {
            k: props.pop(k)
            for k in V1alpha1WorkflowTemplateSpec.attribute_map
            if props.get(k)
        }

        bases = (*bases, cls.__model__)
        klass = super().__new__(cls, name, bases, props)

        if name == cls.__kind__:
            # No need to initialize any further
            return klass

        cls.__compile(klass, name, bases, props)

        return klass

    @classmethod
    def __compile(
        cls,
        klass: "WorkflowTemplate",
        name: str,
        bases: Tuple[Type["WorkflowTemplate"], ...],
        props: Dict[str, Any],
        **kwargs,
    ):
        tasks: List[V1alpha1DAGTask] = []
        templates: List[V1alpha1Template] = []

        scopes: Dict[str, List[Any]] = {}

        # get scopes first
        for key, prop in props.items():
            scope = getattr(prop, "__scope__", None)
            if scope is None:
                continue

            scoped_objects = [prop]
            scoped_objects.extend(scopes.get(scope, []))

            scopes[scope] = scoped_objects

        for key, prop in props.items():
            model = getattr(prop, "__model__", None)
            if model is None:
                continue

            template: Optional[V1alpha1Template] = None

            # V1alpha1Template
            if issubclass(model, V1alpha1Template):
                template = prop

                # closures require special treatment
                if hasattr(template, "__closure__") and template.script is not None:
                    template = cls.__compile_closure(template, scopes)

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
        spec_dict["entrypoint"] = spec_dict.get("entrypoint", "main")
        spec_dict["templates"] = templates

        klass.spec: V1alpha1WorkflowTemplateSpec = V1alpha1WorkflowTemplateSpec(
            **spec_dict
        )

    @classmethod
    def __compile_closure(
        cls, template: V1alpha1Template, scopes: Dict[str, Any] = None
    ) -> V1alpha1Template:
        scopes = scopes or {}

        scope: str = template.__closure__
        if scope is None:
            # nothing to do
            return template

        script: List[str] = [f"class {scope}:\n"]
        script.append(f'    """Scoped objects injected from scope \'{scope}\'."""\n\n')

        scoped_objects = scopes.get(scope) or []
        for so in scoped_objects:
            source, _ = inspect.getsourcelines(so.__get__(cls).__code__)

            for co_start, line in enumerate(source):
                if line.strip().startswith("def"):
                    break

            source = ["    @staticmethod\n"] + source[co_start:] + ["\n"]
            script.extend(source)

        script = script + [
            "\n",
            *template.script.source.splitlines(keepends=True),
        ]

        import_lines: List[str] = []
        source_lines: List[str] = []

        import_in_previous_line = False
        for line in script:
            if "import " in line:
                import_lines.append(line.strip(" "))
                import_in_previous_line = True
            else:
                is_blankline = not bool(line.strip())
                if import_in_previous_line and is_blankline:
                    # blank line separating imports
                    pass
                else:
                    source_lines.append(line)

                import_in_previous_line = False

        # split `imports` and `from` and sort them separately
        import_lines_with_from: Set[str] = set()
        import_lines_without_from: Set[str] = set()

        for line in import_lines:
            if "from " in line:
                import_lines_with_from.add(line)
            else:
                import_lines_without_from.add(line)

        import_lines = [
            *sorted(import_lines_without_from),
            "\n",
            *sorted(import_lines_with_from),
        ]

        template.script.source = "".join((*import_lines, "\n", *source_lines))

        return template


class WorkflowTemplate(metaclass=WorkflowTemplateMeta):
    """Base class for Workflows."""

    __model__ = V1alpha1WorkflowTemplate

    def __init__(self, compile=True):
        """WorkflowTemplate is the definition of a workflow resource.

        This class is a base class for Argo Workflows. It is not meant
        to be instantiated directly.

        :para compile: bool, whether to compile during initialization [True]
        """
        self._compiled_model: Union[V1alpha1WorkflowTemplate, None] = None
        self.__validated = False

        if compile:
            self.compile()

    def __hash__(self) -> str:
        """Compute hash of this WorkflowTemplate."""
        return self.to_str().__hash__()

    @property
    def model(self) -> Union[V1alpha1WorkflowTemplate, None]:
        """Return the WorkflowTemplate model.

        :returns: V1alpha1WorkflowTemplate if compiled, otherwise None
        """
        return self._compiled_model

    @model.setter
    def model(self, m: V1alpha1WorkflowTemplate):
        """Set WorkflowTemplate model."""
        if not isinstance(m, self.__model__):
            raise TypeError(f"Expected type {self.__model__}, got: {type(m)}")

        self._compiled_model = m

    @property
    def name(self) -> Union[str, None]:
        """Return the WorkflowTemplate name."""
        return self.metadata.name

    @name.setter
    def name(self, name: str):
        """Set WorkflowTemplate name."""
        self.metadata.name = name

    @property
    def validated(self) -> bool:
        """Return whether this workflow has been validated."""
        return self.__validated

    @classmethod
    def from_file(
        cls, fp: Union[str, Path], validate: bool = True
    ) -> "WorkflowTemplate":
        """Create a WorkflowTemplate from a file."""
        wf_path = Path(fp)

        wf: Dict[str, Any] = yaml.safe_load(wf_path.read_text())
        return cls.from_dict(wf, validate=validate)

    @classmethod
    def from_url(cls, url: str, validate: bool = True) -> "WorkflowTemplate":
        """Create a WorkflowTemplate from a remote file."""
        resp = requests.get(url)
        resp.raise_for_status()

        wf: Dict[str, Any] = yaml.safe_load(resp.text)
        return cls.from_dict(wf, validate=validate)

    @classmethod
    def from_dict(cls, wf: Dict[str, Any], validate: bool = True) -> "WorkflowTemplate":
        """Create a WorkflowTemplate from a dict."""
        return cls.from_string(json.dumps(wf), validate=validate)

    @classmethod
    def from_string(cls, wf: str, validate: bool = True) -> "WorkflowTemplate":
        """Create a WorkflowTemplate from a YAML string."""
        body = {"data": wf}

        return cls.__deserialize(body, validate=validate)

    @classmethod
    def __deserialize(
        cls, body: Dict[str, str], *, validate: bool
    ) -> "WorkflowTemplate":
        """Deserialize given object into a WorkflowTemplate instance."""
        wf: Union[V1alpha1WorkflowTemplate, Dict[str, Any]]
        if validate:
            attr = type("Response", (), body)

            wf = client.ApiClient().deserialize(attr, cls.__model__)
        else:
            _LOGGER.warning(
                "Validation is turned off. This may result in missing or invalid attributes."
            )
            wf = json.loads(body["data"])

        self = cls(compile=False)

        if isinstance(wf, cls.__model__):
            self.__dict__.update(
                api_version=wf.api_version,
                kind=wf.kind,
                metadata=wf.metadata,
                spec=wf.spec,
            )
        else:
            self.__dict__.update(**wf)

        self.__validated = validate

        return self

    def compile(self) -> V1alpha1WorkflowTemplate:
        """Compile the WorkflowTemplate class to V1alpha1WorkflowTemplate model."""
        if self.model is not None:
            return self.model

        def _compile(obj: Any):
            if hasattr(obj, "__model__"):
                if not hasattr(obj, "model"):
                    # results of compilation (i.e. dicts, lists)
                    return obj

                if hasattr(obj, "model") and obj.model is not None:
                    # prevents compiled templates from being compiled again
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
                        args[underscore(artifact.name)] = artifact

                    for param in getattr(arguments, "parameters", []) or []:
                        if hasattr(param, "to_dict"):
                            param = V1alpha1Parameter(**param.to_dict())
                        else:
                            param = V1alpha1Parameter(**param)
                        args[underscore(param.name)] = param

                # __call__ sets the `model` attribute when compiled successfully
                return obj.__get__(self).__call__(**args)
            if isinstance(obj, list):
                return list(map(_compile, obj))
            if hasattr(obj, "attribute_map"):
                for attr in obj.attribute_map:
                    value: Any = _compile(getattr(obj, attr))
                    setattr(obj, attr, value)

            return obj

        self.spec = _compile(self.spec)
        self.model = self.__model__(**self.to_dict(omitempty=False))

        self.__validated = True

        return self.model

    def to_file(self, fp: Union[Path, str], fmt="yaml", **kwargs):
        """Dumps the WorkflowTemplate to a file."""
        d: Dict[str, Any] = _utils.sanitize_for_serialization(self)

        opts = kwargs

        if fmt == "json":
            Path(fp).write_text(json.dumps(d, **opts))
        else:
            Path(fp).write_text(yaml.dump(d, Dumper=_utils.BlockDumper, **opts) + "\n")

    def to_yaml(self, omitempty=True, **kwargs) -> str:
        """Returns the WorkflowTemplate manifest as a YAML."""
        d: Dict[str, Any] = self.to_dict(omitempty=omitempty)

        opts = dict(default_flow_style=False)
        opts.update(kwargs)

        serialized = yaml.dump(d, Dumper=_utils.BlockDumper, **opts)

        return serialized

    def to_dict(self, omitempty=True) -> Dict[str, Any]:
        """Returns the WorkflowTemplate manifest as a dict.

        :param omitempty: bool, whether to omit empty values
        """
        result = self.__model__.to_dict(self)

        if omitempty:
            return _utils.omitempty(result)

        return result


class ClusterWorkflowTemplateMeta(WorkflowTemplateMeta):

    __kind__ = "ClusterWorkflowTemplate"
    __model__ = V1alpha1ClusterWorkflowTemplate


class ClusterWorkflowTemplate(WorkflowTemplate, metaclass=ClusterWorkflowTemplateMeta):
    """Base class for Workflows."""

    __model__ = V1alpha1ClusterWorkflowTemplate
