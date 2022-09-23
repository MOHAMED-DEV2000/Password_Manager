import bcrypt
from argon2 import PasswordHasher
ph = PasswordHasher()

def bcrypt_hash(master_paswrd):
    master_paswrd = master_paswrd.encode('utf-8')
    salt = bcrypt.gensalt(15)
    salted_hash = bcrypt.hashpw(master_paswrd, salt)
    
    return salted_hash

def argon2_hash(master_paswrd):
    paswrd_hash = ph.hash(master_paswrd)
    return paswrd_hash



