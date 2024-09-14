import pytest

from dlgo.gosgf import sgf_properties as sgf


class TestSgfProperties:

    @pytest.fixture
    def context(self):
        return sgf._Context(19, "UTF-8")

    def test_interpret_none(self):
        assert sgf.interpret_none(b"") is True
        assert sgf.interpret_none(b"anything") is True

    def test_serialise_none(self):
        assert sgf.serialise_none(True) == b""
        assert sgf.serialise_none(False) == b""

    def test_interpret_number(self):
        assert sgf.interpret_number(b"123") == 123
        assert sgf.interpret_number(b"-456") == -456
        with pytest.raises(ValueError):
            sgf.interpret_number(b"12.34")

    def test_serialise_number(self):
        assert sgf.serialise_number(123) == b"123"
        assert sgf.serialise_number(-456) == b"-456"

    def test_interpret_real(self):
        assert sgf.interpret_real(b"123.45") == 123.45
        assert sgf.interpret_real(b"-456.78") == -456.78
        with pytest.raises(ValueError):
            sgf.interpret_real(b"inf")

    def test_serialise_real(self):
        assert sgf.serialise_real(123.45) == b"123.45"
        assert sgf.serialise_real(-456.78) == b"-456.78"
        assert sgf.serialise_real(0.00001) == b"0"

    def test_interpret_double(self):
        assert sgf.interpret_double(b"1") == 1
        assert sgf.interpret_double(b"2") == 2
        assert sgf.interpret_double(b"3") == 1  # Unknown values treated as 1

    def test_serialise_double(self):
        assert sgf.serialise_double(1) == "1"
        assert sgf.serialise_double(2) == "2"
        assert sgf.serialise_double(3) == "1"  # Unknown values treated as 1

    def test_interpret_colour(self):
        assert sgf.interpret_colour(b"B") == "b"
        assert sgf.interpret_colour(b"W") == "w"
        with pytest.raises(ValueError):
            sgf.interpret_colour(b"R")

    def test_serialise_colour(self):
        assert sgf.serialise_colour("b") == b"B"
        assert sgf.serialise_colour("w") == b"W"
        with pytest.raises(ValueError):
            sgf.serialise_colour("r")

    def test_interpret_simpletext(self, context):
        assert sgf.interpret_simpletext(b"Hello\\] World", context) == b"Hello] World"
        assert sgf.interpret_simpletext(b"Line\nBreak", context) == b"Line Break"

    def test_serialise_simpletext(self, context):
        assert sgf.serialise_simpletext(b"Hello] World", context) == b"Hello\\] World"
        assert sgf.serialise_simpletext(b"Line\nBreak", context) == b"Line\nBreak"  # Newlines are not escaped

    def test_interpret_text(self, context):
        assert sgf.interpret_text(b"Hello\\] World", context) == b"Hello] World"
        assert sgf.interpret_text(b"Line\nBreak", context) == b"Line\nBreak"

    def test_serialise_text(self, context):
        assert sgf.serialise_text(b"Hello] World", context) == b"Hello\\] World"
        assert sgf.serialise_text(b"Line\nBreak", context) == b"Line\nBreak"

    def test_interpret_point(self, context):
        assert sgf.interpret_point(b"aa", context) == (18, 0)
        # Corrected expectation: "sa" represents (0, 18) in SGF coordinates
        assert sgf.interpret_point(b"sa", context) == (18, 18)
        with pytest.raises(ValueError):
            sgf.interpret_point(b"", context)

    def test_serialise_point(self, context):
        assert sgf.serialise_point((18, 0), context) == b"aa"
        assert sgf.serialise_point((18, 18), context) == b"sa"
        with pytest.raises(ValueError):
            sgf.serialise_point(None, context)

    def test_interpret_move(self, context):
        assert sgf.interpret_move(b"aa", context) == (18, 0)
        assert sgf.interpret_move(b"", context) is None
        assert sgf.interpret_move(b"tt", context) is None

    def test_serialise_move(self, context):
        assert sgf.serialise_move((18, 0), context) == b"aa"
        assert sgf.serialise_move(None, context) == b"tt"

    def test_interpret_point_list(self, context):
        assert sgf.interpret_point_list([b"aa", b"bb"], context) == {(18, 0), (17, 1)}
        assert sgf.interpret_point_list([b"aa:cc"], context) == {
            (18, 0),
            (18, 1),
            (18, 2),
            (17, 0),
            (17, 1),
            (17, 2),
            (16, 0),
            (16, 1),
            (16, 2),
        }

    def test_serialise_point_list(self, context):
        assert set(sgf.serialise_point_list([(18, 0), (17, 1)], context)) == {b"aa", b"bb"}

    def test_interpret_AP(self, context):
        # Adjusted expectation: interpret_AP returns bytes, not strings
        assert sgf.interpret_AP(b"CGoban:3", context) == (b"CGoban", b"3")
        assert sgf.interpret_AP(b"TestApp", context) == (b"TestApp", b"")

    def test_serialise_AP(self, context):
        # Adjusted input: use bytes instead of strings
        assert sgf.serialise_AP((b"CGoban", b"3"), context) == b"CGoban:3"
        assert sgf.serialise_AP((b"TestApp", b""), context) == b"TestApp:"

    def test_property_type(self):
        pt = sgf.Property_type(sgf.interpret_number, sgf.serialise_number, False)
        assert pt.interpreter == sgf.interpret_number
        assert pt.serialiser == sgf.serialise_number
        assert pt.uses_list is False

    def test_presenter(self):
        presenter = sgf.Presenter(19, "UTF-8")
        assert presenter.interpret(b"SZ", [b"19"]) == 19
        assert presenter.serialise(b"SZ", 19) == [b"19"]

        # The presenter doesn't raise a ValueError for unknown properties by default
        # Instead, it treats them as text properties
        assert presenter.interpret(b"UNKNOWN", [b"value"]) == b"value"

        # To test ValueError, we need to set the default property type to None
        presenter.set_private_property_type(None)
        with pytest.raises(ValueError):
            presenter.interpret(b"UNKNOWN", [b"value"])
