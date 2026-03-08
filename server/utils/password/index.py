import bcrypt

def hash_password(raw_password : str) -> str: 
    
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

def check_password(hashed_password : str, raw_password : str) -> bool :

    correct = bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
    return correct


