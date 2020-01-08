from typing import Callable
from typing import List

from argo.workflows.client.models import (
    V1alpha1Outputs,
    V1alpha1Artifact,
    V1alpha1Parameter,
)

from ._base import Prop
from ._arguments import artifact as artifact
from ._arguments import parameter as parameter

__all__ = ["outputs", "V1alpha1Artifact", "V1alpha1Parameter"]


class outputs:
    """Outputs namespace."""

    class artifact(artifact, extends=("outputs", V1alpha1Outputs)):

        __model__ = V1alpha1Artifact

    class parameter(parameter, extends=("outputs", V1alpha1Outputs)):

        __model__ = V1alpha1Parameter
