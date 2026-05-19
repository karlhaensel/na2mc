"""Tests for MastermindColour enum."""

from scripts.colour import MasterMindColour

MANUAL_MAPPING = {
    "r": MasterMindColour.RED,
    "o": MasterMindColour.ORANGE,
    "y": MasterMindColour.YELLOW,
    "g": MasterMindColour.GREEN,
    "b": MasterMindColour.BLUE,
    "i": MasterMindColour.INDIGO,
    "p": MasterMindColour.PURPLE,
}


def test_mapping() -> None:
    """Test dynamical mapping with current setup."""
    assert MANUAL_MAPPING == MasterMindColour.get_letter_mapping()


def test_first_letters_for_regex() -> None:
    """Test dynamical generation of first letters for regex."""
    assert (
        "".join(MANUAL_MAPPING.keys()) == MasterMindColour.get_first_letters_for_regex()
    )


def test_colour_from_first_letter() -> None:
    """Test generation colour from first letter."""
    for letter in MANUAL_MAPPING.keys():
        assert MasterMindColour.from_first_letter(letter) == MANUAL_MAPPING[letter]
    assert MasterMindColour.from_first_letter("x") is None
