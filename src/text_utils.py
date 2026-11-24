"""Small, dependency-free utility helpers for working with text.

The first helper, :func:`normalize_whitespace`, cleans up a string by
trimming surrounding whitespace and collapsing any run of whitespace
characters (spaces, tabs, newlines, carriage returns, form feeds, vertical
tabs, and other standard whitespace) into a single space.
"""


def normalize_whitespace(text: str) -> str:
    """Return ``text`` with leading/trailing whitespace removed and runs of
    consecutive whitespace characters collapsed to single spaces.

    All standard whitespace characters (spaces, tabs, newlines, carriage
    returns, form feeds, vertical tabs, and other Unicode whitespace) are
    treated as separators. The relative order and content of the
    non-whitespace characters is preserved exactly.

    Examples:
        >>> normalize_whitespace("  Hello   world!  ")
        'Hello world!'
        >>> normalize_whitespace("a\\tb\\nc")
        'a b c'

    Args:
        text: The string to normalize.

    Returns:
        The cleaned string. Empty strings and strings containing only
        whitespace (e.g. "   \\t\\n") return an empty string.

    Raises:
        TypeError: If ``text`` is not a ``str`` (e.g. ``None``, ``int``,
            ``bytes``, ``list``) and therefore has no meaningful textual
            value to normalize.
    """
    if not isinstance(text, str):
        raise TypeError(
            "normalize_whitespace() expects a str, got "
            f"{type(text).__name__}"
        )

    # str.split() with no separator splits on runs of any standard
    # whitespace and drops leading/trailing whitespace, so joining the
    # resulting words with single spaces performs both the collapse and
    # the trim in one step. Empty or whitespace-only input yields [] and
    # therefore an empty result string.
    return " ".join(text.split())
