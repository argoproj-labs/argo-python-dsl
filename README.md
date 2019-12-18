# argo-python-sdk
Python SDK for [Argo Workflows](https://github.com/argoproj/argo)

:warning: The project is currently in a development phase and is not yet meant for production purposes.

<div style="text-align: justify">

If you're new to Argo, we recommend checking out the examples in pure YAML. The language is descriptive and the Argo [examples](https://github.com/argoproj/argo/tree/master/examples) provide an exhaustive explanation.

For a more experienced audience, this SDK grants you the ability to programatically define Argo Workflows in Python which is then translated to the Argo YAML specification.

The SDK makes use of the Argo models defined in the [Argo Python client](https://github.com/CermakM/argo-client-python) repository. Combining the two approaches we are given the whole low-level control over Argo Workflows.

</div>

## Getting started

#### Hello World

<div style="text-align: justify">

This example demonstrates the simplest functionality. Defining a `Workflow` by subclassing the `@Workflow` class and a single template with the `@template` decorator.

The entrypoint to the workflow is defined as an `entrypoint` class property.

</div>

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

#### DAG: Tasks

<div style="text-align: justify">

This example demonstrates tasks defined via dependencies forming a *diamond* structure. Tasks are defined using the `@task` decorator and they **must return a valid template**.

The entrypoint is automatically created as `main` for the top-level tasks of the `Workflow`.

</div>

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

#### Artifacts

<div style="text-align: justify">

`Artifacts` can be passed similarly to `parameters` in three forms: `arguments`, `inputs` and `outputs`

I.e.: `inputs.artifact(...)`

Both artifacts and parameters are passed **one by one**, which means that for multiple artifacts (parameters), one should call:


```python
@inputs.artifact(name="artifact", ...)
@inputs.parameter(name="parameter_a", ...)
@inputs.parameter(...)
def foo(self, artifact: V1alpha1Artifact, prameter_b: V1alpha1Parameter, ...): pass
```

A complete example:

</div>

<table>
<tr><th>Argo YAML</th><th>Argo Python</th></tr>
<tr>
<td valign="top"><p>

```yaml
# @file: artifacts.yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: artifact-passing
  generateName: artifact-passing-
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - name: generate-artifact
        template: whalesay
      - name: consume-artifact
        template: print-message
        arguments:
          artifacts:
          # bind message to the hello-art artifact
          # generated by the generate-artifact step
          - name: message
            from: "{{tasks.generate-artifact.outputs.artifacts.hello-art}}"

  - name: whalesay
    container:
      name: "whalesay"
      image: docker/whalesay:latest
      command: [sh, -c]
      args: ["cowsay hello world | tee /tmp/hello_world.txt"]
    outputs:
      artifacts:
      # generate hello-art artifact from /tmp/hello_world.txt
      # artifacts can be directories as well as files
      - name: hello-art
        path: /tmp/hello_world.txt

  - name: print-message
    inputs:
      artifacts:
      # unpack the message input artifact
      # and put it at /tmp/message
      - name: message
        path: /tmp/message
    container:
      name: "print-message"
      image: alpine:latest
      command: [sh, -c]
      args: ["cat", "/tmp/message"]
```

</p></td>
<td valign="top"><p>

```python
from argo.workflows.sdk import Workflow

from argo.workflows.sdk.tasks import *
from argo.workflows.sdk.templates import *

class ArtifactPassing(Workflow):

    @task
    def generate_artifact(self) -> V1alpha1Template:
        return self.whalesay()

    @task
    @arguments.artifact(
        name="message",
        _from="{{tasks.generate-artifact.outputs.artifacts.hello-art}}"
    )
    def consume_artifact(self, message: V1alpha1Artifact) -> V1alpha1Template:
        return self.print_message(message=message)

    @template
    @outputs.artifact(name="hello-art", path="/tmp/hello_world.txt")
    def whalesay(self) -> V1Container:
        container = V1Container(
            name="whalesay",
            image="docker/whalesay:latest",
            command=["sh", "-c"],
            args=["cowsay hello world | tee /tmp/hello_world.txt"]
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