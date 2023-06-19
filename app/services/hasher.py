from passlib.hash import bcrypt

hasher = bcrypt


def hash_password(pws: str) -> str:
    return hasher.hash(pws)


def verify_password(psw, hash_psw) -> bool:
    return hasher.verify(psw, hash_psw)

