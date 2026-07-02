from app.extensions import bcrypt


def hash_password(plain_password: str) -> str:
    return bcrypt.generate_password_hash(plain_password).decode("utf-8")


def verify_password(password_hash: str, plain_password: str) -> bool:
    return bcrypt.check_password_hash(password_hash, plain_password)
