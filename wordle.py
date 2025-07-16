import pathlib
import random
from string import ascii_letters, ascii_uppercase
from rich.console import Console
from rich.theme import Theme

console = Console(theme=Theme({"warning": "red on yellow"}))
WORDLIST = pathlib.Path("/usr/share/dict/words")
NUM_LETTERS = 5
NUM_GUESSES = 6

def main():
    words = get_words()
    word = random.choice(words)
    guesses = ["_" * NUM_LETTERS] * NUM_GUESSES

    for idx in range(NUM_GUESSES):
        refresh_page(headline=f"Guess {idx + 1}")
        compare_guesses(guesses, word)
        guesses[idx] = get_valid_input(guesses, words)
        if guesses[idx] == word:
            break
    
    game_over(guesses, word, guessed_correctly=guesses[idx] == word)

def get_valid_input(guesses, words):
    while ((word := console.input("[bold blue]\nGuess word: ").upper()) not in words
           or word in guesses):
        refresh_page("Try Again")
        compare_guesses(guesses, "placeholder")
        console.print(f"\n{word} is invalid!", style="warning")
        console.print(f"Word must be exactly {NUM_LETTERS} letters long", style="warning")
        console.print("Word cannot contain any special characters", style="warning")
        console.print("Word cannot have been previously used", style="warning")
        console.print("Word must be a valid word in the dictionary", style="warning")
    return word

def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

def get_words():
    words = [
        word.upper()
        for word in WORDLIST.read_text(encoding="utf-8").strip().split("\n")
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
        ]

    return words

def compare_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify="center")
    console.print("\n" + "".join(letter_status.values()), justify="center")

def game_over(guesses, word, guessed_correctly):
    refresh_page(headline="Game Over")
    compare_guesses(guesses, word)

    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

if __name__ == "__main__":
    main()