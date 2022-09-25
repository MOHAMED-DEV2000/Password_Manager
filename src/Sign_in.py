import os
from dbConfig import make_conncetion
from time import sleep
from rich import print as printc
from rich.console import Console
from ast import literal_eval
from getpass import getpass
console = Console()


# This function logs in into your personnel vaulet account
def login():
    printc("\t\t\t[green][ Log in ][/green]\n")
    username = input("\tUsername:\t\t ")

    email = input("\tEmail:\t\t ")
    # Add email verification

    master_passwrd = getpass("\tPassword:\t\t ")
    # Add password confirmation
    master_passwrd.encode('utf-8')
    # salt = bcrypt.gensalt(12)
    get_salt = """SELECT salt FROM accounts 
        WHERE account_username = '%s'
        AND account_email = '%s'
        LIMIT 1
        """

    db = make_conncetion()
    db_cursor = db.cursor()

    search_query = """SELECT COUNT(*) FROM accounts
        WHERE account_username = '%s' 
        AND account_email = '%s' 
        AND account_hash = '%s'"""

    db_cursor.execute(search_query % (username, email, master_passwrd))
    counter = db_cursor.fetchone()
    printc(counter)

    str_counter = ' '.join([str(elem) for elem in counter])
    printc(str_counter)

    int_counter = int(str_counter)
    printc(int_counter)

    if int_counter == 0:
        printc("\n\t[yellow]No account has been found![/yellow]")
        printc("\t[red]Please try again![/red]")
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        login()
    else:
        printc(f"\n\tWelcome back [green]{username}[/green]!\n")
        get_account_id_query = """SELECT account_id FROM accounts 
       WHERE account_username = '%s' 
       AND account_email = '%s' 
       AND account_hash = '%s'"""

        db_cursor.execute(get_account_id_query %
                          (username, email, master_passwrd))
        Id = db_cursor.fetchone()

        # Converting the Id data type from a tyole to an integer
        int_id = functools.reduce(lambda sub, ele: sub * 10 + ele, Id)
        db.close()

        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        account_menu(int_id)


def vault(account_id):
    printc("\t\t [red][ My Vaulet ][/red]\n\n")


def add_password_to_vault(account_id):
    printc("\t\t[yellow]Adding a new password is proccessing.......[/yellow]\n")

# This function shows the application menu to see, edite, delete and add passwords


def account_menu(account_id):
    account_id = account_id

    printc("\t\t [red] [ Menu ] [/red]\n")
    printc("\t1) My Vault")
    printc("\t2) Add a password")
    printc("\t3) Exit\n\t")

    val = input()
    val = mustBeInt(val)
    val = mustBeInMenu(val)

    if val == 1:
        vault(account_id)
    elif val == 2:
        add_password_to_vault(account_id)
    elif val == 3:
        printc("\t\t[yellow]Returing to home page .........[/yellow]\n")
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        inputProccessing()
