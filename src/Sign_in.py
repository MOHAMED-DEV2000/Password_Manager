import os
import main
import argon2
import sign_up
from dbConfig import make_conncetion
from time import sleep
from rich import print as printc
from rich.console import Console
from getpass import getpass

argon2Hasher = argon2.PasswordHasher(
    time_cost = 3, # number of iterations
    memory_cost = 64 * 1024, # 64mb
    parallelism = 1, # how many parallel threads to use
    hash_len = 32, # the size of the derived key
    salt_len = 16 # the size of the random generated salt in bytes
)
console = Console()


def cleanScreen():
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def isUserExist(username, email):
    search_query = """SELECT COUNT(*) FROM accounts
        WHERE account_username = %s 
        AND account_email = %s 
        """
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(search_query, (username, email))
    counter = db_cursor.fetchone()

    str_counter = ' '.join([str(elem) for elem in counter])
    int_counter = int(str_counter)

    if int_counter != 0:
        return True
    return False 

def pwdAuthentication(username, email, MasterPswd):

    get_stored_hash = """SELECT account_hash FROM accounts 
        WHERE account_username = %s
        AND account_email = %s
        LIMIT 1 
        """
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_stored_hash, (username, email))
    StrdAccountHash = db_cursor.fetchone()

    strdAccountHash = ''
    for row in StrdAccountHash:
        strdAccountHash = row

    try:
        areTheyMatch = argon2Hasher.verify(strdAccountHash, MasterPswd)
        return areTheyMatch
    except (Exception, argon2.exceptions.VerifyMismatchError):
        while True:
            printc("\n\t[red] password isn't corresct try again! [/red]\n")
            cleanScreen()
            
            printc("\t\t\t[green][ Password Verification ][/green]\n")
            master_passwrd = getpass("\tPassword:\t\t ")
            areTheyMatch = pwdAuthentication(username, email, master_passwrd)
            if areTheyMatch == True:
                return areTheyMatch            

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
                        
                        printc("\t\t\t[green][ Log in ][/green]\n")
                        username = input("\tUsername:\t\t ")
                        email = input("\tEmail:\t\t ")
                        email = sign_up.email_verification(email)
                        IsUserExit = isUserExist(username, email)

    cleanScreen()

    #TODO Task: Page 2 make sure that the master password is correct
    printc("\t\t\t[green][ Password Verification ][/green]\n")
    master_passwrd = getpass("\tPassword:\t\t ")           
    isValid = pwdAuthentication(username, email, master_passwrd)
    
    cleanScreen()
    account_menu(username, email, master_passwrd)

def edite_password():
    printc("\t\t[yellow]Editing the password is proccessing.......[/yellow]\n")
    # Todo : Give the user the choice of either editing all infos or just one info
    # Todo : Then if user want to change one info go to Single change
    # Todo : Then if user want to change all infos go to full change

def delete_password():
    printc("\t\t[yellow]Deleting the password is proccessing.......[/yellow]\n")
    # Todo : connect to the database and execute a SQL query to delete this password from the valut table

def password_infos(username, email, master_passwrd):
    printc("\t\t[yellow]Password infos is proccessing.......[/yellow]\n")
    # Todo : connect to the database with the account key: 
    # Todo : grap the password from it 
    # Todo : Display all the password infos : 
        # Todo :         [ Platform name ]
        # Todo : Url 
        # Todo : Username
        # Todo : Email
        # Todo : Password
        # Todo :       [0] Exit     [1] Edite
        # Todo :              [2] Delete
    # Todo : DO some logic based on that value
        # Todo : Make sure the value it's int and [0, 2]
        # Todo : If value = 0 Go back to vault
        # Todo : If value = 1 Go to Edite
        # Todo : If value = 2 Go to Delete


def vault(username, email, master_passwrd):
    printc("\t\t [red][ My Vault ][/red]\n\n")
    # TODO : Get all passwords related to this account
        # Todo : First create an account key (hash[username + email + Master_pswd]) to access the vault
        # Todo : Then create a SQL query to search for all passwords that has that key

    # TODO : Display them to user as an ordered list to chose from
        # Todo : loop through and display them all [nbr platform url username email password]
        # Todo : At the bottom [0] Exit

    # TODO : Take the value chosen by user
        # Todo : Take it and proccess it i.e. must be int and within the n passwords we have [0, n]

    # TODO : DO some logic based on that value
        # Todo : If 0 return to account menu
        # Todo : If n != 0 Go to Password info
            # Todo : Where user can Delete or modify the password infos

def add_new_platform_to_vault(username, email, master_passwrd):
    printc("\t\t[yellow]Adding a new password is proccessing.......[/yellow]\n")
    # Todo : First get the account key from the database or just create it(hash[username + email + Master_pswd]) to access the vault
    # Todo : Then take user data(platform_name, url, ....etc)
    # Todo : Then connect to the database and execute a SQL query to add this infos as a new row in the vault
    # Todo : Then say it is successfully done and Go to Vault page with the new password added to it 


# This function shows the application menu to see, edite, delete and add passwords
def account_menu(username, email, master_passwrd):

    printc("\t\t [red] [ Menu ] [/red]\n")
    printc(f"\n\tWelcome back [green]{username}[/green]!\n")
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
