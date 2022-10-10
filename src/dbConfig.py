from modules import *

console = Console()

# This function makes a connection to the password_manger database

# Todo : later on automate adding the attrs of this function
def make_conncetion():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='N@r02o7uF1?]',
            database='password_manager'
        )
    except Exception:
        printc(
            "[red][!] An error occurred while trying to connect to the database[/red]")
        console.print_exception(show_locals=True)
    return db
