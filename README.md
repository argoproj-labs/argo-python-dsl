# argo-python-sdk
Python SDK for [Argo Workflows](https://github.com/argoproj/argo)

:warning: The project is currently in a development phase and is not yet meant for production purposes.

<br>

## Examples

#### Hello World

This example demonstrates the simplest functionality. Defining a `Workflow` by subclassing the `Workflow` class and a single template with the `@template` decorator.

The entrypoint to the workflow is defined as an `entrypoint` class property.

<table>
<tr><th>Argo YAML</th><th>Argo Python</th></tr>
<tr>
<td valign="top"><p>

```yaml
# @file: hello-world.yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: hello-world
  generateName: hello-world-
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      name: whalesay
      image: docker/whalesay:latest
      command: [cowsay]
      args: ["hello world"]
```

</p></td>
<td valign="top"><p>

```python
from argo.workflows.sdk import Workflow
from argo.workflows.sdk import template

from argo.workflows.sdk.templates import V1Container


class HelloWorld(Workflow):

    entrypoint = "whalesay"

    @template
    def whalesay(self) -> V1Container:
        container = V1Container(
            image="docker/whalesay:latest",
            name="whalesay",
            command=["cowsay"],
            args=["hello world"]
        )

        return container
```

</p></td>
</tr>
</table>

#### Dag Diamond

This example demonstrates tasks defined via dependencies forming a *diamond* structure. Tasks are defined using the `@task` decorator and they **must return a valid template**.

The entrypoint is automatically created as `main` for the top-level tasks of the `Workflow`.

<table>
<tr><th>Argo YAML</th><th>Argo Python</th></tr>
<tr>
<td valign="top"><p>

```yaml
# @file: dag-diamond.yaml
# The following workflow executes a diamond workflow
#
#   A
#  / \
# B   C
#  \ /
#   D
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: dag-diamond
  generateName: dag-diamond-
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - name: A
        template: echo
        arguments:
          parameters: [{name: message, value: A}]
      - name: B
        dependencies: [A]
        template: echo
        arguments:
          parameters: [{name: message, value: B}]
      - name: C
        dependencies: [A]
        template: echo
        arguments:
          parameters: [{name: message, value: C}]
      - name: D
        dependencies: [B, C]
        template: echo
        arguments:
          parameters: [{name: message, value: D}]

  # @task: [A, B, C, D]
  - name: echo
    inputs:
      parameters:
      - name: message
    container:
      name: echo
      image: alpine:3.7
      command: [echo, "{{inputs.parameters.message}}"]
status: {}
```

</p></td>
<td valign="top"><p>

```python
from argo.workflows.sdk import Workflow

from argo.workflows.sdk.tasks import *
from argo.workflows.sdk.templates import *


class DagDiamond(Workflow):

    @task
    @arguments.parameter(name="message", value="A")
    def A(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @arguments.parameter(name="message", value="B")
    @dependencies(["A"])
    def B(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @arguments.parameter(name="message", value="C")
    @dependencies(["A"])
    def C(self, message: V1alpha1Parameter) -> V1alpha1Template:
        return self.echo(message=message)

    @task
    @arguments.parameter(name="message", value="D")
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

```

</p></td>
</tr>
</table>

<br>

For more examples see the [examples](https://github.com/CermakM/argo-python-sdk/tree/master/examples) folder.

<br>

---

Authors:
- [ Maintainer ] Marek Cermak <macermak@redhat.com>
- Vaclav Pavlin <vpavlin@redhat.com>

@[AICoE](https://github.com/AICoE), Red Hat