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

    # Todo : Add Forget password? function if it is chosen
    # Take his email and send a verification message contains a random string of lenght = 5
    # Print Verification code and wait him to enter what you sent in his email
    # If it is correct let him reset his master password

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
    # Todo : Give the user the choice of either editing all infos or just one info
    # Todo : Then if user want to change one info go to Single change
    # Todo : Then if user want to change all infos go to full change
    printc("\t\t[yellow]Editing the password is proccessing.......[/yellow]\n")

def delete_password():
    # Todo : connect to the database and execute a SQL query to delete this password from the valut table
    printc("\t\t[yellow]Deleting the password is proccessing.......[/yellow]\n")

def platform_infos(account_id, platform_name, username, email, master_passwrd):
    def mustBeInMenu(val):
        if val != 0 and val != 1 and val != 2:
            while val != 0 and val != 1 and val != 2:
                printc("\t[red]Please try again![/red]")
                val = main.mustBeInt(input())
            return int(val)
        return int(val)

    # Todo : connect to the database through the account id:
    get_platform_url_query = """SELECT platform_url FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_username_query = """SELECT platform_username FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_email_query = """SELECT platform_email FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_password_query = """SELECT platform_password FROM vault WHERE account_id = %s AND platform_name = %s"""

    db = make_conncetion()
    db_cursor = db.cursor()

    db_cursor.execute(get_platform_url_query, (account_id, platform_name))
    get_platform_url = db_cursor.fetchone()
    platform_url = ''.join([row for row in get_platform_url])

    db_cursor.execute(get_platform_username_query, (account_id, platform_name))
    get_platform_username = db_cursor.fetchone()
    platform_username = ''.join([row for row in get_platform_username])

    db_cursor.execute(get_platform_email_query, (account_id, platform_name))
    get_platform_email = db_cursor.fetchone()
    platform_email = ''.join([row for row in get_platform_email])

    db_cursor.execute(get_platform_password_query, (account_id, platform_name))
    get_platform_password = db_cursor.fetchone()
    platform_password = ''.join([row for row in get_platform_password])

    # Todo : Display all the password infos :
    cleanScreen()
    printc(f"\n\t\t[yellow][ {platform_name} ][/yellow]\n\n")
    printc(f"\t[green]URL:[/green] {platform_url}\n")
    printc(f"\t[green]Username:[/green] {platform_username}\n")
    printc(f"\t[green]Email:[/green] {platform_email}\n")
    printc(f"\t[green]Password:[/green] {platform_password}\n")
    printc("    [0] [green]Exit[/green] \t[1] [yellow]Edite[/yellow] \t[2] [red]Delete[/red]\n")

    val = main.mustBeInt(input())
    val = mustBeInMenu(val)

    if val == 0:
        printc("\t[yellow]Returning to My Vault .......[/yellow]")
        cleanScreen()
        vault(username, email, master_passwrd)

    elif val == 1:
        cleanScreen()
        edite_password()

    elif val == 2:
        cleanScreen()
        delete_password()


def must_be_in_platform_list(val, platform_counter):
    platform_counter += 1
    if val > platform_counter:
        while val > platform_counter:
            printc("\t[red]Please try again![/red]")
            val = main.mustBeInt(input())
        return int(val)
    return int(val)

def convertTuple(tup):
    # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

def vault(username, email, master_passwrd):
    # Todo : Get all passwords related to this account
    printc("\t\t [red][ My Vault ][/red]\n\n")
    
    get_account_id_query = """SELECT account_id FROM accounts
        WHERE account_username = %s 
        AND account_email = %s
        LIMIT 1
    """ ## Todo : First get the account id

    get_platform_name__by_id_query = """SELECT platform_name FROM vault
        WHERE account_id = %s
    """ ## Todo : Then create a SQL query to search for all passwords that has that account id
    
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_account_id_query, (username, email))
    get_account_id = db_cursor.fetchone()

    account_id : int
    for row in get_account_id:
        account_id = row
    
    db_cursor.execute(get_platform_name__by_id_query, (account_id, ))
    get_platform_name = db_cursor.fetchall()

    # TODO : Display them to user as an ordered list to chose from
    ## Todo : loop through and display them all [nbr platform url username email password]
    list_of_platforms = {}
    row_nbr, platform_counter = 1, 0
    for row in get_platform_name:
        if row is not None:
            Row = convertTuple(row)
            printc(f"\t{row_nbr}) {Row}\n")
            platform_counter += 1
            list_of_platforms[row_nbr] = row
        row_nbr += 1

    if platform_counter == 0:
        printc("\t[yellow]No platform has been added yet![/yellow]")
        cleanScreen()

        account_menu(username, email, master_passwrd)
        
    printc("\t\t[0] Exit\n")

    # TODO : Take the value chosen by user
    ## Todo : Take it and proccess it i.e. must be int and within the n passwords we have [0, n]
    val = main.mustBeInt(input())
    val = must_be_in_platform_list(val, row_nbr)
    
    # TODO : DO some logic based on that value
    ## Todo : If val == 0 return to account menu
    if val == 0:
        cleanScreen()
        printc("\t[yellow]Returning to Account Menu .......[/yellow]")
        account_menu(username, email, master_passwrd)
    
    ## Todo : If val == n Go to Platform info of this n Where user can Delete or modify the password infos
    platform_infos(account_id, convertTuple(list_of_platforms[val]), username, email, master_passwrd)

def add_new_platform_to_vault(username, email, master_passwrd):
    # Todo : First get the account id from the database to access the vault
    get_account_id_query = """SELECT account_id FROM accounts
        WHERE account_username = %s 
        AND account_email = %s
        LIMIT 1
    """
    add_platform_query = """INSERT INTO vault (platform_name, platform_url, platform_username, platform_email, platform_password, account_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_account_id_query, (username, email))
    get_account_id = db_cursor.fetchone()

    account_id : int
    for row in get_account_id:
        account_id = row

    # Todo : Then take user data(platform_name, url, ....etc)
    printc("\t\t[green][ New platform ][/green]\n\n")
    platform_name = input("\tPlatform name: \n")
    platform_url = input("\tURL: \n")
    platform_username = input("\tUsername: \n")
    platform_email = input("\tEmail: \n")
    platform_password = getpass("\tPassword: \n")

    # Todo : Then connect to the database and execute a SQL query to add this infos as a new row in the vault
    db_cursor.execute(add_platform_query, (platform_name, platform_url, platform_username, platform_email, platform_password, account_id))
    db.commit()
    db.close()

    # Todo : Then say it is successfully done and Go to Vault page with the new password added to it 
    printc(f"\t[green]{platform_name} was successfully added to your vault .......[/green]\n")
    cleanScreen()

    account_menu(username, email, master_passwrd)

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
        cleanScreen()
        vault(username, email, master_passwrd)

    elif val == 2:
        cleanScreen()
        add_new_platform_to_vault(username, email, master_passwrd)

    elif val == 3:
        printc("\t\t[yellow]Returing to home page .........[/yellow]\n")
        cleanScreen()

        main.inputProccessing()
