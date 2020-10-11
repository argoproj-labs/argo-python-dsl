import ntpath
import pathlib

from argo.workflows.dsl import Workflow
from argo.workflows.dsl.tasks import task
from argo.workflows.dsl.tasks import dependencies
from argo.workflows.dsl.templates import inputs
from argo.workflows.dsl.templates import outputs
from argo.workflows.dsl.templates import artifact
from argo.workflows.dsl.templates import template
from argo.workflows.dsl.templates import V1alpha1Artifact
from argo.workflows.dsl.templates import V1alpha1Template
from argo.workflows.dsl.templates import V1Container


class Artifacts(Workflow):
    @task
    def generate(self) -> V1alpha1Template:
        return self.whalesay()

    @task
    @artifact(name="message", _from="{{tasks.generate.outputs.artifacts.hello-art}}")
    @dependencies(["generate"])
    def consume_artifact(self, message: V1alpha1Artifact) -> V1alpha1Template:
        return self.print_message(message=message)

    @template
    @outputs.artifact(name="hello-art", path="/tmp/hello_world.txt")
    def whalesay(self) -> V1Container:
        container = V1Container(
            name="whalesay",
            image="docker/whalesay:latest",
            command=["sh", "-c"],
            args=["cowsay hello world | tee /tmp/hello_world.txt"],
        )

        return container

    @template
    @inputs.artifact(name="message", path="/tmp/message")
    def print_message(self, message: V1alpha1Artifact) -> V1Container:
        container = V1Container(
            name="print-message",
            image="alpine:latest",
            command=["sh", "-c"],
            args=["cat", "/tmp/message"],
        )

        return container


if __name__ == "__main__":
    wf = Artifacts()
    wf_file = ntpath.basename(__file__).replace(".py", ".yaml")
    wf.to_file(f"{pathlib.Path(__file__).parent}/{wf_file}")
