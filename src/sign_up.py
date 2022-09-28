import os
import argon2
import main
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

# This function makes sure that the email has the correct format
def email_verification(email):
    if email.endswith('@gmail.com') != True:
        while email.endswith('@gmail.com') != True:
            printc("\t[red]Incorrect email format\n[/red]")
            email = input('\t')
    return email

# This function let the user confirms the password
def password_verification(f_pswrd, l_pswrd):
    if f_pswrd != l_pswrd:
        while f_pswrd != l_pswrd:
            printc("\n\t[red]Password isn't the same try again![/red]\n")
            l_pswrd = getpass('\t')

# This function creates an account
def create_account():

    printc("\n\n\t\t  [green][ Create an account ][/green]\n\n")

    # Taking data from user(username, email, Master password)
    username = input("\tUsername: ")
    email = input("\tEmail: ")
    email = email_verification(email) # verify that email has the correct format

    master_pswrd = getpass("\tCreate a master password: ")
    pswrd_confirm = getpass("\tConform your master password: ")
    password_verification(master_pswrd, pswrd_confirm) # verify that 1st password is same as the 2nd one
    hash = argon2Hasher.hash(master_pswrd)

    printc("\n\t[0]-Exit \t[1]-Register")
    val = input()
    val = main.mustBeInt(val) # Makes sure the value is an integer
    val = main.mustBe0or1(val) # Makes sure the value is either 0 or 1 nothing else

    if val == 1:

        # add an account to your database if it doesn't already exist in the database
        db = make_conncetion()
        db_cursor = db.cursor()

        check_query = """ SELECT COUNT(*) FROM accounts
            WHERE account_username = %s 
            AND account_email = %s
            """ # SQL query to check out how many accounts has the same username and email

        Argadd_query = """INSERT INTO accounts(account_username, account_email, account_hash)
            VALUES (%s, %s, %s)
            """ # SQL query to insert collected data to the database

        db_cursor.execute(check_query, (username, email)) # executes the cheking query
        counter = db_cursor.fetchone()

        x = 0 
        for row in counter:
            x = row

        if x != 0:
            while x != 0:
                printc("\t[yellow]This username is already taken.[/yellow]")
                printc("\t[red]Try again![/red]\n")

                cleanScreen()
                create_account()

        # account doesn't exist yet in database so we add it to the database

        db_cursor.execute(Argadd_query, (username, email, hash))
        db.commit()

        printc("\n\t[green]Your account has been successfully created![/green]")
        db.close()

        # Returning to landing page
        cleanScreen()
        main.inputProccessing()

    elif val == 0:
        cleanScreen()
        main.inputProccessing()
