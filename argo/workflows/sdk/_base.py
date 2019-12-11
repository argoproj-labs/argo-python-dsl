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


class PropMeta(type):

    __model__ = Generic[T]

    def __new__(cls, name: Union[str, T], bases: Tuple[T, ...], props: Dict[str, Any], **kwargs):
        __model__ = props.get("__model__", None)

        if __model__ is not None:
            # typing
            if hasattr(typing, __model__.__name__):
                props["__type__"] = __model__.__extra__
                bases = (*bases, props["__type__"],)
            # argo models
            elif hasattr(models, __model__.__name__):
                props.update(zip(__model__.attribute_map.keys(), [None]))
                bases = (*bases, __model__,)

        return super().__new__(cls, name, bases, props)


class Prop(metaclass=PropMeta):

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
