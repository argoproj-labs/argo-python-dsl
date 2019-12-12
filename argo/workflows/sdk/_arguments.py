from typing import List

from argo.workflows.client.models import (
    V1alpha1Artifact,
    V1alpha1Parameter
)

from ._base import Prop


class artifact(Prop):

    __model__ = V1alpha1Artifact


class parameter(Prop):

    __model__ = V1alpha1Parameter
