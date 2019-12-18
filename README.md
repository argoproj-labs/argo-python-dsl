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

<br>

---

Authors:
- [ Maintainer ] Marek Cermak <macermak@redhat.com>
- Vaclav Pavlin <vpavlin@redhat.com>

@[AICoE](https://github.com/AICoE), Red Hat