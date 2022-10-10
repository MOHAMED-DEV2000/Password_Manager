from modules import *

# Creating the required objects
argon2_hasher_obj = argon2.PasswordHasher(

        time_cost = 3, # number of iterations
        memory_cost = 64 * 1024, # 64mb
        parallelism = 1, # how many parallel threads to use
        hash_len = 32, # the size of the derived key
        salt_len = 16 # the size of the random generated salt in bytes
)
console = Console()

# This function clears the command line prompt
def cleanScreen():

    sleep(1.1)
    os.system('cls' if os.name == 'nt' else 'clear')

# This function checks if the account the user wants to log in exist or not
def is_user_exist(username, email):

    search_query = """SELECT COUNT(*) FROM accounts
        WHERE account_username = %s 
        AND account_email = %s 
        """

    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(search_query, (username, email))

    # counting the accounts that has the same username & email the user inputed 
    accounts_counter = int(' '.join([str(elem) for elem in db_cursor.fetchone()]))

    if accounts_counter != 0:
        return True
    return False

# This function checks if the password given by user matches the account password
def master_pwd_authentication(username, email, MasterPswd):

    get_stored_hash = """SELECT account_hash FROM accounts 
        WHERE account_username = %s
        AND account_email = %s
        LIMIT 1 
        """

    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_stored_hash, (username, email))

    account_hash = ''.join([row for row in db_cursor.fetchone()])

    try:
        # Campare the hash of the password given by user & the account hash
        are_they_a_match = argon2_hasher_obj.verify(account_hash, MasterPswd)
        return are_they_a_match

    except (Exception, argon2.exceptions.VerifyMismatchError):
        # Making sure the user gives the right master password
        while True:
            printc("\n\t[red] password isn't corresct try again! [/red]\n")
            cleanScreen()
            
            printc("\t\t\t[green][ Password Verification ][/green]\n")
            master_passwrd = getpass("\tPassword:\t\t ")
            are_they_a_match = master_pwd_authentication(username, email, master_passwrd)

            if are_they_a_match == True:
                return are_they_a_match            

# This function logs in into your personnel vaulet account
def login():
    
    # Todo : Add Forget password? function if it is chosen
    """ Take his email and send a verification message contains a random string of lenght = 5
    Print Verification code and wait him to enter what you sent in his email
    If it is correct let him reset his master password."""
    
    # Checking if the account exist
    printc("\t\t\t[green][ Log in ][/green]\n")
    username = input("\tUsername:\t\t ")
    email = input("\tEmail:\t\t ")
    email = sign_up.email_verification(email)
    is_exist = is_user_exist(username, email)
    
    if is_exist != True:
            while is_exist != True:
                        # ERROR MESSAGE FOR THE USER
                        printc("\n\t[yellow]No account has been found![/yellow]")
                        printc("\t[red]Please try again![/red]")
                        cleanScreen()
                        
                        printc("\t\t\t[green][ Log in ][/green]\n")
                        username = input("\tUsername:\t\t ")
                        email = input("\tEmail:\t\t ")
                        email = sign_up.email_verification(email)
                        is_exist = is_user_exist(username, email)

    cleanScreen()

    # Checking if the master password is correct
    printc("\t\t\t[green][ Password Verification ][/green]\n")
    master_passwrd = getpass("\tPassword:\t\t ")           
    is_master_pswrd_valid = master_pwd_authentication(username, email, master_passwrd)
    
    if is_master_pswrd_valid:
        cleanScreen()
        account_menu(username, email, master_passwrd)

# This function shows the application menu to see, edite, delete and add passwords
def account_menu(username, email, master_passwrd):
    printc("\t\t [red] [ Menu ] [/red]\n")
    printc(f"\n\tWelcome back [green]{username}[/green]!\n")
    printc("\t[0] My Vault")
    printc("\t[1] Add a password")
    printc("\t[2] Exit\n\t")

    val = main.mustBeInMenu(main.mustBeInt(input()))

    if val == 0:
        cleanScreen()
        vault(username, email, master_passwrd)

    elif val == 1:
        cleanScreen()
        add_new_platform_to_vault(username, email, master_passwrd)

    elif val == 2:
        printc("\t\t[yellow]Returing to home page .........[/yellow]\n")
        cleanScreen()

        main.inputProccessing()

