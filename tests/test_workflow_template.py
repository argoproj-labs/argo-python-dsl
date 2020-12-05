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

from argo.workflows.dsl import WorkflowTemplate
from argo.workflows.dsl.tasks import dependencies, parameter, task
from argo.workflows.dsl.templates import inputs, template

from ._base import TestCase

"""WorkflowTemplate test suite."""


@pytest.fixture  # type: ignore
def api() -> ApiClient:
    """Fake API client."""
    return ApiClient()


@pytest.fixture  # type: ignore
def url() -> str:
    """Fake URL fixture."""


@pytest.fixture  # type: ignore
def wf() -> WorkflowTemplate:
    """Fake WorkflowTemplate."""

    class FakeWorkflowTemplate(WorkflowTemplate):
        name = "test"

    wf = FakeWorkflowTemplate(compile=True)
    return wf


class TestWorkflow(TestCase):
    """Test WorkflowTemplate."""

    _WORKFLOW_FILE = TestCase.DATA / "workflows" / "workflow-template.yaml"

    def test_compile(self) -> None:
        """Test `WorkflowTemplate.compile` method."""

        class TestWorfklowTemplateWithParameters(WorkflowTemplate):
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
        wf_not_compiled = TestWorfklowTemplateWithParameters(compile=False)

        assert wf_not_compiled.model is None

        # test multiple instances
        wf_a = TestWorfklowTemplateWithParameters()
        wf_b = TestWorfklowTemplateWithParameters()

        assert wf_a == wf_b

        assert isinstance(wf_a, V1alpha1WorkflowTemplate)
        assert isinstance(wf_b, V1alpha1WorkflowTemplate)

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` method."""
        wf = WorkflowTemplate.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, WorkflowTemplate)
        assert wf.name == "hello-template"
        assert wf.kind == "WorkflowTemplate"
        assert len(wf.spec.templates) == 1

    def test_from_url(self, url: str) -> None:
        """Test `Workflow.from_url` method."""
        fake_response = type(
            "Response",
            (),
            {"text": self._WORKFLOW_FILE.read_text(), "raise_for_status": lambda: None},
        )
        flexmock(requests).should_receive("get").and_return(fake_response)

        wf = WorkflowTemplate.from_url(url)

        assert isinstance(wf, WorkflowTemplate)
        # assert wf.name == "test"
        assert wf.kind == "WorkflowTemplate"
        assert len(wf.spec.templates) == 1
