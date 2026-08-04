from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "taskflow_secret_key"
ALGORITHM = "HS256"


# -------------------------
# CREATE JWT TOKEN
# -------------------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# -------------------------
# VERIFY JWT TOKEN
# -------------------------

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None