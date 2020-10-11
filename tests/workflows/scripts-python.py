import ntpath
import pathlib
import textwrap

from argo.workflows.dsl import Workflow
from argo.workflows.dsl.tasks import task
from argo.workflows.dsl.tasks import dependencies
from argo.workflows.dsl.tasks import parameter
from argo.workflows.dsl.templates import inputs
from argo.workflows.dsl.templates import template
from argo.workflows.dsl.templates import V1alpha1Template
from argo.workflows.dsl.templates import V1Container
from argo.workflows.dsl.templates import V1alpha1ScriptTemplate


class ScriptsPython(Workflow):
    @task
    def generate(self) -> V1alpha1Template:
        return self.gen_random_int()

    @task
    @parameter(name="message", value="{{tasks.generate.outputs.result}}")
    @dependencies(["generate"])
    def print(self, message: str) -> V1alpha1Template:
        return self.print_message(message)

    @template
    def gen_random_int(self) -> V1alpha1ScriptTemplate:
        source = textwrap.dedent(
            """\
          import random
          i = random.randint(1, 100)
          print(i)
        """
        )

        template = V1alpha1ScriptTemplate(
            image="python:alpine3.6",
            name="gen-random-int",
            command=["python"],
            source=source,
        )

        return template

    @template
    @inputs.parameter(name="message")
    def print_message(self, message: str) -> V1Container:
        container = V1Container(
            image="alpine:latest",
            name="print-message",
            command=["sh", "-c"],
            args=["echo result was: {{inputs.parameters.message}}"],
        )

        return container


wf = ScriptsPython()


if __name__ == "__main__":
    wf = ScriptsPython()
    wf_file = ntpath.basename(__file__).replace(".py", ".yaml")
    wf.to_file(f"{pathlib.Path(__file__).parent}/{wf_file}")
