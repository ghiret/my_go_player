import pytest

from dlgo.gosgf.sgf_grammar import (
    Coarse_game_tree,
    block_format,
    compose,
    escape_text,
    is_valid_property_identifier,
    is_valid_property_value,
    parse_compose,
    parse_sgf_collection,
    parse_sgf_game,
    serialise_game_tree,
    simpletext_value,
    text_value,
    tokenise,
)


def test_is_valid_property_identifier():
    assert is_valid_property_identifier(b"AB")
    assert is_valid_property_identifier(b"C")
    assert is_valid_property_identifier(b"ABCDEFGH")
    assert not is_valid_property_identifier(b"ab")
    assert not is_valid_property_identifier(b"A1")
    assert not is_valid_property_identifier(b"ABCDEFGHI")
    assert not is_valid_property_identifier(b"")


def test_is_valid_property_value():
    assert is_valid_property_value(b"Hello, world!")
    assert is_valid_property_value(b"Contains (parentheses)")
    assert is_valid_property_value(b"Escaped \\] bracket")
    assert is_valid_property_value(b"Escaped \\\\ backslash")
    assert is_valid_property_value(b"Multi\nline\nvalue")
    assert is_valid_property_value(b"")  # Empty string is valid
    assert is_valid_property_value(b"Escaped \\[ left bracket")
    assert is_valid_property_value(b"Multiple \\] \\[ \\] \\[ brackets")

    assert not is_valid_property_value(b"Unescaped [bracket]")
    assert not is_valid_property_value(b"Unescaped ] bracket")
    assert not is_valid_property_value(b"Ends with backslash \\")
    assert not is_valid_property_value(b"Unescaped ] after some \\ escapes")


def test_tokenise():
    sgf_data = b"(;A[B];C[D])"
    tokens, end_position = tokenise(sgf_data)
    expected_tokens = [("D", b"("), ("D", b";"), ("I", b"A"), ("V", b"B"), ("D", b";"), ("I", b"C"), ("V", b"D"), ("D", b")")]
    assert tokens == expected_tokens
    assert end_position == len(sgf_data)


def test_coarse_game_tree():
    tree = Coarse_game_tree()
    tree.sequence = [{"A": [b"B"]}, {"C": [b"D"]}]
    tree.children = [Coarse_game_tree(), Coarse_game_tree()]
    assert len(tree.sequence) == 2
    assert len(tree.children) == 2


def test_parse_sgf_game():
    sgf_data = b"(;A[B];C[D](;E[F])(;G[H]))"
    game_tree = parse_sgf_game(sgf_data)
    assert isinstance(game_tree, Coarse_game_tree)
    assert len(game_tree.sequence) == 2
    assert len(game_tree.children) == 2


def test_parse_sgf_collection():
    sgf_collection = b"(;A[B])(;C[D])"
    trees = parse_sgf_collection(sgf_collection)
    assert len(trees) == 2
    assert all(isinstance(tree, Coarse_game_tree) for tree in trees)


def test_block_format():
    pieces = [b"Hello", b"world", b"This", b"is", b"a", b"test"]
    result = block_format(pieces, width=10)
    assert result == b"Helloworld\nThisisa\ntest"

    # Test with different width
    result_wide = block_format(pieces, width=25)
    assert result_wide == b"HelloworldThisisatest"

    # Test with pieces that exactly fit the width
    exact_pieces = [b"abc", b"def", b"ghi"]
    result_exact = block_format(exact_pieces, width=9)
    assert result_exact == b"abcdefghi"

    # Test with empty list
    assert block_format([]) == b""

    # Test with a single piece longer than width
    long_piece = [b"abcdefghijklmnop"]
    result_long = block_format(long_piece, width=10)
    assert result_long == b"\nabcdefghijklmnop"

    # Test with multiple lines and last line shorter than width
    multi_pieces = [b"abcdef", b"ghijkl", b"mnopqr", b"stu"]
    result_multi = block_format(multi_pieces, width=12)
    assert result_multi == b"abcdefghijkl\nmnopqrstu"


def test_serialise_game_tree():
    tree = Coarse_game_tree()
    tree.sequence = [{b"A": [b"B"]}, {b"C": [b"D"]}]
    result = serialise_game_tree(tree)
    assert result.startswith(b"(;A[B];C[D]")
    assert result.endswith(b")\n")


def test_parse_compose():
    assert parse_compose(b"Hello:World") == (b"Hello", b"World")
    assert parse_compose(b"No colon") == (b"No colon", None)
    assert parse_compose(b"Escaped\\:colon:after") == (b"Escaped\\:colon", b"after")


