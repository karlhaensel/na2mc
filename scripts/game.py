"""Main game logic for Mastermind."""

from scripts.code import MasterMindCode
from scripts.const import CODE_LENGTH, MAX_GUESSES


def run_game():
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
            raw_guess = input(f"Your guess {tries + 1}:")
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
        if (
            _ := input(
                'Would you like to try again? Type "a"! Any other key exits the game.'
            )
            != "a"
        ):
            break
