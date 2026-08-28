from fastapi import FastAPI, HTTPException
from Encode import token
from Decode import plain_text

app = FastAPI()


@app.get('/hello')
async def hello():
    return{
        "message" : "Hello"
    }



@app.get('/encrypt')
async def encrypt():
    return{
        "token" : token
    }

@app.get('/decrypt')
async def decrypt():
    return{
        "token" : token,
        "plain_text" : plain_text
    }