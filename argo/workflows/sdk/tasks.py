from functools import partial
from functools import wraps

from typing import Any
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1ContinueOn,
    V1alpha1DAGTask,
    V1alpha1Parameter,
    V1alpha1Sequence,
    V1alpha1Template,
    V1alpha1TemplateRef,
)

from ._base import Prop
from ._arguments import artifact, parameter


__all__ = [
    # decorators
    "artifact",
    "continue_on",
    "dependencies",
    "parameter",
    "task",
    "when",
    "with_items",
    "with_param",
    "with_sequence",
    # models
    "V1alpha1Template",
    "V1alpha1TemplateRef",
]

# return type
T = Union[V1alpha1Template, V1alpha1TemplateRef]


class task:

    __model__ = V1alpha1DAGTask

    def __new__(
        cls,
        f: Callable[..., T] = None,
        *,
        artifacts: List[V1alpha1Artifact] = None,
        continue_on: V1alpha1ContinueOn = None,
        dependencies: List[str] = None,
        name: str = None,
        parameters: List[V1alpha1Parameter] = None,
        when: str = None,
        with_items: List[str] = None,
        with_param: str = None,
        with_sequence: V1alpha1Sequence = None,
    ):
        """"""
        self = super().__new__(cls)

        # name of the task will be taken from the function name
        # ( if not provided )
        self.name = name

        self.continue_on = continue_on
        self.dependencies = dependencies
        self.when = when
        self.with_items = with_items
        self.with_param = with_param
        self.with_sequence = with_sequence

        if f is not None:
            instance = cls.__call__(self, f)
        else:
            instance = partial(
                cls, **{k: v for k, v in self.__dict__.items() if not k.startswith("_")}
            )

        # additional model properties

        self.arguments: V1alpha1Arguments = V1alpha1Arguments(
            dict(artifacts=artifacts, parameters=parameters)
        )

        # template is the name of the template returned by the wrapped function
        # (if applicable)
        self.template: str = None
        # template_ref is the template_ref returned by the function
        # (if applicable)
        self.template_ref: V1alpha1TemplateRef = None

        return instance

    def __call__(self, f: Callable[..., T]) -> Tuple[V1alpha1DAGTask, Union[T, None]]:

        f.__model__ = self.__model__

        # __props__ is set by other relevant task decorators
        for prop in getattr(f, "__props__", {}):
            if prop not in self.__model__.attribute_map:
                raise ValueError(f"Unknown property '{prop}' of '{self.__model__}")

            setattr(self, prop, f.__props__[prop])

        @wraps(f)
        def _wrap_task(
            klass: Type["Workflow"], *args, **kwargs
        ) -> Tuple[V1alpha1DAGTask, Union[V1alpha1Template, V1alpha1TemplateRef]]:
            ret: Union[T, Callable] = f(klass, *args, **kwargs)

            template_or_template_ref: T
            if isinstance(ret, Callable):
                # wrapped method
                template_or_template_ref = ret.__call__(klass, *args, **kwargs)
            else:
                template_or_template_ref = ret

            if isinstance(template_or_template_ref, V1alpha1TemplateRef):
                self.template_ref = template_or_template_ref
            elif isinstance(template_or_template_ref, V1alpha1Template):
                self.template = template_or_template_ref.name
            else:
                raise TypeError(f"Expected {T}, got: {type(template_or_template_ref)}")

            self.name: str = self.name or f.__code__.co_name

            spec = {
                prop: getattr(self, f"{prop}", None)
                for prop in self.__model__.attribute_map
            }

            return self.__model__(**spec), template_or_template_ref

        return _wrap_task


class dependencies(Prop):

    __model__ = List[str]


class continue_on(Prop):

    __model__ = V1alpha1ContinueOn


class when(Prop):

    __model__ = str


class with_items(Prop):

    __model__ = List[str]


class with_param(Prop):

    __model__ = str


class with_sequence(Prop):

    __model__ = V1alpha1Sequence
