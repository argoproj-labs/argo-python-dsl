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
from ._arguments import artifact, parameter


__all__ = [
    # decorators
    "template",
    # models
    "V1Container",
]

# return type
T = Union[V1Container]


class template:

    __model__ = V1alpha1Template

    def __new__(
        cls, f: Callable[..., T] = None, *, name: str = None,
    ):
        """"""
        self = super().__new__(cls)

        # name of the template will be taken from the function name
        # ( if not provided )
        self.name = name

        if f is not None:
            instance = cls.__call__(self, f)
        else:
            instance = partial(
                cls, **{k: v for k, v in self.__dict__.items() if not k.startswith("_")}
            )

        return instance

    def __call__(self, f: Callable[..., T]) -> Tuple[V1alpha1Template, Union[T, None]]:

        f.__model__ = self.__model__

        # __props__ is set by other relevant template decorators
        for prop in getattr(f, "__props__", {}):
            if prop not in self.__model__.attribute_map:
                raise ValueError(f"Unknown property '{prop}' of '{self.__model__}")

            setattr(self, prop, f.__props__[prop])

        @wraps(f)
        def _wrap_template(*args, **kwargs) -> V1alpha1Template:
            self.name: str = self.name or f.__code__.co_name

            template_spec: T = f(*args, **kwargs)

            if isinstance(template_spec, V1Container):
                self.container = template_spec

            spec = {
                prop: getattr(self, f"{prop}", None)
                for prop in self.__model__.attribute_map
            }

            return self.__model__(**spec)

        return _wrap_template
