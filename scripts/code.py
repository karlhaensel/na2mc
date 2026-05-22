"""Mastermind code class."""

import random
import re

from scripts.colour import MasterMindColour
from scripts.const import CODE_LENGTH


class MasterMindCode:
    """Class representing Mastermind code of colours (actual code or guess)."""

    def __init__(self, colours: tuple[MasterMindColour, ...]) -> None:
        """Initialise MasterMindCode."""
        if len(colours) != CODE_LENGTH:
            raise ValueError(
                f"Mastermind code must have exactly {CODE_LENGTH} colours."
            )
        self.colours = colours

    @classmethod
    def randomise(cls) -> "MasterMindCode":
        """Generate random MasterMindCode."""
        return cls(
            tuple(random.choice(list(MasterMindColour)) for _ in range(CODE_LENGTH))
        )

    @classmethod
    def from_guess(cls, guess_code: str) -> "MasterMindCode":
        """Generate MasterMindCode from guess with beginning letters of colours."""
        pattern = re.compile(
            f"^[{MasterMindColour.get_first_letters_for_regex()}]{{{CODE_LENGTH}}}$"
        )
        if not re.search(pattern, guess_code):
            raise ValueError(
                "Guess must contain exactly four letters out of "
                f"{MasterMindColour.get_first_letters_for_regex()} "
                "to represent the colours."
            )
        colours = []
        for letter in guess_code:
            colour = MasterMindColour.from_first_letter(letter)
            if colour is None:
                raise ValueError(f"Invalid colour letter: {letter}")
            colours.append(colour)
        return cls(tuple(colours))

    def __eq__(self, other):
        """Determine, whether two MasterMindCodes are equal."""
        if not isinstance(other, MasterMindCode):
            raise ValueError(
                "You can only compare a MasterMindCode with another MasterMindCode!"
            )
        return self.colours == other.colours

    def __str__(self):
        """Return string representation of MasterMindCode colours."""
        return ", ".join(self.colours)

    def diff_to_other(self, other: "MasterMindCode") -> str:
        """Get result string for exact and non-exact colours matches."""
        exact_matches = [
            self.colours[i] == other.colours[i] for i in range(CODE_LENGTH)
        ]
        colour_matches: int = 0
        for i, exact in enumerate(exact_matches):
            if not exact:
                other_matches = [
                    j
                    for j, colour in enumerate(other.colours)
                    if (colour == self.colours[i] and not exact_matches[j])
                ]
                if len(other_matches) > 0:
                    colour_matches += 1
        return (
            f"exact matches: {sum(exact_matches)}, "
            f"colour matches but wrong place: {colour_matches}"
        )