def test_compose():
    assert compose(b"Hello", b"World") == b"Hello:World"
    assert compose(b"With:colon", b"After") == b"With\\:colon:After"


def test_simpletext_value():
    # Test backslash followed by newline
    assert simpletext_value(b"hello\\\nworld") == b"helloworld"

    # Test other linebreaks
    assert simpletext_value(b"hello\nworld") == b"hello world"
    assert simpletext_value(b"hello\r\nworld") == b"hello world"

    # Test other whitespace
    assert simpletext_value(b"hello\tworld") == b"hello world"
    assert simpletext_value(b"hello\fworld") == b"hello world"
    assert simpletext_value(b"hello\vworld") == b"hello world"

    # Test backslash behavior
    assert simpletext_value(b"hello\\world") == b"helloworld"  # Single backslash is removed
    assert simpletext_value(b"hello\\\\world") == b"hello\\world"  # Double backslash becomes single
    assert simpletext_value(b"hello\\\\\\world") == b"hello\\world"  # Triple backslash becomes single

    # Test complex case
    assert simpletext_value(b"a\\\\b\\c\\\nd\n\\e") == b"a\\bcd e"

    # Test escaped special characters
    assert simpletext_value(b"hello\\]world") == b"hello]world"
    assert simpletext_value(b"hello\\:world") == b"hello:world"

    # Test multiple consecutive whitespace characters
    assert simpletext_value(b"hello   world") == b"hello   world"

    # Test backslash at the end of the string
    assert simpletext_value(b"hello\\") == b"hello"

    # Test empty string
    assert simpletext_value(b"") == b""


def test_text_value():
    # Test newline normalization
    assert text_value(b"hello\nworld") == b"hello\nworld"
    assert text_value(b"hello\r\nworld") == b"hello\nworld"
    assert text_value(b"hello\rworld") == b"hello\nworld"

    # Test other whitespace
    assert text_value(b"hello\tworld") == b"hello world"
    assert text_value(b"hello\fworld") == b"hello world"
    assert text_value(b"hello\vworld") == b"hello world"

    # Test backslash followed by newline
    assert text_value(b"hello\\\nworld") == b"helloworld"
    assert text_value(b"hello\\\r\nworld") == b"helloworld"

    # Test backslash behavior
    assert text_value(b"hello\\world") == b"helloworld"  # Single backslash is removed
    assert text_value(b"hello\\\\world") == b"hello\\world"  # Double backslash becomes single
    assert text_value(b"hello\\\\\\world") == b"hello\\world"  # Triple backslash becomes single

    # Test escaped special characters
    assert text_value(b"hello\\]world") == b"hello]world"
    assert text_value(b"hello\\:world") == b"hello:world"

    # Test multiple consecutive whitespace characters
    assert text_value(b"hello   world") == b"hello   world"

    # Test backslash at the end of the string
    assert text_value(b"hello\\") == b"hello"

    # Test empty string
    assert text_value(b"") == b""

    # Test complex case
    assert text_value(b"a\\\\b\\c\\\nd\n\\e") == b"a\\bcd\ne"

    # Test preservation of newlines
    assert text_value(b"hello\nworld\n") == b"hello\nworld\n"

    # Test backslash followed by non-newline whitespace
    assert text_value(b"hello\\ world") == b"hello world"

    # Test multiple newlines
    assert text_value(b"hello\n\nworld") == b"hello\n\nworld"


def test_escape_text():
    # Test escaping backslashes
    assert escape_text(b"hello\\world") == b"hello\\\\world"

    # Test escaping right square brackets
    assert escape_text(b"hello]world") == b"hello\\]world"

    # Test escaping both backslashes and right square brackets
    assert escape_text(b"hello\\]world") == b"hello\\\\\\]world"

    # Test with left square bracket (should not be escaped)
    assert escape_text(b"hello[world") == b"hello[world"

    # Test with newlines (should not be escaped)
    assert escape_text(b"hello\nworld") == b"hello\nworld"

    # Test with other whitespace (should not be escaped)
    assert escape_text(b"hello\tworld") == b"hello\tworld"

    # Test empty string
    assert escape_text(b"") == b""

    # Test string with only characters to be escaped
    assert escape_text(b"\\]") == b"\\\\\\]"

    # Test with multiple characters to be escaped
    assert escape_text(b"\\]\\]") == b"\\\\\\]\\\\\\]"

    # Test that the result passes is_valid_property_value()
    assert is_valid_property_value(escape_text(b"hello\\]world"))

    # Test the property mentioned in the docstring
    original = b"hello\nworld\ttab"
    escaped = escape_text(original)
    assert text_value(escaped) == b"hello\nworld tab"
