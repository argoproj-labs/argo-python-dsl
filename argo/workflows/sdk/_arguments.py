from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop

__all__ = ["arguments", "V1alpha1Artifact", "V1alpha1Parameter"]


class arguments:
    """Arguments namespace."""

    class artifact(Prop, extends="arguments"):

        __model__ = V1alpha1Artifact

    class parameter(Prop, extends="arguments"):

        __model__ = V1alpha1Parameter

        def __call__(self, f: Callable):
            parameters: List[V1alpha1Parameter] = [self]

            if not hasattr(f, "__props__"):
                f.__props__ = {"arguments": V1alpha1Arguments(parameters=parameters)}
            else:
                arguments: V1alpha1Arguments = getattr(
                    f.__props__, "arguments", V1alpha1Arguments()
                )

                if not getattr(arguments, "parameters"):
                    arguments.parameters = parameters
                else:
                    arguments.parameters.extend(parameters)

                f.__props__["arguments"] = arguments

            return f
