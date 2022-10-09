# importing the os, time, rich and ast libraries
import os
from time import sleep
from ast import literal_eval
from rich import print as printc
from rich.console import Console

# importing the local modules
import sign_up
import sign_in

# Creating the required objects
console = Console()

def cleanScreen():

    sleep(1.1)
    os.system('cls' if os.name == 'nt' else 'clear')

# This function display a landing page
def MS_vault_interface():

    console.print("\n\t\t\t [ MS Vault ]", style="bold red")
    console.print("\tWelcome to your secure password manager! Log in\nor create your account to access your secret and secure vaulet.", style="bold")
    printc("\n\t[green][0] Log in[/green]\n\t[yellow][1] Sign up[/yellow]\n\t[red][2] Exit[/red]\n")
    val = input()

    return val

# This function tell us what type of data the user inputed
def val_type(val):
    try:
        return type(literal_eval(val))
    except (ValueError, SyntaxError):
        return str

# This function makes sure the val is an integer
def mustBeInt(val):
    if val_type(val) != int:
        while val_type(val) != int:
            printc("\t[red]Try again![/red]")
            val = input()
        return int(val)
    return int(val)

# This function makes sure it's within the range [1, 3]
def mustBeInMenu(val):
    if val != 0 and val != 1 and val != 2:
        while val != 0 and val != 1 and val != 2:
            printc("\t[red]Please try again![/red]")
            val = mustBeInt(input())
        return int(val)
    return int(val)

# This function makes sure value is within [0, 1]
def mustBe0or1(val):
    if val != 0 and val != 1:
        while val != 0 and val != 1:
            print("\tPlease try again!")
            val = mustBeInt(input())
        return int(val)
    return int(val)

# This function for the input proccessing operation
def inputProccessing():
    val = MS_vault_interface()

    if val_type(val) != int:
        val = mustBeInt(val)
        val = mustBeInMenu(val)
    val = int(val)
    
    if val == 0:
        cleanScreen()
        sign_in.login()

    elif val == 1:
        cleanScreen()

        sign_up.create_account()
    elif val == 2:
        printc("\n\t\t[yellow]Exiting ..............[/yellow]")
        cleanScreen()
        
    else:
        printc("\t[red]Please choose a number from the menu[/red]\n")
        cleanScreen()

        inputProccessing()


if __name__ == "__main__":
    inputProccessing()