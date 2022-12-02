import random

__name__ = "utils"
__doc__ = "Utilities script required for playing Guess The Number."

menu_message = '''Welcome to Guess The Number!\n\n
1. Challenge Computer\n
2. Challenge Player\n
3. Help\n
4. Exit\n'''

challenger_message = ''''Welcome to Guess The Number!\n\n
The game is already in progress, so you will be challenging the host.\n'''

help_message = '''This is a simple game of Guess The Number.\n
Here is how it works:\n
- you can choose to play against the computer or another player\n
- the first person to join gets to pick the number, while the second one will try guessing it\n
- a number between 0 and 50 will then be selected by the first player\n
- on each turn, the second player will attempt to guess the number by typing it in\n
- for each wrong guess, a message will appear prompting the player to go higher or lower\n
- once number is guesses, a message containing the scores will be displayed\n
- you can then choose to play again or go back to the main menu\n

That's it, now go have some fun!'''


def generate_random_number() -> int:
    return random.randint(0, 50)