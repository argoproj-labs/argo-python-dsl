# argo-python-dsl &nbsp; [![Release](https://img.shields.io/github/v/tag/argoproj-labs/argo-python-dsl.svg?sort=semver&label=Release)](https://github.com/argoproj-labs/argo-python-dsl/releases/latest)

[![License](https://img.shields.io/github/license/argoproj-labs/argo-python-dsl)](https://github.com/argoproj-labs/argo-python-dsl/blob/master/LICENSE) &nbsp; [![CI](https://github.com/argoproj-labs/argo-python-dsl/workflows/CI/badge.svg)](https://github.com/argoproj-labs/argo-python-dsl/actions) &nbsp;

### Python DSL for [Argo Workflows](https://github.com/argoproj/argo)

<div style="text-align: justify">

If you're new to Argo, we recommend checking out the examples in pure YAML. The language is descriptive and the Argo [examples](https://github.com/argoproj/argo/tree/master/examples) provide an exhaustive explanation.

For a more experienced audience, this DSL grants you the ability to programatically define Argo Workflows in Python which is then translated to the Argo YAML specification.

The DSL makes use of the Argo models defined in the [Argo Python client](https://github.com/argoproj-labs/argo-client-python) repository. Combining the two approaches we are given the whole low-level control over Argo Workflows.

</div>

## Getting Started

#### Hello World

<div style="text-align: justify">

This example demonstrates the simplest functionality. Defining a `Workflow` by subclassing the `Workflow` class and a single template with the `@template` decorator.

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
from argo.workflows.dsl import Workflow
from argo.workflows.dsl import template

from argo.workflows.dsl.templates import V1Container


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
from argo.workflows.dsl import Workflow

from argo.workflows.dsl.tasks import *
from argo.workflows.dsl.templates import *


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

```

</p></td>
</tr>
</table>

#### Artifacts

<div style="text-align: justify">

`Artifacts` can be passed similarly to `parameters` in three forms: `arguments`, `inputs` and `outputs`, where `arguments` is the default one (simply `@artifact` or `@parameter`).

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
from argo.workflows.dsl import Workflow

from argo.workflows.dsl.tasks import *
from argo.workflows.dsl.templates import *

class ArtifactPassing(Workflow):

    @task
    def generate_artifact(self) -> V1alpha1Template:
        return self.whalesay()

    @task
    @artifact(
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

## Going further: `closure` and `scope`

<div style="text-align: justify">

This is where it gets quite interesting. So far, we've only scratched the benefits that the Python implementation provides.

What if we want to use native Python code and execute it as a step in the Workflow. What are our options?

**Option A)** is to reuse the existing mindset, dump the code in a string, pass it as the source to the `V1ScriptTemplate` model and wrap it with the `template` decorator.
This is illustrated in the following code block:

</div>

```python
import textwrap

class ScriptsPython(Workflow):

    ...

    @template
    def gen_random_int(self) -> V1alpha1ScriptTemplate:
        source = textwrap.dedent("""\
          import random
          i = random.randint(1, 100)
          print(i)
        """)

        template = V1alpha1ScriptTemplate(
            image="python:alpine3.6",
            name="gen-random-int",
            command=["python"],
            source=source
        )

        return template
```

Which results in:

```yaml
api_version: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generate_name: scripts-python-
  name: scripts-python
spec:
  entrypoint: main

  ...

  templates:
  - name: gen-random-int
    script:
      command:
      - python
      image: python:alpine3.6
      name: gen-random-int
      source: 'import random\ni = random.randint(1, 100)\nprint(i)\n'
```

<div style="text-align: justify">

Not bad, but also not living up to the full potential. Since we're already writing Python, why would we wrap the code in a string? This is where we introduce `closure`s.

#### `closure`s

The logic of `closure`s is quite simple. Just wrap the function you want to execute in a container in the `@closure` decorator. The `closure` then takes care of the rest and returns a `template` (just as the `@template` decorator).

The only thing we need to take care of is to provide it an image which has the necessary Python dependencies installed and is present in the cluster.

> There is a plan to eliminate even this step in the future, but currently it is inavoidable.

Following the previous example:

</div>

```python
class ScriptsPython(Workflow):

    ...

    @closure(
      image="python:alpine3.6"
    )
    def gen_random_int() -> V1alpha1ScriptTemplate:
          import random

          i = random.randint(1, 100)
          print(i)
```

<div style="text-align: justify">

The closure implements the `V1alpha1ScriptTemplate`, which means that you can pass in things like `resources`, `env`, etc...

Also, make sure that you `import` whatever library you are using, the context is not preserved --- `closure` behaves as a staticmethod and is *sandboxed* from the module scope.

#### `scope`

Now, what if we had a function (or a whole script) which is quite big. Wrapping it in a single Python function is not very Pythonic and it gets tedious. This is where we can make use of `scope`s.

Say that we, for example, wanted to initialize logging before running our `gen_random_int` function.

</div>

```python
    ...

    @closure(
      scope="main",
      image="python:alpine3.6"
    )
    def gen_random_int(main) -> V1alpha1ScriptTemplate:
          import random

          main.init_logging()

          i = random.randint(1, 100)
          print(i)

    @scope(name="main")
    def init_logging(level="DEBUG"):
        import logging

        logging_level = getattr(logging, level, "INFO")
        logging.getLogger("__main__").setLevel(logging_level)
```

Notice the 3 changes that we've made:</div>

```python
    @closure(
      scope="main",  # <--- provide the closure a scope
      image="python:alpine3.6"
    )
    def gen_random_int(main):  # <--- use the scope name
```

```python
    @scope(name="main")  # <--- add function to a scope
    def init_logging(level="DEBUG"):
```

<div style="text-align: justify">

Each function in the given scope is then namespaced by the scope name and injected to the closure.

I.e. the resulting YAML looks like this:</div>

```yaml
...
spec:
  ...
  templates:
    - name: gen-random-int
      script:
        command:
        - python
        image: python:alpine3.6
        name: gen-random-int
        source: |-
          import logging
          import random

          class main:
            """Scoped objects injected from scope 'main'."""

            @staticmethod
            def init_logging(level="DEBUG"):
              logging_level = getattr(logging, level, "INFO")
              logging.getLogger("__main__").setLevel(logging_level)


          main.init_logging()

          i = random.randint(1, 100)
          print(i)
```

## Submitting with dsl

Assume we are running `kubectl -n argo port-forward deployment/argo-server 2746:2746`

#### Workflow
```python
from argo.workflows.client import (
    ApiClient,
    Configuration,
    WorkflowServiceApi,
    V1alpha1WorkflowCreateRequest)

from argo.workflows.dsl import Workflow
from argo.workflows.dsl.tasks import *
from argo.workflows.dsl.templates import *


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
    config = Configuration(host="http://localhost:2746")
    client = ApiClient(configuration=config)
    wf.submit(client, 'argo')
```

#### CronWorkflow

```python
from argo.workflows.client import Configuration, ApiClient
from argo.workflows.dsl import template
from argo.workflows.dsl import CronWorkflow
from argo.workflows.dsl.templates import V1Container


class HelloCron(CronWorkflow):

    entrypoint = "whalesay"
    schedule = "0 0 1 1 *"

    @template
    def whalesay(self) -> V1Container:
        container = V1Container(
            image="docker/whalesay:latest",
            name="whalesay",
            command=["cowsay"],
            args=["hello world"],
        )
        return container


if __name__ == "__main__":
    wf = HelloCron()
    print(wf)
    config = Configuration(host="http://localhost:2746")
    client = ApiClient(configuration=config)
    wf.submit(client, "argo")
```

The compilation also takes all imports to the front and remove duplicates for convenience and more natural look so that you don't feel like poking your eyes when you look at the resulting YAML.

<br>

For more examples see the [examples](https://github.com/argoproj-labs/argo-python-dsl/tree/master/examples) folder.

<br>

---

Authors:
- [ Maintainer ] Yudi Xue <binarycrayon@gmail.com>
- [ Past Maintainer ] Marek Cermak <macermak@redhat.com>, <prace.mcermak@gmail.com>
