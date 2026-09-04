import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password.encode(encoding="utf-8"), salt)
    return hashed_password.decode(encoding="utf-8")

def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(encoding="utf-8"), hashed_password.encode(encoding="utf-8"))