import bcrypt
import uuid

def hash_password(input_pwd):
    """
        generate the hash password for your password
    """
    stored_hashed_constant = b'$2b$12$rHcOz3tq9kNxwLBC2dmBCem1gklpH2bjR0iRL20gJXvMYe.qdXymS'
    hashed_user_bytes = bcrypt.hashpw(input_pwd.encode('utf-8'), stored_hashed_constant)
    return hashed_user_bytes.decode('utf-8')


def get_random_string():
    """
        generate a random string
    """
    uid = uuid.uuid4()
    return uid.hex

# print(hash_password("password"))




