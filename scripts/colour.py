"""Mastermind Colour Enum."""

from enum import StrEnum


class MasterMindColour(StrEnum):
    """Enum representation of Mastermind colours."""

    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    INDIGO = "indigo"
    PURPLE = "purple"

    @classmethod
    def get_letter_mapping(cls) -> dict[str, "MasterMindColour"]:
        return {member.value[0].lower(): member for member in cls}

    @classmethod
    def get_first_letters_for_regex(cls) -> str:
        return "".join(cls.get_letter_mapping().keys())

    @classmethod
    def from_first_letter(cls, letter: str) -> "MasterMindColour | None":
        """Get MasterMindColour from first letter."""
        return cls.get_letter_mapping().get(letter.lower())
