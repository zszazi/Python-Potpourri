import random
from constants import *
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


lives = 6
replay = True


console = Console()

console.print(panel, style= "bold magenta", justify="center")
console.print(panel_zszazi, style = "magenta", justify="right")


def get_random_word(category):
    if category == "Actors":    
        return random.choice(actors).lower()
    elif category == "Country":
        return random.choice(country).lower()
    elif category == "Capital":
        return random.choice(capital).lower()
    elif category == "FootBall Players":
        return random.choice(football).lower()
    elif category == "IPL Players":
        return random.choice(ipl_players).lower()

    
def choose_category():
    console.print("Hangman Categories", style = "Bold blue")
    print()
    categories = ["Capital", "Country", "Actors", "FootBall Players", "IPL Players"]

    for index, cat in enumerate(categories):
        console.print("Press {} for {}".format(index+1, cat), style = "violet",) 
    print()   
    user_input = console.input("[bold blue]      Choose a Category [/]")

    return get_random_word(category=categories[int(user_input)-1])


while replay:

    hangman_word = choose_category()

    guess_list = []
    guess_list = ["_" for _ in range(len(hangman_word))]

    console.print(" ".join(guess_list),justify="center", style="bold green")

    while "_" in guess_list and lives !=0:
        print()
        guess = console.input("[bold magenta] Guess a Letter[/] :game_die: ").lower()
        for index, letter in enumerate(hangman_word):
            if letter == guess:
                guess_list[index] = letter
                console.print(" ".join(guess_list), style = "bold green", justify = "center")

        if guess not in guess_list:
            lives = lives - 1
            console.print("Remaining Lives " + lives * ":sparkling_heart: ", style = "red", justify = "center" ) if lives else console.print("No More Lives" ,style = "red", justify = "center" )
            console.print(stages[lives], style="bold red", justify="right")

    print()
    if lives > 0:
        panel_text = "You Won"
        console.print(Panel(Text(panel_text, justify="center",style= "bold green"),title="Result",padding=1))

    else :
        panel_text = "You Lost \n The correct answer was {}".format(hangman_word.title())
        console.print(Panel(Text(panel_text, justify="center",style= "bold red"),title="Result",padding=1))

    print()
    replay_choice = console.input("[violet]Press [bold green]r[/] to [green]Replay[/] , [bold red]q[/] to [red]Quit[/] then enter => [/]").lower()

    if replay_choice == "r":
        replay = True
    elif replay_choice == "q":
        replay = False
    print()
