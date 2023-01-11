import hashlib

PASSWORD_SALT = "jsjs7lso!!@00%Z"


def hash_password(password: str) -> str:
    hashed_password = hashlib.md5(f"{password}{PASSWORD_SALT}".encode('utf-8')).hexdigest()
    return hashed_password
