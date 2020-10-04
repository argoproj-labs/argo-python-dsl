import ntpath
import pathlib

from argo.workflows.dsl import Workflow
from argo.workflows.dsl.tasks import task
from argo.workflows.dsl.tasks import dependencies
from argo.workflows.dsl.templates import inputs
from argo.workflows.dsl.templates import parameter
from argo.workflows.dsl.templates import template
from argo.workflows.dsl.templates import V1alpha1Parameter
from argo.workflows.dsl.templates import V1alpha1Template
from argo.workflows.dsl.templates import V1Container


class DagDiamond(Workflow):
    @task
    @parameter(name="message", value="A")
    def A(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @parameter(name="message", value="B")
    @dependencies(["A"])
    def B(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @parameter(name="message", value="C")
    @dependencies(["A"])
    def C(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @parameter(name="message", value="D")
    @dependencies(["B", "C"])
    def D(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @template
    @inputs.parameter(name="message")
    def echo(self, message: V1alpha1Parameter) -> V1Container:
        container = V1Container(
            image="alpine:3.7",
            name="echo",
            command=["echo", "{{inputs.parameters.message}}"],
        )

        return container


if __name__ == "__main__":
    wf = DagDiamond()
    wf_file = ntpath.basename(__file__).replace(".py", ".yaml")
    wf.to_file(f"{pathlib.Path(__file__).parent}/{wf_file}")
