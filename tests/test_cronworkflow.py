import flexmock
import pytest
import requests

from argo.workflows.client import ApiClient
from argo.workflows.client.models import (
    V1alpha1CronWorkflow,
    V1alpha1Parameter,
    V1alpha1Template,
    V1Container,
)

from argo.workflows.dsl import CronWorkflow
from argo.workflows.dsl.tasks import dependencies, parameter, task
from argo.workflows.dsl.templates import inputs, template

from ._base import TestCase

"""CronWorkflow test suite."""


@pytest.fixture  # type: ignore
def api() -> ApiClient:
    """Fake API client."""
    return ApiClient()


@pytest.fixture  # type: ignore
def url() -> str:
    """Fake URL fixture."""


@pytest.fixture  # type: ignore
def cronwf() -> CronWorkflow:
    """Fake CronWorkflow."""

    class FakeCronWorkflow(CronWorkflow):
        name = "test"
        schedule = "0 0 1 1 *"

    wf = FakeCronWorkflow(compile=True)
    return wf


class TestCronWorkflow(TestCase):
    """Test CronWorkflow."""

    _WORKFLOW_FILE = TestCase.DATA / "workflows" / "cron-workflow.yaml"

    def test_compile(self) -> None:
        """Test `CronWorkflow.compile` method."""

        class TestCronWorfklowWithParameters(CronWorkflow):
            name = "test"
            schedule = "0 0 1 1 *"

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
        wf_not_compiled = TestCronWorfklowWithParameters(compile=False)

        assert wf_not_compiled.model is None

        # test multiple instances
        wf_a = TestCronWorfklowWithParameters()
        wf_b = TestCronWorfklowWithParameters()

        assert wf_a == wf_b

        assert isinstance(wf_a, V1alpha1CronWorkflow)
        assert isinstance(wf_b, V1alpha1CronWorkflow)

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` method."""
        wf = CronWorkflow.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, CronWorkflow)
        assert wf.name == "hello-world"
        assert wf.kind == "CronWorkflow"
        assert len(wf.spec.workflow_spec.templates) == 1

    def test_from_url(self, url: str) -> None:
        """Test `Workflow.from_url` method."""
        fake_response = type(
            "Response",
            (),
            {"text": self._WORKFLOW_FILE.read_text(), "raise_for_status": lambda: None},
        )
        flexmock(requests).should_receive("get").and_return(fake_response)

        wf = CronWorkflow.from_url(url)

        assert isinstance(wf, CronWorkflow)
        # assert wf.name == "test"
        assert wf.kind == "CronWorkflow"
        assert len(wf.spec.workflow_spec.templates) == 1
