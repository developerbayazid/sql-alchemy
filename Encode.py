import jwt
import datetime
from Config import ALGORITHM, SECRET_KEY

# Header # Payload # Signature

Payload = {
    "id" : 1,
    "name" : "Bayazid Hasan",
    "email" : "bayazid.freelancer@gmail.com",
    "iss" : "bayazidhasan.com",
    "iat" : datetime.datetime.now(datetime.timezone.utc),
    "exp" : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
}

token = jwt.encode(Payload, SECRET_KEY, algorithm=ALGORITHM)