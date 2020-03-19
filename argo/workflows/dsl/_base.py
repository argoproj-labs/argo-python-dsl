import inspect
import typing

from functools import partial
from functools import wraps

from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from argo.workflows.client import models

T = TypeVar("T")


class SpecProxy(object):
    """Spec Proxy.

    NOTE: This class is not meant to be used directly.
    """

    def __new__(cls, spec: "Spec", obj: Any, callable: bool):
        self = super(SpecProxy, cls).__new__(cls)

        self._obj = obj
        self._spec = spec

        self._callable = callable

        return self

    def __call__(self, *args, **kwargs):
        spec: "Spec" = self._spec

        T = Type[spec.__model__]

        if self._callable:
            ret: Any = spec.fget(self._obj, *args, **kwargs)

            if hasattr(spec.__model__, "swagger_types"):
                for attr, swagger_type in spec.__model__.swagger_types.items():
                    t: Any = getattr(models, swagger_type, None)
                    if t == type(ret):
                        setattr(spec, attr, ret)
                        break
            else:
                for attr, openapi_type in spec.__model__.openapi_types.items():
                    t: Any = getattr(models, openapi_type, None)
                    if t == type(ret):
                        setattr(spec, attr, ret)
                        break

            spec.__init_model__(ret, *args, **kwargs)

        attr_dict: Dict[str, Any] = {
            k: spec.__dict__[k] for k in spec.__model__.attribute_map
        }
        model: T = spec.__model__(**attr_dict)

        self._spec.model = model

        return model


class Spec(property):
    """Base class for Workflow Specs.

    NOTE: This class is not meant to be used directly.
    """

    __model__ = T

    def __new__(cls, f: Callable[..., T]):
        f.__model__ = cls.__model__

        self = super().__new__(cls, f)
        self.__callable = True
        self.__compiled_model = None

        for prop in cls.__model__.attribute_map.keys():
            setattr(self, prop, None)

        # __props__ is set by Type[Prop] decorator
        for prop in getattr(f, "__props__", {}):
            if prop not in self.__model__.attribute_map:
                raise ValueError(f"Unknown property '{prop}' of '{self.__model__}")

            setattr(self, prop, f.__props__[prop])

        sig: inspect.Signature = inspect.signature(f)
        sig = sig.replace(return_annotation=cls.__model__)
        setattr(self, "__signature__", sig)

        return self

    def __call__(self, *args, **kwargs) -> T:
        # This function is required for the call signature and should NOT be called
        raise NotImplementedError("This function shouldn't be called directly.")

    def __get__(self, obj: Any, objtype: Any = None, **kwargs):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"Unreadable attribute '{self.fget}'")
        return SpecProxy(self, obj, callable=self.__callable)

    def __init_model__(self, *args, **kwargs) -> None:
        """A hook executed before creation of a model."""

    @property
    def callable(self) -> bool:
        """Return whether current spec is callable."""
        return self.__callable

    @callable.setter
    def callable(self, is_callable: bool):
        """Set whether current spec is callable."""
        self.__callable = is_callable

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
            if hasattr(__model__, "__origin__"):
                try:
                    # Python 3.5, 3.6
                    props["__type__"] = __model__.__extra__
                except AttributeError:
                    # Python >=3.7
                    props["__type__"] = __model__.__origin__
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

        if kwargs.get("extends") is not None:
            props["__extends__"] = kwargs.pop("extends")

        props.update({"name": props.get("name", name)})
        props.update(kwargs)

        return super().__new__(cls, name, bases, props)


class Prop(metaclass=PropMeta):
    """Base class for Spec props.

    NOTE: This class is not meant to be used directly.
    """

    def __init_subclass__(cls):
        return super().__init_subclass__()

    def __call__(self, f: Callable, **kwargs) -> Callable:
        if "name" in kwargs:
            name = kwargs.pop("name")
        else:
            name = self.name

        dct: Dict[str, any] = {name: self, **kwargs}
        if not hasattr(f, "__props__"):
            f.__props__ = dct
        else:
            f.__props__.update(dct)

        return f
