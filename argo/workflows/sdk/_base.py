import typing

from functools import wraps

from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Tuple
from typing import TypeVar
from typing import Union

from argo.workflows import models

T = TypeVar("T")


class Spec(property):
    """Base class for Workflow Specs."""

    __model__ = T

    def __new__(
        cls, f: Callable[..., T],
    ):
        self = super().__new__(cls)

        for prop in cls.__model__.attribute_map.keys():
            setattr(self, prop, None)

        return self

    def __call__(self, f: Callable[..., T]) -> Callable[..., T]:
        f.__model__ = self.__model__

        # __props__ is set by other relevant template decorators
        for prop in getattr(f, "__props__", {}):
            if prop not in self.__model__.attribute_map:
                raise ValueError(f"Unknown property '{prop}' of '{self.__model__}")

            setattr(self, prop, f.__props__[prop])

        return f


class PropMeta(type):

    __model__ = Generic[T]

    def __new__(
        cls, name: Union[str, T], bases: Tuple[T, ...], props: Dict[str, Any], **kwargs
    ):
        __model__ = props.get("__model__", None)

        if __model__ is not None:
            # typing
            if hasattr(typing, __model__.__name__):
                props["__type__"] = __model__.__extra__
                bases = (
                    *bases,
                    props["__type__"],
                )
            # argo models
            elif hasattr(models, __model__.__name__):
                bases = (
                    *bases,
                    __model__,
                )

        return super().__new__(cls, name, bases, props)


class Prop(metaclass=PropMeta):
    """Base class for Spec props."""

    def __init_subclass__(cls):
        return super().__init_subclass__()

    def __call__(self, f: Callable):
        if not hasattr(f, "__props__"):
            f.__props__ = {self.name: self}
        else:
            f.__props__.update({self.name: self})

        return f

    @property
    def name(self) -> str:
        return self.__class__.__name__
