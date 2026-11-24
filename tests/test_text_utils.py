"""Unit tests for the normalize_whitespace() function in src/text_utils.py.

These tests use Python's built-in unittest framework only, so the file can
be run directly from the repository root with:

    python -m unittest tests.test_text_utils -v

Import strategy
--------------
The project has no packages, installable distribution, or configured
``sys.path`` hints, and the module lives one directory below the repository
root (``src/text_utils.py``). To keep the imports robust regardless of how
the test is invoked (``python -m unittest``, ``python
tests/test_text_utils.py``, or from inside the ``tests`` directory), we:

1. Locate the repository root relative to the test file itself.
2. Insert it into ``sys.path`` before importing the module by name.
3. Fall back to importing ``text_utils`` (works when ``src/`` is already
   importable, e.g. when tests are run with the repo root on the path via
   an editor or CI configuration).

This mirrors the convention used by the existing test file
``tests/test_agent_smoke.py`` without modifying any existing source files
or adding packaging metadata.
"""

import os
import sys
import unittest

# ---------------------------------------------------------------------------
# Make the repository root importable so that ``src.text_utils`` resolves.
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)  # parent of tests/

if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

try:
    from src.text_utils import normalize_whitespace
except ImportError:  # pragma: no cover - fallback for unusual execution contexts
    from text_utils import normalize_whitespace


class TestNormalizeWhitespaceValidInput(unittest.TestCase):
    """Tests for normalizing well-formed and regular strings."""

    def test_normal_single_spaced_string_unchanged(self):
        """A string with single spaces is returned as-is."""
        self.assertEqual(normalize_whitespace("hello world"), "hello world")

    def test_word_without_whitespace_unchanged(self):
        """A single word containing no whitespace is returned as-is."""
        self.assertEqual(normalize_whitespace("helloworld"), "helloworld")

    def test_leading_and_trailing_spaces_removed(self):
        """Leading and trailing spaces are removed."""
        self.assertEqual(normalize_whitespace("  hello world  "), "hello world")

    def test_repeated_spaces_collapsed_to_single_space(self):
        """A run of multiple spaces becomes one space."""
        self.assertEqual(normalize_whitespace("a  b   c"), "a b c")

    def test_tabs_replaced_with_single_space(self):
        """Tab characters are replaced with single spaces."""
        self.assertEqual(normalize_whitespace("a\tb\tc"), "a b c")

    def test_newlines_replaced_with_single_space(self):
        """Newline characters are replaced with single spaces."""
        self.assertEqual(normalize_whitespace("a\nb\nc"), "a b c")

    def test_carriage:return_replaced_with_single_space(self):
        """Carriage returns are replaced with single spaces."""
        self.assertEqual(normalize_whitespace("a\rb\rc"), "a b c")

    def test_form_feed_and_vertical_tab_replaced(self):
        """Form feeds and vertical tabs are replaced with single spaces."""
        self.assertEqual(normalize_whitespace("a\x0cb\x0bc"), "a b c")

    def test_mixed_whitespace_variety_collapsed(self):
        """Runs mixing spaces, tabs, newlines, and CRs collapse to one space."""
        mixed = "  Hello   world\t!\n\t Python\t\r\n/ws  "
        self.assertEqual(
            normalize_whitespace(mixed), "Hello world! Python/ws"
        )

    def test_multiline_paragraph_collapsed_to_one_line(self):
        """A multi-line paragraph is collapsed to a single space-separated line."""
        paragraph = "The quick brown fox\njumps over\tthe lazy dog.\n"
        self.assertEqual(
            normalize_whitespace(paragraph), "The quick brown fox jumps over the lazy dog."
        )

    def test_non_whitespace_content_and_order_preserved(self):
        """Original order and content of non-whitespace characters is preserved."""
        result = normalize_whitespace("  b  a\t c  ba\n")
        self.assertEqual(result, "b a c ba")
        self.assertEqual(result.index("b"), 0)

    def test_repeated_word_separators_do_not_merge_tokens(self):
        """Separated tokens stay distinct; no characters are dropped."""
        self.assertEqual(normalize_whitespace("x      y     z"), "x y z")


class TestNormalizeWhitespaceEmptyInput(unittest.TestCase):
    """Tests covering empty and whitespace-only strings."""

    def test_empty_string_returns_empty_string(self):
        """An empty string normalizes to an empty string."""
        self.assertEqual(normalize_whitespace(""), "")

    def test_single_space_returns_empty_string(self):
        """A single space normalizes to an empty string."""
        self.assertEqual(normalize_whitespace(" "), "")

    def test_whitespace_only_string_returns_empty_string(self):
        """A string of only whitespace (spaces/tabs/newlines) becomes empty."""
        self.assertEqual(normalize_whitespace("   \t\t \n\r\n \x0c\x0b \t"), "")

    def test_whitespace_only_tabs_and_newlines_returns_empty_string(self):
        """Tabs and newlines alone normalize to an empty string."""
        self.assertEqual(normalize_whitespace("\t\n\t\n"), "")

    def test_result_of_whitespace_only_is_str(self):
        """The empty result for whitespace-only input is still a str."""
        self.assertIsInstance(normalize_whitespace("\t  \n"), str)


class TestNormalizeWhitespaceInvalidInput(unittest.TestCase):
    """Tests verifying TypeError for non-string input values."""

    def test_none_raises_type_error(self):
        """Passing None raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(None)

    def test_integer_raises_type_error(self):
        """Passing an int raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(12345)

    def test_float_raises_type_error(self):
        """Passing a float raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(3.14)

    def test_bytes_raises_type_error(self):
        """Passing bytes raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(b"  hello  world  ")

    def test_bytearray_raises_type_error(self):
        """Passing a bytearray raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(bytearray(b"hello"))

    def test_list_raises_type_error(self):
        """Passing a list raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace(["hello", "world"])

    def test_dict_raises_type_error(self):
        """Passing a dict raises TypeError."""
        with self.assertRaises(TypeError):
            normalize_whitespace({"key": "value"})

    def test_type_error_message_mentions_expected_type(self):
        """The TypeError message names the offending type."""
        with self.assertRaises(TypeError) as ctx:
            normalize_whitespace(None)
        self.assertIn("str", str(ctx.exception))
        self.assertIn("NoneType", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
