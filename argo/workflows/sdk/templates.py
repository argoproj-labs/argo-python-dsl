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
    V1alpha1Arguments,
    V1alpha1Inputs,
    V1alpha1Outputs,
    V1alpha1Template,
    V1Container,
)

from ._base import Prop
from ._base import Spec
from ._arguments import artifact, parameter


__all__ = [
    # decorators
    "template",
    # models
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
        self.inputs = V1alpha1Inputs(
            parameters=[
                {
                    "name": p.name,
                    "default": p.default if not p.default == inspect._empty else None,
                }
                for p in inspect.signature(f).parameters.values()
                if p.name not in ["self", "cls"]
            ]
        )

        return self
