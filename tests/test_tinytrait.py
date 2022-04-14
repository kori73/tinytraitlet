import pytest

from tinytraitlet import Traitful, String, validate
from tinytraitlet.tinytraitlet import TraitError


class Tester(Traitful):
    dummy = String()


class TesterValid(Traitful):
    dummy = String()

    @validate("dummy")
    def my_dummy_validator(self, value):
        if value == "hello":
            raise TraitError("dummy cannot be hello!")


def test_model():
    tester = Tester()
    assert tester.dummy == ""
    tester = Tester(dummy="dummy")
    assert tester.dummy == "dummy"
    with pytest.raises(TraitError):
        tester.dummy = 1
    with pytest.raises(TraitError):
        Tester(dummy=1)


def test_custom_validator():
    tester = TesterValid(dummy="foo")
    with pytest.raises(TraitError):
        tester.dummy = "hello"
    with pytest.raises(TraitError):
        TesterValid(dummy="hello")
