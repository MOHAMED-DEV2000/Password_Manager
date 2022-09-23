f int_counter == 0:
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