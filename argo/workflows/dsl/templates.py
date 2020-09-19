import inspect
import re
import textwrap

from inflection import dasherize
from functools import partial
from functools import wraps

from typing import Any
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1Inputs,
    V1alpha1Outputs,
    V1alpha1Parameter,
    V1alpha1ResourceTemplate,
    V1alpha1ScriptTemplate,
    V1alpha1Template,
    V1Container,
    V1ContainerPort,
    V1EnvFromSource,
    V1EnvVar,
    V1Lifecycle,
    V1Probe,
    V1ResourceRequirements,
    V1SecurityContext,
    V1VolumeDevice,
    V1VolumeMount,
)

from ._arguments import artifact
from ._arguments import parameter
from ._base import Prop
from ._base import Spec
from ._inputs import inputs
from ._outputs import outputs


__all__ = [
    # decorators
    "artifact",
    "closure",
    "inputs",
    "outputs",
    "parameter",
    "scope",
    "template",
    # models
    "V1alpha1Arguments",
    "V1alpha1Artifact",
    "V1alpha1Parameter",
    "V1alpha1ResourceTemplate",
    "V1alpha1ScriptTemplate",
    "V1Container",
    "V1ContainerPort",
    "V1EnvFromSource",
    "V1EnvVar",
    "V1Lifecycle",
    "V1Probe",
    "V1ResourceRequirements",
    "V1SecurityContext",
    "V1VolumeDevice",
    "V1VolumeMount",
]

# return type
T = Union[V1alpha1ResourceTemplate, V1alpha1ScriptTemplate, V1Container]


class template(Spec):

    __model__ = V1alpha1Template

    def __new__(cls, f: Callable[..., T]):
        """Workflow spec for V1alpha1Template."""
        self = super().__new__(cls, f)
        self.name = dasherize(f.__code__.co_name)

        return self


class closure(Prop, command=["python"]):
    """Workflow spec for V1alpha1Template using closure."""

    __model__ = V1alpha1ScriptTemplate

    def __init__(
        self,
        image: str,
        scope: str = None,
        *,
        env: List[V1EnvVar] = None,
        env_from: List[V1EnvFromSource] = None,
        image_pull_policy: str = None,
        lifecycle: V1Lifecycle = None,
        liveness_probe: V1Probe = None,
        ports: List[V1ContainerPort] = None,
        readiness_probe: V1Probe = None,
        resources: V1ResourceRequirements = None,
        security_context: V1SecurityContext = None,
        stdin: bool = None,
        stdin_once: bool = None,
        termination_message_path: str = None,
        termination_message_policy: str = None,
        tty: bool = None,
        volume_devices: List[V1VolumeDevice] = None,
        volume_mounts: List[V1VolumeMount] = None,
        working_dir: str = None,
    ):  # noqa: E501
        super().__init__(**self.__dict__, name="script", source="", image="")

        self.image = image
        self.scope = scope

        if env is not None:
            self.env = env
        if env_from is not None:
            self.env_from = env_from
        if image_pull_policy is not None:
            self.image_pull_policy = image_pull_policy
        if lifecycle is not None:
            self.lifecycle = lifecycle
        if liveness_probe is not None:
            self.liveness_probe = liveness_probe
        if ports is not None:
            self.ports = ports
        if readiness_probe is not None:
            self.readiness_probe = readiness_probe
        if resources is not None:
            self.resources = resources
        if security_context is not None:
            self.security_context = security_context
        if stdin is not None:
            self.stdin = stdin
        if stdin_once is not None:
            self.stdin_once = stdin_once
        if termination_message_path is not None:
            self.termination_message_path = termination_message_path
        if termination_message_policy is not None:
            self.termination_message_policy = termination_message_policy
        if tty is not None:
            self.tty = tty
        if volume_devices is not None:
            self.volume_devices = volume_devices
        if volume_mounts is not None:
            self.volume_mounts = volume_mounts
        if working_dir is not None:
            self.working_dir = working_dir

    def __call__(self, f: Callable[..., None]) -> template:
        super().__call__(f)

        self.name = dasherize(f.__code__.co_name)

        source: List[str]
        source, _ = inspect.getsourcelines(f.__code__)

        co_start: int = 0
        for i, line in enumerate(source):
            if re.search(r"\)( -> (.+))?:[\s\n\r]+$", line):
                co_start = i + 1
                break

        self.source = textwrap.dedent("".join(source[co_start:]))

        tmpl = template(f)
        tmpl.callable = False

        tmpl.__closure__ = self.scope

        return tmpl


class scope:
    """Mark scope for closures."""

    def __init__(self, name: str):
        self.name = name

    def __call__(self, f: Callable) -> Callable:
        m = staticmethod(f)
        m.__scope__ = self.name

        return m

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        """Validate and set scope name.

        :raises: ValueError
        """
        valid_pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"

        if not bool(re.match(valid_pattern, name)):
            raise ValueError(
                f"String {name} is not valid scope name."
                f"Scope name must match expression '{valid_pattern}'."
            )

        self._name = name
