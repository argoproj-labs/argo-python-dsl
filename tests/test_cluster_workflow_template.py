import flexmock
import pytest
import requests

from argo.workflows.client import ApiClient
from argo.workflows.client.models import (
    V1alpha1Parameter,
    V1alpha1Template,
    V1alpha1WorkflowTemplate,
    V1Container,
)

from argo.workflows.dsl import ClusterWorkflowTemplate
from argo.workflows.dsl.tasks import dependencies, parameter, task
from argo.workflows.dsl.templates import inputs, template

from ._base import TestCase

"""ClusterWorkflowTemplate test suite."""


@pytest.fixture  # type: ignore
def api() -> ApiClient:
    """Fake API client."""
    return ApiClient()


@pytest.fixture  # type: ignore
def url() -> str:
    """Fake URL fixture."""


@pytest.fixture  # type: ignore
def wf() -> ClusterWorkflowTemplate:
    """Fake ClusterWorkflowTemplate."""

    class FakeClusterWorkflowTemplate(ClusterWorkflowTemplate):
        name = "test"

    wf = FakeClusterWorkflowTemplate(compile=True)
    return wf


class TestWorkflow(TestCase):
    """Test ClusterWorkflowTemplate."""

    _WORKFLOW_FILE = TestCase.DATA / "workflows" / "cluster-workflow-template.yaml"

    def test_compile(self) -> None:
        """Test `ClusterWorkflowTemplate.compile` method."""

        class TestClusterWorfklowTemplateWithParameters(ClusterWorkflowTemplate):
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
        wf_not_compiled = TestClusterWorfklowTemplateWithParameters(compile=False)

        assert wf_not_compiled.model is None

        # test multiple instances
        wf_a = TestClusterWorfklowTemplateWithParameters()
        wf_b = TestClusterWorfklowTemplateWithParameters()

        # assert wf_a.name == "hello-cluster-template"
        assert wf_b.kind == "ClusterWorkflowTemplate"

        assert wf_a == wf_b

        assert isinstance(wf_a, V1alpha1WorkflowTemplate)
        assert isinstance(wf_b, V1alpha1WorkflowTemplate)

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` method."""
        wf = ClusterWorkflowTemplate.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, ClusterWorkflowTemplate)
        assert wf.name == "hello-cluster-template"
        assert wf.kind == "ClusterWorkflowTemplate"
        assert len(wf.spec.templates) == 1

    def test_from_url(self, url: str) -> None:
        """Test `Workflow.from_url` method."""
        fake_response = type(
            "Response",
            (),
            {"text": self._WORKFLOW_FILE.read_text(), "raise_for_status": lambda: None},
        )
        flexmock(requests).should_receive("get").and_return(fake_response)

        wf = ClusterWorkflowTemplate.from_url(url)

        assert isinstance(wf, ClusterWorkflowTemplate)
        # assert wf.name == "test"
        assert wf.kind == "ClusterWorkflowTemplate"
        assert len(wf.spec.templates) == 1
