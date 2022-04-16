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


class TesterWithInit(Traitful):
    dummy = String()

    def __init__(self, param=1):
        self.param = param


class ChildTester(TesterWithInit):
    new_trait = String()

    def __init__(self, param=2, new_param=2):
        super().__init__(param)
        self.new_param = new_param

    @validate("new_trait")
    def new_trait_validator(self, value):
        if value == "hello":
            raise TraitError("new_trait cannot be hello!")


class GrandChild(ChildTester):
    latest = String()

    @validate("latest")
    def latest_validator(self, value):
        if value == "hello":
            raise TraitError("new_trait cannot be hello!")


class VeryGrandChild(GrandChild):
    @validate("latest")
    def latest_validator(self, value): return value

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


def test_with_init():
    tester = TesterWithInit(param=3, dummy="dummy")
    assert tester.dummy == "dummy"
    assert tester.param == 3


def test_with_child_class():
    tester = ChildTester(
        dummy="dummy",
        new_trait="new_trait",
        param=5,
        new_param=10
    )
    grand_child = GrandChild()
    assert len(tester.traits) == 2
    assert len(grand_child.traits) == 3

    assert tester.dummy == "dummy"
    assert tester.new_trait == "new_trait"
    assert tester.param == 5
    assert tester.new_param == 10
    with pytest.raises(TraitError):
        GrandChild(latest="hello")
    VeryGrandChild(latest="hello")


def test_class_traits():
    assert Tester.traits == frozenset({"dummy"})
    assert len(Tester.validators) == 0
    assert len(GrandChild.validators) == 2
    assert len(VeryGrandChild.validators) == 2
    assert "latest" in GrandChild.validators.keys()
    assert "new_trait" in GrandChild.validators.keys()
    assert len(ChildTester.validators) == 1
    assert ChildTester.traits == frozenset({"dummy", "new_trait"})
    assert GrandChild.traits == frozenset({"dummy", "new_trait", "latest"})
