from passlib.context import CryptContext

# bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password ko hash karega
def hash_password(password: str):
    return pwd_context.hash(password)


# Password verify karega
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)