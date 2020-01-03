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
)

from ._arguments import arguments
from ._base import Prop
from ._base import Spec
from ._inputs import inputs
from ._outputs import outputs


__all__ = [
    # decorators
    "arguments",
    "closure",
    "inputs",
    "outputs",
    "template",
    # models
    "V1alpha1Arguments",
    "V1alpha1Artifact",
    "V1alpha1Parameter",
    "V1alpha1ResourceTemplate",
    "V1alpha1ScriptTemplate",
    "V1Container",
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


class closure(Prop):
    """Workflow spec for V1alpha1Template using closure."""

    __model__ = V1alpha1ScriptTemplate

    def __init__(self, image: str):
        """Create script from a function source.

        :param image: str, image to be used to execute the script
        """
        super().__init__(source="")

        self.name = "script"

        self.image = image
        self.command = ["python"]

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

        return tmpl
