# importing the os, argon2, time, rich and getpass libraries
import os
import argon2
from getpass import getpass
from time import sleep
from rich import print as printc
from rich.console import Console

# importing the local modules
import main
from dbConfig import make_conncetion

# Creating the required objects
argon2_hasher_obj = argon2.PasswordHasher(

        time_cost = 3, # number of iterations
        memory_cost = 64 * 1024, # 64mb
        parallelism = 1, # how many parallel threads to use
        hash_len = 32, # the size of the derived key
        salt_len = 16 # the size of the random generated salt in bytes
)
console = Console()

def cleanScreen():
    sleep(1.1)
    os.system('cls' if os.name == 'nt' else 'clear')

def username_verification(username: str) -> str:
    while True:
        db = make_conncetion()
        db_cursor = db.cursor()

        check_query = """ SELECT COUNT(*) FROM accounts
        WHERE account_username = (%s)
        """
        db_cursor.execute(check_query, (username, )) # executes the cheking query
        account_counter = db_cursor.fetchone()

        Account_counter = 0 
        for row in account_counter:
            Account_counter = row

        if Account_counter == 0:
            return username

        cleanScreen()
        printc("\n\n\t\t  [green][ Create an account ][/green]\n\n")
        printc("\t[yellow]This username is already taken!\n[/yellow]")
        username = input("\tUsername: ")

# This function makes sure that the email has the correct format
def email_verification(email: str) -> str:
    if email.endswith('@gmail.com') != True:
        while email.endswith('@gmail.com') != True:
            printc("\t[red]Incorrect email format\n[/red]")
            email = input('\t')
    return email

# This function let the user confirms the password
def password_verification(f_pswrd: str, l_pswrd: str) -> None:
    # TODO Task: Fix a bug here
    if f_pswrd != l_pswrd:
        while f_pswrd != l_pswrd:
            printc("\n\t[red]Passwords do not match try again![/red]\n")
            l_pswrd = getpass('\t')

# This function creates an account
def create_account():

    printc("\n\n\t\t  [green][ Create an account ][/green]\n\n")

    # Taking data from user(username, email, Master password)
    username = input("\tUsername: ")
    username  = username_verification(username)

    email = input("\tEmail: ")
    email = email_verification(email) # verify that email has the correct format

    master_pswrd = getpass("\tCreate a master password: ")
    pswrd_confirm = getpass("\tConform your master password: ")
    password_verification(master_pswrd, pswrd_confirm) # verify that 1st password is same as the 2nd one
    hash = argon2_hasher_obj.hash(master_pswrd)

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
        account_counter = db_cursor.fetchone()

        Account_counter = 0 
        for row in account_counter:
            Account_counter = row

        if Account_counter != 0:
            while Account_counter != 0:
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
        printc("\n\t[yellow]Returing to home page .........[/yellow]\n")
        cleanScreen()
        main.inputProccessing()
