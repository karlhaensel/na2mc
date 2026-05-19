"""Tests for Mastermind code class."""

import pytest

from scripts.code import MasterMindCode
from scripts.colour import MasterMindColour
from scripts.const import CODE_LENGTH


@pytest.mark.parametrize(
    "colours, should_raise",
    [
        (tuple(MasterMindColour.RED), True),
        ((MasterMindColour.RED, MasterMindColour.GREEN), True),
        (
            (
                MasterMindColour.RED,
                MasterMindColour.GREEN,
                MasterMindColour.RED,
                MasterMindColour.GREEN,
                MasterMindColour.RED,
            ),
            True,
        ),
        (
            (
                MasterMindColour.RED,
                MasterMindColour.GREEN,
                MasterMindColour.RED,
                MasterMindColour.GREEN,
            ),
            False,
        ),
    ],
)
def test_code_init(colours: tuple[MasterMindColour, ...], should_raise: bool) -> None:
    """Test initialisation of Mastermind code."""
    if should_raise:
        with pytest.raises(
            ValueError,
            match=f"Mastermind code must have exactly {CODE_LENGTH} colours.",
        ):
            MasterMindCode(colours)
    else:
        code = MasterMindCode(colours)
        assert code.colours == colours


def test_code_randomise() -> None:
    """Test random generation of Mastermind code."""
    random_code = MasterMindCode.randomise()
    assert isinstance(random_code, MasterMindCode)
    assert len(random_code.colours) == CODE_LENGTH


@pytest.mark.parametrize(
    "guess_code, should_raise",
    [
        ("", True),
        ("r", True),
        ("rrg", True),
        ("rrgg", False),
        ("gggg", False),
        ("rgby", False),
        ("rrggr", True),
        ("ruug", True),
    ],
)
def test_from_guess(guess_code: str, should_raise: bool) -> None:
    """Test Mastermind code generation from guess."""
    if should_raise:
        with pytest.raises(
            ValueError, match="must contain exactly four letters out of"
        ):
            MasterMindCode.from_guess(guess_code)
    else:
        code = MasterMindCode.from_guess(guess_code)
        assert isinstance(code, MasterMindCode)
        assert len(code.colours) == CODE_LENGTH
        assert code.colours == tuple(
            MasterMindColour.from_first_letter(letter) for letter in guess_code
        )


@pytest.mark.parametrize(
    "first_code, second_code, is_equal",
    [
        ("rrrr", "gggg", False),
        ("rrrr", "rrrr", True),
        ("royg", "bipr", False),
        ("royg", "royg", True),
        ("royg", "royo", False),
        ("royg", "gyor", False),
    ],
)
def test_equality(first_code: str, second_code: str, is_equal: bool) -> None:
    """Test Mastermind code equality check."""
    first = MasterMindCode.from_guess(first_code)
    second = MasterMindCode.from_guess(second_code)
    assert (first == second) == is_equal


@pytest.mark.parametrize(
    "code_str, string_rep",
    [
        ("rrrr", "red, red, red, red"),
        ("royg", "red, orange, yellow, green"),
        ("gbip", "green, blue, indigo, purple"),
    ],
)
def test_string_representation(code_str, string_rep: str) -> None:
    """Test Mastermind code string representation."""
    code_str = MasterMindCode.from_guess(code_str)
    assert str(code_str) == string_rep


@pytest.mark.parametrize(
    "actual_code, guess_code, exacts, non_exacts",
    [
        ("rrrr", "rrrr", 4, 0),
        ("rrrr", "gggg", 0, 0),
        ("rgbp", "pbgr", 0, 4),
        ("rgrg", "rggr", 2, 2),
        ("rrrg", "rrrr", 3, 0),
        ("rgrg", "gggg", 2, 0),
        ("rgbi", "ypoi", 1, 0),
    ],
)
def test_diff_to_other(
    actual_code: str, guess_code, exacts: int, non_exacts: int
) -> None:
    """Test Mastermind code difference message between guess and actual code."""
    actual = MasterMindCode.from_guess(actual_code)
    guess = MasterMindCode.from_guess(guess_code)
    diff_message = guess.diff_to_other(actual)
    assert f"exact matches: {exacts}" in diff_message
    assert f"colour matches but wrong place: {non_exacts}" in diff_message
