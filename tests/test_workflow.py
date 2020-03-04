import flexmock
import pytest
import requests

from argo.workflows.client import V1alpha1Api
from argo.workflows.client.models import V1alpha1Arguments, V1alpha1Parameter

from argo.workflows.dsl import Workflow

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

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` method."""
        wf = Workflow.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, Workflow)
        assert wf.name == "test"
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
        assert wf.name == "test"
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
        workflow_name: str = wf.submit(
            client=api, namespace="test", parameters={"param": "test"}
        )

        assert isinstance(workflow_name, str)
        assert workflow_name == "test"
