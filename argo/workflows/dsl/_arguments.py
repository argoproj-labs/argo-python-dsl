from typing import Any
from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop

__all__ = ["artifact", "parameter", "V1alpha1Artifact", "V1alpha1Parameter"]


class artifact(Prop, extends=("arguments", V1alpha1Arguments)):

    __model__ = V1alpha1Artifact

    def __call__(self, f: Callable):
        artifacts: List[V1alpha1Artifact] = [self]

        prop: Any
        prop_name: str
        prop_name, prop = self.__extends__

        if not hasattr(f, "__props__"):
            f.__props__ = {prop_name: prop(artifacts=artifacts)}
        else:
            arguments: Type[prop] = f.__props__.get(prop_name, prop())

            if not getattr(arguments, "artifacts"):
                arguments.artifacts = artifacts
            else:
                arguments.artifacts.extend(artifacts)

            f.__props__[prop_name] = arguments

        return f

class parameter(Prop, extends=("arguments", V1alpha1Arguments)):

    __model__ = V1alpha1Parameter

    def __call__(self, f: Callable):
        parameters: List[V1alpha1Parameter] = [self]

        prop: Any
        prop_name: str
        prop_name, prop = self.__extends__

        if not hasattr(f, "__props__"):
            f.__props__ = {prop_name: prop(parameters=parameters)}
        else:
            arguments: Type[prop] = f.__props__.get(prop_name, prop())

            if not getattr(arguments, "parameters"):
                arguments.parameters = parameters
            else:
                arguments.parameters.extend(parameters)

            f.__props__[prop_name] = arguments

        return f
