#Write a function that checks whether a password is strong
import re
def is_strong_password(password):
    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Z]",password):
        return False
    
    if not re.search(r"[a-z]",password):
        return False
    
    if not re.search(r"\d",password):
        return False
    
    if not re.search(r"[!@#$%^&*()<>?|\/,.]",password):
        return False
    
    return True

password = "Strongpass1!"
print(is_strong_password(password))
    
    
