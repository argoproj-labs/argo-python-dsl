from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop

__all__ = ["arguments"]


class argument:
    """Argument namespace."""

    class artifact(Prop):

        __model__ = V1alpha1Artifact

    class parameter(Prop):

        __model__ = V1alpha1Parameter

        def __call__(self, f: Callable):
            if not hasattr(f, "__props__"):
                f.__props__ = {"arguments": V1alpha1Arguments(parameters=[self])}
            else:
                parameters = [self]

                arguments: Dict[str, Any] = getattr(f.__props__, "arguments", {})
                if not arguments.get("parameters"):
                    arguments["parameters"] = parameters
                else:
                    arguments["parameters"].extend(parameters)

                f.__props__["arguments"] = arguments

            return f

