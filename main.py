from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/hello')
async def hello():
    return{
        "message" : "Hello"
    }

