"""Main script for playing Mastermind."""

import random
import re
from enum import StrEnum


CODE_LENGTH = 4
MAX_GUESSES = 7


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
            return ValueError(
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


if __name__ == "__main__":
    """Run main game logic."""
    while True:
        solved: bool = False
        tries: int = 0
        code: MasterMindCode = MasterMindCode.randomise()
        print("--- MASTERMIND ---")
        print(f"Guess the code of {CODE_LENGTH} colours! Enter letters to guess:")
        while not solved and tries < MAX_GUESSES:
            print(
                "Choose: [r]ed, [o]range, [y]ellow, [g]reen, [b]lue, [i]ndigo, [p]urple"
            )
            raw_guess = input(f"Your guess {tries+1}:")
            try:
                guess = MasterMindCode.from_guess(raw_guess)
            except ValueError:
                print(
                    f"Invalid guess. Please enter exactly {CODE_LENGTH} "
                    "of the given colour letters."
                )
                continue
            tries += 1
            if guess == code:
                print(
                    f"Congratulations! You guessed correctly on guess number {tries}!"
                )
                solved = True
            elif tries == MAX_GUESSES:
                print(
                    f"Sorry, you used the maximum amount of {MAX_GUESSES} guesses "
                    f"and did not find the code."
                )
                print(f"The correct colour code was {code}.")
            else:
                print(guess.diff_to_other(code))
        if choice := input('Would you like to try again? Then type "a".') != "a":
            break
