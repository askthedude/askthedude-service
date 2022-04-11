import bcrypt as bcrypt


HASH_SALT_CONSTANT=10


def get_hashed_password(plain_text_password):
    try:
        passwrd = plain_text_password.encode('utf-8')
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(passwrd, bcrypt.gensalt(HASH_SALT_CONSTANT)).decode('utf-8')
    except Exception as e:
        print(e)
        return ""


def check_password(plain_text_password, hashed_password):
    try:
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(e)
        return False