import flexmock
import pytest
import requests

from argo.workflows.client import V1alpha1Api
from argo.workflows.client.models import (
    V1alpha1Arguments,
    V1alpha1Parameter,
    V1alpha1Template,
    V1alpha1Workflow,
    V1Container
)

from argo.workflows.dsl import Workflow
from argo.workflows.dsl.tasks import (
    dependencies,
    parameter,
    task
)
from argo.workflows.dsl.templates import inputs, template

from ._base import TestCase

"""Workflow test suite."""


@pytest.fixture  # type: ignore
def api() -> V1alpha1Api:
    """Fake API client."""
    return V1alpha1Api()


@pytest.fixture  # type: ignore
def url() -> str:
    """Fake URL fixture."""


@pytest.fixture  # type: ignore
def wf() -> Workflow:
    """Fake Workflow."""

    class FakeWorkflow(Workflow):
        name = "test"

    wf = FakeWorkflow(compile=True)
    return wf


class TestWorkflow(TestCase):
    """Test Workflow."""

    _WORKFLOW_FILE = TestCase.DATA / "workflows" / "hello-world.yaml"

    def test_compile(self) -> None:
        """Test `Workflow.compile` method."""
        class TestWorfklowWithParameters(Workflow):
            name = "test"

            @task
            @parameter(name="message", value="A")
            def A(self, message: V1alpha1Parameter) -> V1alpha1Template:
                return self.echo(message=message)

            @task
            @parameter(name="message", value="B")
            @dependencies(["A"])
            def B(self, message: V1alpha1Parameter) -> V1alpha1Template:
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

        # test compile=False
        wf_not_compiled = TestWorfklowWithParameters(compile=False)

        assert wf_not_compiled.model is None

        # test multiple instances
        wf_a = TestWorfklowWithParameters()
        wf_b = TestWorfklowWithParameters()

        assert wf_a == wf_b

        assert isinstance(wf_a, V1alpha1Workflow)
        assert isinstance(wf_b, V1alpha1Workflow)

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` method."""
        wf = Workflow.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, Workflow)
        assert wf.name == "hello-world"
        assert wf.kind == "Workflow"
        assert len(wf.spec.templates) == 1

    def test_from_url(self, url: str) -> None:
        """Test `Workflow.from_url` method."""
        fake_response = type(
            "Response",
            (),
            {"text": self._WORKFLOW_FILE.read_text(), "raise_for_status": lambda: None},
        )
        flexmock(requests).should_receive("get").and_return(fake_response)

        wf = Workflow.from_url(url)

        assert isinstance(wf, Workflow)
        # assert wf.name == "test"
        assert wf.kind == "Workflow"
        assert len(wf.spec.templates) == 1

    def test_submit(self, api: V1alpha1Api, wf: Workflow) -> None:
        """Test `Workflow.submit` method."""
        fake_workflow_name = "test"
        flexmock(V1alpha1Api).should_receive("create_namespaced_workflow").and_return(
            fake_workflow_name
        )

        # submit w/o parameters
        workflow_name: str = wf.submit(client=V1alpha1Api(), namespace="test")

        assert isinstance(workflow_name, str)
        assert workflow_name == "test"

        # submit w/ parameters
        with pytest.raises(AttributeError) as exc:
            # Expected ValueError due to undefined parameter
            workflow_name: str = wf.submit(
                client=api, namespace="test", parameters={"param": "test"}
            )

        wf.spec.arguments = V1alpha1Arguments(
            parameters=[V1alpha1Parameter(name="param")]
        )
        workflow_result: str = wf.submit(
            client=api, namespace="test", parameters={"param": "test"}
        )
        # assert isinstance(workflow_result, V1alpha1Workflow)
        # assert isinstance(workflow_result.metadata.name, str)
        # assert len(workflow_result.spec.arguments.parameters) == 1
        # assert workflow_result.spec.arguments.parameters[0].name == 'param'
        # assert workflow_result.spec.arguments.parameters[0].value == 'test'
        # assert workflow_result.metadata.name == "test"
