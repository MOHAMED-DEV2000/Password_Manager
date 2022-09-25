import os
import sign_up
import sign_in
from time import sleep
from rich import print as printc
from rich.console import Console
from ast import literal_eval
console = Console()

# This function display a landing page
def main():
    console = Console()
    console.print("\n\t\t [ MS Vault ]", style="bold red")
    console.print("\tWelcome to your secure password manager! Log in\nor create your account to access your secret and secure vaulet.", style="bold green")
    console.print("\n\t1) Log in\n\t2) Sign up\n\t3) Exit\n")
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
    if val != 1 and val != 2 and val != 3:
        while val != 1 and val != 2 and val != 3:
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
    val = main()

    if val_type(val) != int:
        val = mustBeInt(val)
        val = mustBeInMenu(val)
    val = int(val)
    
    # if val == 1:
    #     sleep(0.2)
    #     os.system('cls' if os.name == 'nt' else 'clear')

    #     sign_in.login()
    if val == 2:
        # elif val == 2:
        sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')

        sign_up.create_account()
    # elif val == 3:
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     sleep(0.3)

    #     printc("\n\t\t[yellow]Exiting ..............[/yellow]")
    # else:
    #     printc("\t[red]Please choose a number from the menu[/red]\n")
    #     sleep(1)
    #     os.system('cls' if os.name == 'nt' else 'clear')

    #     inputProccessing()


if __name__ == "__main__":
    inputProccessing()
