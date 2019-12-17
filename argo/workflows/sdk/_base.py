import inspect
import typing

from functools import partial
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


class SpecProxy(object):
    """Spec Proxy.

    NOTE: This class is not meant to be used directly.
    """

    def __new__(cls, spec: "Spec", obj: Any):
        self = super(SpecProxy, cls).__new__(cls)

        self._obj = obj
        self._spec = spec

        return self

    def __call__(self, *args, **kwargs):
        T = self._spec.__model__

        spec: Type["Spec"] = self._spec
        ret: Any = self._spec.fget(self._obj, *args, **kwargs)

        for attr, swagger_type in spec.__model__.swagger_types.items():
            t: Any = getattr(models, swagger_type, None)
            if t == type(ret):
                setattr(spec, attr, ret)
                break

        self._spec.__compilehook__(ret)

        attr_dict = {k: spec.__dict__[k] for k in spec.__model__.attribute_map}
        model: T = spec.__model__(**attr_dict)

        self._spec.model = model

        return model


class Spec(property):
    """Base class for Workflow Specs.

    NOTE: This class is not meant to be used directly.
    """

    __model__ = T

    def __new__(
        cls, f: Callable[..., T],
    ):
        f.__model__ = cls.__model__

        self = super().__new__(cls, f)
        self.__compiled_model = None

        # __props__ is set by other relevant template decorators
        for prop in getattr(f, "__props__", {}):
            if prop not in self.__model__.attribute_map:
                raise ValueError(f"Unknown property '{prop}' of '{self.__model__}")

            setattr(self, prop, f.__props__[prop])

        sig: inspect.Signature = inspect.signature(f)
        sig = sig.replace(return_annotation=cls.__model__)
        setattr(self, "__signature__", sig)

        for prop in cls.__model__.attribute_map.keys():
            setattr(self, prop, None)

        return self

    def __call__(self, *args, **kwargs) -> T:
        # This function is required for the call signature and is NEVER called
        raise NotImplementedError("This function shouldn't be called directly.")

    def __get__(self, obj: Any, objtype: Any = None, **kwargs):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"Unreadable attribute '{self.fget}'")
        return SpecProxy(self, obj)

    def __compilehook__(self, *args, **kwargs) -> None:
        """A hook executed after the model has been compiled."""
        pass

    @property
    def model(self) -> Union[T, None]:
        """Return the model specification.

        :returns: T if compiled, otherwise None
        """
        return self.__compiled_model

    @model.setter
    def model(self, spec: T):
        if not isinstance(spec, self.__model__):
            raise TypeError(f"Expected type {self.__model__}, got: {type(spec)}")

        self.__compiled_model = spec


class PropMeta(type):
    """Prop metaclass."""

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
    """Base class for Spec props.

    NOTE: This class is not meant to be used directly.
    """

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
