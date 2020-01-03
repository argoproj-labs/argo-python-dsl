"""A base class for implementing tests."""

from pathlib import Path


_HERE = Path(__file__).parent


class TestCase:
    """A base class for implementing test cases."""

    DATA = _HERE / "data"
