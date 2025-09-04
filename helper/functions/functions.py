import re 
from hashlib import sha256
#===============================================
def check_password(pwd: str)-> bool:
    # This function checking the valide password
    password_regex = r"(?=.*[a-zA-Z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%#?&]{8,}$"

    if re.fullmatch(password_regex, pwd):
        return True 
    else: return False

#===============================================
def check_email(pwd: str)-> bool:
    # this function checking the valid email
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.fullmatch(email_regex, pwd):
        return True 
    else: return False

#===============================================
def hash_password(pwd: str) -> str:
    #this function hash and return the clear password passed in parameter

    clear_password = b""+pwd.encode("utf-8")
    return sha256(clear_password).hexdigest()


# ====  testing code 

if __name__ == "__main__":
    print(hash_password("Hello world"))