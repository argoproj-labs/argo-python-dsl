import flexmock
import pytest
import requests

from argo.workflows.sdk import Workflow

from ._base import TestCase

"""Workflow test suite."""


@pytest.fixture  # type: ignore
def url() -> str:
    """Fake URL fixture."""


class TestWorkflow(TestCase):
    """Test Workflow."""

    _WORKFLOW_FILE = TestCase.DATA / "workflows" / "hello-world.yaml"

    def test_from_file(self) -> None:
        """Test `Workflow.from_file` methods."""
        wf = Workflow.from_file(self._WORKFLOW_FILE)

        assert isinstance(wf, Workflow)
        assert wf.name == "test"
        assert wf.kind == "Workflow"
        assert len(wf.spec.templates) == 1

    def test_from_url(self, url: str) -> None:
        """Test `Workflow.from_url` methods."""
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
