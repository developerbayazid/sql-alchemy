import jwt
from Config import ALGORITHM, SECRET_KEY
from Encode import token

plain_text = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)