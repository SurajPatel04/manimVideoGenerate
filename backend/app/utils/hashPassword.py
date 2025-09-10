from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwdContext.hash(password)

def verifyPassword(plain_password, hash_password):
    return pwdContext.verify(plain_password, hash_password)