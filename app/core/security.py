from bcrypt import hashpw, gensalt, checkpw

def hash_password(password: str):
    salt = gensalt()
    pw_bytes = password.encode('utf-8')
    hashed_password = hashpw(pw_bytes, salt)
    return hashed_password.decode('utf-8')

def check_password(plain_password: str, hashed_password: str):
    return checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )