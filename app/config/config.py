import jwt
import datetime
import bcrypt

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/school_db"


# Token encode decode
SECRET_KEY="8f3a9c2e71d4b6f0a8e5c2d9f7b1a4e68c3f9d2a7b5e1c6d8f0a2b4c9e7d3f1e9c3l0e"
ALGORITHM="HS256"

def encode_access_token(id: int, email: str):
    exp = datetime.datetime.now() + datetime.timedelta(hours=24)
    payload = {
        "user_id": id,
        "email" : email,
        "exp" : exp
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return decoded


# Password Hash, Hash verify
def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))