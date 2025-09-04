import re 

def check_password(pwd: str)-> bool:
    # This function checking the valide password
    password_regex = r"(?=.*[a-zA-Z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%#?&]{8,}$"

    if re.fullmatch(password_regex, pwd):
        return True 
    else: return False

def check_email(pwd: str)-> bool:
    # this function checking the valid email
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.fullmatch(email_regex, pwd):
        return True 
    else: return False

# ====  testing code 

# if __name__  == "__main__":
#     list_of_email = ['dryikobu987@gmia.com', 'passw.com', 'password1^@passwor.com', 'password@emi.com', 'password@']
#     list_of_password = ['1289878892', 'kjkskjkls', 'kdslklksld2898', 'drykdKK88', 'KJkdslk9880@?']

#     for email in list_of_email:
#         print(f"Is this a valide email {email} ?  : {check_email(email)}")
#     print("*"*50)
#     for password in list_of_password:
#         print(f"Is this valide password {password} ? {check_password(password)}")