# This function shows all details that are related a password
def platform_infos(account_id, platform_name, username, email, master_passwrd):

    # Todo : connect to the database through the account id:
    get_platform_id_query = """SELECT password_id FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_url_query = """SELECT platform_url FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_username_query = """SELECT platform_username FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_email_query = """SELECT platform_email FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_encryption_key_query = """SELECT encryption_key FROM vault WHERE account_id = %s AND platform_name = %s"""
    get_platform_password_query = """SELECT platform_password FROM vault WHERE account_id = %s AND platform_name = %s"""

    db = make_conncetion()
    db_cursor = db.cursor()

    # Todo : Solve this TypeError: 'NoneType' object is not iterable in 'get_platform_id' i think
    db_cursor.execute(get_platform_id_query, (account_id, platform_name))
    get_platform_id = db_cursor.fetchone()
    platform_id_as_list = [row for row in get_platform_id] # These three line for converting the id from a list to int
    platform_id_as_str = "".join([str(i) for i in platform_id_as_list])
    platform_id = int(platform_id_as_str)

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
    e_platform_password = ''.join([row for row in get_platform_password])

    db_cursor.execute(get_encryption_key_query, (account_id, platform_name))
    get_encryption_key = db_cursor.fetchone()
    encryption_key = ''.join([row for row in get_encryption_key])

    f_obj = Fernet(encryption_key)
    platform_password = str(f_obj.decrypt(e_platform_password), 'utf-8')

    # Todo : Display all the password infos :
    cleanScreen()
    printc(f"\n\t\t[yellow][ {platform_name} ][/yellow]\n\n")
    printc(f"\t[green]URL:[/green] {platform_url}\n")
    printc(f"\t[green]Username:[/green] {platform_username}\n")
    printc(f"\t[green]Email:[/green] {platform_email}\n")
    printc(f"\t[green]Password:[/green] {platform_password}\n")
    printc("    [0] [green]Exit[/green] \t[1] [yellow]Edit[/yellow] \t[2] [red]Delete[/red]\n")

    val = main.mustBeInMenu(main.mustBeInt(input()))

    if val == 0:
        printc("\t[yellow]Returning to My Vault .......[/yellow]")
        cleanScreen()
        vault(username, email, master_passwrd)

    elif val == 1:
        cleanScreen()
        edit_password(username, email, master_passwrd)

    elif val == 2:
        value = input("Are you sure you want to delete this password from your vault?(Y/N)\n").lower()
        if value.startswith("n"):
            cleanScreen()
            platform_infos(account_id, platform_name, username, email, master_passwrd)

        cleanScreen()
        delete_password(platform_id, platform_name, username, email, master_passwrd)

# This function make sure the value inputed is within the range of paltform nbrs list
def must_be_in_platform_list(val, platform_counter):
    platform_counter += 1
    if val > platform_counter:
        while val > platform_counter:
            printc("\t[red]Please try again![/red]")
            val = main.mustBeInt(input())
        return int(val)
    return int(val)

# This function showa a menu from where the user can chose what to do in his account
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
            Row = ''.join([i for i in row])
            printc(f"\t[{row_nbr}] {Row}\n")
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
    try:
        platform = ''.join([i for i in list_of_platforms[val]])
        platform_infos(account_id, platform, username, email, master_passwrd)
    except KeyError:
        print('key does not exist in dict')
        list_of_platforms[0] = ''
        platform = ''.join([i for i in list_of_platforms[val]])
        platform_infos(account_id, platform, username, email, master_passwrd)
        

# This function deletes a password from the account vault
def delete_password(platform_id, platform_name, username, email, master_passwrd):

    # Todo : add a deletion verification query to be sure the password was deleted
    verify_deletion_query = """SELECT COUNT(*) FROM vault
        WHERE password_id = %s AND platform_name = %s
    """
    delete_platform_query = """DELETE FROM `password_manager`.`vault` 
        WHERE (`password_id` = %s AND platform_name = %s)
    """

    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(delete_platform_query, (platform_id, platform_name))
    db.commit()
    db_cursor.execute(verify_deletion_query, (platform_id, platform_name))

    platforms_counter = int(' '.join([str(elem) for elem in db_cursor.fetchone()]))

    if platforms_counter != 0:
        # printc("\tThrough some ERROR message for you not for user or run some code to make sure deletion is Done!\n")
        pass
    
    printc("\t\t[green]The password was deleted successfully![/green]\n")
    printc("\t\t[yellow]Returning to My Vault .......[/yellow]\n")
    cleanScreen()

    db.close()
    vault(username, email, master_passwrd)

# This function modifies the infos related to a password
def edit_password(username, email, master_passwrd):
    
    printc(f"\n\t\t[yellow][ Editing ][/yellow]\n\n")
    printc("\n\t[0] Edit all \t [1] Single Edit\n")
    user_choice = main.mustBe0or1(main.mustBeInt(input()))

    if user_choice == 0:
        # edit_all_paswrd_infos()
        pass
    elif user_choice == 1:
        # printc("\t[1] pswrd \n [2] Email ....")
        # edite(selected_data)
        pass

    # Todo : Then if user want to change all infos go to full change
    printc("\t\t[yellow]Editing the password is proccessing.......[/yellow]\n")

# This function adds a new password to user account vault
def add_new_platform_to_vault(username, email, master_passwrd):
    # Todo : First get the account id from the database to access the vault
    get_account_id_query = """SELECT account_id FROM accounts
        WHERE account_username = %s 
        AND account_email = %s
        LIMIT 1
    """
    add_platform_query = """INSERT INTO vault (platform_name, platform_url, platform_username, platform_email, platform_password, encryption_key, account_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    db = make_conncetion()
    db_cursor = db.cursor()
    db_cursor.execute(get_account_id_query, (username, email))
    get_account_id = db_cursor.fetchone()

    account_id : int
    for row in get_account_id:
        account_id = row

    # Todo : Then take user data(platform_name, url, ....etc)
    printc("\t\t[green][ New platform ][/green]\n")
    platform_name = input("\n\tPlatform name: ")
    platform_url = input("\n\tURL: ")
    platform_username = input("\n\tUsername: ")
    platform_email = sign_up.email_verification(input("\n\tEmail: "))

    key = Fernet.generate_key()
    f_obj = Fernet(key)
    platform_password = f_obj.encrypt(getpass("\n\tPassword: ").encode())

    # Todo : Then connect to the database and execute a SQL query to add this infos as a new row in the vault
    db_cursor.execute(add_platform_query, (platform_name, platform_url, platform_username, platform_email, platform_password, key, account_id))
    db.commit()
    db.close()

    # Todo : Then say it is successfully done and Go to Vault page with the new password added to it 
    printc(f"\t[green]{platform_name} was successfully added to your vault .......[/green]\n")
    cleanScreen()

    account_menu(username, email, master_passwrd)



