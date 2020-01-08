from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Inputs,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop
from ._arguments import artifact as artifact
from ._arguments import parameter as parameter

__all__ = ["inputs", "V1alpha1Artifact", "V1alpha1Parameter"]


class inputs:
    """Arguments namespace."""

    class artifact(artifact, extends=("inputs", V1alpha1Inputs)):

        __model__ = V1alpha1Artifact

    class parameter(parameter, extends=("inputs", V1alpha1Inputs)):

        __model__ = V1alpha1Parameter
