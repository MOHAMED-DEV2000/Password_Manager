import os
import functools
import encrypt
from dbConfig import make_conncetion
from time import sleep
from rich import print as printc
from rich.console import Console
from ast import literal_eval
from getpass import getpass
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
    if val == 1:
        sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')
        login()
    elif val == 2:
        sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')
        create_account()
    elif val == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        sleep(0.3)
        printc("\n\t\t[yellow]Exiting ..............[/yellow]")
    else:
        printc("\t[red]Please choose a number from the menu[/red]\n")
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        inputProccessing()

def email_verification(email):
    if email.endswith('@gmail.com') != True:
        while email.endswith('@gmail.com') != True:
            printc("\t[red]Incorrect email format\n[/red]")
            email = input('\t')
    return email

def password_verification(f_pswrd, l_pswrd):
    if f_pswrd != l_pswrd:
        while f_pswrd != l_pswrd:
            printc("\n\t[red]Password isn't the same try again![/red]\n")
            l_pswrd = getpass('\t')
    return f_pswrd

# This function creates an account
def create_account():

    printc("\n\n\t\t  [green][ Create an account ][/green]\n\n")
    username = input("\tUsername: ")
    email = input("\tEmail: ")

    email = email_verification(email)

    master_pswrd = getpass("\tCreate a master password: ")
    pswrd_confirmation = getpass("\tConform your master password: ")

    password_verification(master_pswrd, pswrd_confirmation)
    
    master_pswrd = encrypt.argon2_hash(master_pswrd)

    printc("\n\t[0]-Exit \t[1]-Register")
    val = input()
    val = mustBeInt(val)
    val = mustBe0or1(val)
    
    if val == 1:

        # add an account to your database if it doesn't already exist in the database
        db = make_conncetion()
        db_cursor = db.cursor()
        
        # check_query = "SELECT account_username, account_email FROM accounts WHERE account_username = '%s' AND account_email = '%s'"
        check_query = "SELECT COUNT(*) FROM accounts WHERE account_username = '%s' AND account_email = '%s'"
        add_query = "INSERT INTO accounts(account_username, account_email, account_master_passwrd) VALUES ('%s', '%s', '%s')"

        db_cursor.execute(check_query%(username, email))
        counter = db_cursor.fetchone()
        
        str_counter = ' '.join([str(elem) for elem in counter]) 
        int_counter = int(str_counter)

        if int_counter != 0:
            while int_counter != 0:
                printc("\t[yellow]This username is already taken.[/yellow]")
                printc("\t[red]Try again![/red]\n")
                sleep(1.8)
                os.system('cls' if os.name == 'nt' else 'clear')
                create_account()

        # account doesn't exist yet in database so we add it to the database
        db_cursor.execute(add_query%(username, email, master_pswrd))
        db.commit()
        printc("\n\t[green]Your account has been successfully created![/green]")
        db.close()
        
        # Returning to landing page
        sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        inputProccessing() 

    elif val == 0:
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        inputProccessing()

# This function logs in into your personnel vaulet account
def login():
    printc("\t\t\t[green][ Log in ][/green]\n")
    username = input("\tUsername:\t\t ")

    email = input("\tEmail:\t\t ")
    # Add email verification

    master_passwrd = getpass("\tPassword:\t\t ")
    # Add password confirmation

    master_passwrd = encrypt.argon2_hash(master_passwrd)

    db = make_conncetion() 
    db_cursor = db.cursor()
    
    search_query = """SELECT COUNT(*) FROM accounts
        WHERE account_username = '%s' 
        AND account_email = '%s' 
        AND account_master_passwrd = '%s'"""

    db_cursor.execute(search_query%(username, email, master_passwrd))
    counter = db_cursor.fetchone()
    printc(counter)

    str_counter = ' '.join([str(elem) for elem in counter]) 
    printc(str_counter)

    int_counter = int(str_counter)
    printc(int_counter)


    # if int_counter == 0:
    #    printc("\n\t[yellow]No account has been found![/yellow]")
    #    printc("\t[red]Please try again![/red]")
    #    sleep(2)
    #    os.system('cls' if os.name == 'nt' else 'clear')
    #    login()
    # else:
    #    printc(f"\n\tWelcome back [green]{username}[/green]!\n")
    #    get_account_id_query = """SELECT account_id FROM accounts 
    #    WHERE account_username = '%s' 
    #    AND account_email = '%s' 
    #    AND account_master_passwrd = '%s'"""

    #    db_cursor.execute(get_account_id_query%(username, email, master_passwrd))
    #    Id = db_cursor.fetchone()
       
    #    # Converting the Id data type from a tyole to an integer
    #    int_id = functools.reduce(lambda sub, ele: sub * 10 + ele, Id)
    #    db.close()

    #    sleep(2)
    #    os.system('cls' if os.name == 'nt' else 'clear')
    #    account_menu(int_id)

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


if __name__ == "__main__":
    inputProccessing()