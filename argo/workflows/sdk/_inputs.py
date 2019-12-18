from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Inputs,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop

__all__ = ["inputs", "V1alpha1Artifact", "V1alpha1Parameter"]


class inputs:
    """Arguments namespace."""

    class artifact(Prop, extends="inputs"):

        __model__ = V1alpha1Artifact

    class parameter(Prop, extends="inputs"):

        __model__ = V1alpha1Parameter

        def __call__(self, f: Callable):
            parameters: List[V1alpha1Parameter] = [self]

            if not hasattr(f, "__props__"):
                f.__props__ = {"inputs": V1alpha1Inputs(parameters=parameters)}
            else:
                inputs: V1alpha1Arguments = getattr(
                    f.__props__, "inputs", V1alpha1Inputs()
                )

                if not getattr(inputs, "parameters"):
                    inputs.parameters = parameters
                else:
                    inputs.parameters.extend(parameters)

                f.__props__["inputs"] = inputs

            return f
