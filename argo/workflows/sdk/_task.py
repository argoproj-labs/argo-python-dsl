from functools import wraps
from functools import partial

from typing import Any
from typing import Dict
from typing import Callable
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from argo.workflows.client.models import *

from ._base import Prop

T = TypeVar("T")


class task():

    __model__ = V1alpha1DAGTask

    def __new__(
        cls,
        f: Callable = None,
        arguments: V1alpha1Arguments = None,
        continue_on: V1alpha1ContinueOn = None,
        dependencies: List[str] = None,
        name: str = None,
        template: str = None,
        template_ref: V1alpha1TemplateRef = None,
        when: str = None,
        with_items: List[str] = None,
        with_param: str = None,
        with_sequence: V1alpha1Sequence = None
    ):
        """"""
        # The name of the task will be taken from the function name
        # ( if not provided )
        self = type("Task", (), {"__model__": cls.__model__})
        self.name = name

        self.arguments = arguments
        self.continue_on = continue_on
        self.dependencies = dependencies
        self.template = template
        self.template_ref = template_ref
        self.when = when
        self.with_items = with_items
        self.with_param = with_param
        self.with_sequence = with_sequence

        if f is not None:
            return cls.__call__(self, f)

        return partial(cls, **{k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def __call__(self, f: Callable[..., V1alpha1DAGTask]) -> V1alpha1DAGTask:

        @wraps(f)
        def _wrap_task(*args, **kwargs) -> T:
            template: V1alpha1Template = f()

            # __props__ is set by other relevant task decorators
            for prop in getattr(f, "__props__", {}):
                if prop not in self.__model__.attribute_map:
                    raise ValueError(
                        f"Unknown property '{prop}' of '{self.__model__}"
                    )

                setattr(self, prop, f.__props__[prop])

            self.name: str = self.name or f.__code__.co_name
            self.template = template.name

            task_spec = {
                prop: getattr(self, f"{prop}") for prop in self.__model__.attribute_map
            }

            return task.__model__(**task_spec), template

        return _wrap_task


class dependencies(Prop):

    __model__ = List[str]


class continue_on(Prop):

    __model__ = V1alpha1ContinueOn
