import inspect

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
    V1alpha1Artifact,
    V1alpha1Inputs,
    V1alpha1Outputs,
    V1alpha1Parameter,
    V1alpha1Template,
    V1Container,
)

from ._arguments import arguments
from ._base import Prop
from ._base import Spec
from ._inputs import inputs


__all__ = [
    # decorators
    "arguments",
    "inputs",
    "template",
    # models
    "V1alpha1Artifact",
    "V1alpha1Parameter",
    "V1Container",
]

# return type
T = Union[V1Container]


class template(Spec):

    __model__ = V1alpha1Template

    def __new__(cls, f: Callable[..., T]):
        """Workflow spec for V1alpha1Template."""
        self = super().__new__(cls, f)
        self.name: str = f.__code__.co_name

        return self
