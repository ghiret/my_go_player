"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.gosgf import sgf_properties
from dlgo.gosgf.sgf import Node


class MockPresenter:
    def __init__(self, size=19, encoding="UTF-8"):
        self.size = size
        self.encoding = encoding

    def interpret(self, identifier, values):
        return values[0].decode(self.encoding)

    def serialise(self, identifier, value):
        if isinstance(value, (list, tuple)):
            return [sgf_properties.serialise_go_point(point, self.size) for point in value]
        elif value is None:
            return [b""]
        elif isinstance(value, str):
            return [value.encode(self.encoding)]
        else:
            return [str(value).encode(self.encoding)]


@pytest.fixture
def node():
    property_map = {b"C": [b"Test comment"]}
    presenter = MockPresenter()
    return Node(property_map, presenter)


def test_init(node):
    assert isinstance(node, Node)
    assert node.get_size() == 19
    assert node.get_encoding() == "UTF-8"


def test_has_property(node):
    assert node.has_property(b"C")
    assert not node.has_property(b"B")


def test_properties(node):
    assert set(node.properties()) == {b"C"}


def test_get_raw_list(node):
    assert node.get_raw_list(b"C") == [b"Test comment"]
    with pytest.raises(KeyError):
        node.get_raw_list(b"B")


def test_get_raw(node):
    assert node.get_raw(b"C") == b"Test comment"
    with pytest.raises(KeyError):
        node.get_raw(b"B")


def test_get_raw_property_map(node):
    assert node.get_raw_property_map() == {b"C": [b"Test comment"]}


def test_unset(node):
    node.unset(b"C")
    assert not node.has_property(b"C")
    with pytest.raises(KeyError):
        node.unset(b"B")


def test_set_raw_list(node):
    node.set_raw_list(b"B", [b"dd"])
    assert node.get_raw_list(b"B") == [b"dd"]
    with pytest.raises(ValueError):
        node.set_raw_list(b"Invalid!", [b"value"])


def test_set_raw(node):
    node.set_raw(b"B", b"dd")
    assert node.get_raw(b"B") == b"dd"
    with pytest.raises(ValueError):
        node.set_raw(b"Invalid!", b"value")


def test_get(node):
    assert node.get(b"C") == "Test comment"
    with pytest.raises(KeyError):
        node.get(b"B")


def test_set(node):
    node.set(b"B", "dd")
    assert node.get(b"B") == "dd"


def test_get_raw_move(node):
    node.set_raw(b"B", b"dd")
    assert node.get_raw_move() == ("b", b"dd")
    node.unset(b"B")
    node.set_raw(b"W", b"pp")
    assert node.get_raw_move() == ("w", b"pp")
    node.unset(b"W")
    assert node.get_raw_move() == (None, None)


def test_has_setup_stones(node):
    assert not node.has_setup_stones()
    node.set(b"AB", [(1, 1)])
    assert node.has_setup_stones()


def test_set_setup_stones(node):
    node.set_setup_stones([(1, 1)], [(2, 2)], [(3, 3)])
    assert node.get
