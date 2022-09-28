import os
from platform import platform
import main
import argon2
import sign_up
from dbConfig import make_conncetion
from time import sleep
from rich import print as printc
from rich.console import Console
from getpass import getpass

argon2Hasher = argon2.PasswordHasher(
    time_cost=3, # number of iterations
    memory_cost=64 * 1024, # 64mb
    parallelism=1, # how many parallel threads to use
    hash_len=32, # the size of the derived key
    salt_len=16 # the size of the random generated salt in bytes
)
console = Console()


def cleanScreen():
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def isUserExist(username, email):
    search_query = """SELECT COUNT(*) FROM accounts
        WHERE account_username = "%s" 
        AND account_email = "%s" 
        """
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(search_query % (username, email))
    counter = db_cursor.fetchone()

    str_counter = ' '.join([str(elem) for elem in counter])
    int_counter = int(str_counter)

    if int_counter != 0:
        return True
    return False 

def pwdAuthentication(username, email, MasterPswd):
    get_hash = """SELECT account_hash FROM accounts 
        WHERE account_username = '%s'
        AND account_email = '%s'
        LIMIT 1 
        """
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_hash % (username, email))
    j = db_cursor.fetchone()
    J = ''
    for h in j:
        J = h
    verifyValid = argon2Hasher.verify(J, MasterPswd)

    return verifyValid

# This function logs in into your personnel vaulet account
def login():
    #TODO Task: Page 1 make sure that we have the account in the database
    printc("\t\t\t[green][ Log in ][/green]\n")

    username = input("\tUsername:\t\t ")
    email = input("\tEmail:\t\t ")
    email = sign_up.email_verification(email)
    IsUserExit = isUserExist(username, email)
    
    if IsUserExit != True:
            while IsUserExit != True:
                        printc("\n\t[yellow]No account has been found![/yellow]")
                        printc("\t[red]Please try again![/red]")
                        cleanScreen()

                        username = input("\tUsername:\t\t ")
                        email = input("\tEmail:\t\t ")
                        email = sign_up.email_verification(email)
                        IsUserExit = isUserExist(username, email)

    cleanScreen()

    #TODO Task: Page 2 make sure that the master password is correct
    printc(f"\n\tWelcome back [green]{username}[/green]!\n")
    master_passwrd = getpass("\tPassword:\t\t ")           
    isValid = pwdAuthentication(username, email, master_passwrd)
    if isValid != True:
        while isValid != True:
            printc("\tpassword isn't corresct try again!\n")
            cleanScreen()

            master_passwrd = getpass("\tPassword:\t\t ")
            isValid = pwdAuthentication(username, email, master_passwrd)
    
    cleanScreen()
    account_menu(username, email, master_passwrd)

def vault(username, email, master_passwrd):
    printc("\t\t [red][ My Vault ][/red]\n\n")

def add_new_platform_to_vault(username, email, master_passwrd):
    printc("\t\t[yellow]Adding a new password is proccessing.......[/yellow]\n")

# This function shows the application menu to see, edite, delete and add passwords
def account_menu(username, email, master_passwrd):

    printc("\t\t [red] [ Menu ] [/red]\n")
    printc("\t1) My Vault")
    printc("\t2) Add a password")
    printc("\t3) Exit\n\t")

    val = input()
    val = main.mustBeInt(val)
    val = main.mustBeInMenu(val)

    if val == 1:
        vault(username, email, master_passwrd)

    elif val == 2:
        add_new_platform_to_vault(username, email, master_passwrd)

    elif val == 3:
        printc("\t\t[yellow]Returing to home page .........[/yellow]\n")
        cleanScreen()

        main.inputProccessing()
