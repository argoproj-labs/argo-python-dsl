import pathlib
import ntpath

from argo.workflows.dsl import task
from argo.workflows.dsl.tasks import parameter
from argo.workflows.dsl.templates import inputs
from argo.workflows.dsl import Workflow
from argo.workflows.dsl.templates import template
from argo.workflows.dsl.templates import V1Container
from argo.workflows.dsl.tasks import V1alpha1Template
from argo.workflows.dsl.tasks import with_items


class Loop(Workflow):
    @task
    @with_items(["apple", "orange", "pineapple", "watermelon"])
    @parameter(name="message", value="{{item}}")
    def generate(self, message) -> V1alpha1Template:
        return self.whalesay("")

    @template
    @inputs.parameter(name="message")
    def whalesay(self, message: str) -> V1Container:
        container = V1Container(
            image="docker/whalesay:latest",
            name="whalesay",
            command=["cowsay"],
            args=["{{inputs.parameters.message}}"],
        )
        return container


if __name__ == "__main__":
    wf = Loop()
    wf_file = ntpath.basename(__file__).replace(".py", ".yaml")
    wf.to_file(f"{pathlib.Path(__file__).parent}/{wf_file}")