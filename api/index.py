from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from requests import get, post, head
from dotenv import dotenv_values
from base64 import b64encode
import json

ACCESS_TOKEN = None
REFRESH_TOKEN = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ACCESS_TOKEN
    global REFRESH_TOKEN

    tokens = await create_initial_token()

    ACCESS_TOKEN = tokens["access_token"]
    REFRESH_TOKEN = tokens["refresh_token"]

    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
async def read_root():
    request_url = "https://api.spotify.com/v1/me/player/currently-playing"
    request_headers = { "Authorization": f"Bearer {ACCESS_TOKEN}" }
    data = get(request_url, headers=request_headers)

    if (data.status_code == 200):
        return {
            "data": data.json()
        }
    elif (data.status_code != 200):
        await refresh_token()
    else:
        return {
            "message": "Error!"
        }

async def refresh_token():
    grant_type = "refresh_token"
    client_id = dotenv_values(".env")["client_id"]
    client_secret = dotenv_values(".env")["client_secret"]
    request_url = f"https://accounts.spotify.com/api/token?grant_type={grant_type}&refresh_token={REFRESH_TOKEN}&client_id={client_id}"
    
    credentials = f"{client_id}:{client_secret}"
    credentials_b64 = b64encode(credentials.encode("ascii")).decode("ascii")

    request_headers = { 
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {credentials_b64}" 
    }
    
    data = post(request_url, headers=request_headers)

    if (data.status_code == 200):
        global ACCESS_TOKEN
        ACCESS_TOKEN = data.json()["access_token"]

    return None

async def create_initial_token():
    callback_uri = "https://accounts.spotify.com/api/token"
    grant_type = "authorization_code"
    client_id = dotenv_values(".env")["client_id"]
    initial_code = dotenv_values(".env")["initial_code"]
    redirect_uri = dotenv_values(".env")["redirect_uri"]
    client_secret = dotenv_values(".env")["client_secret"]
    code_verifier = "code"
    
    url = f"{callback_uri}?client_id={client_id}&grant_type={grant_type}&code={initial_code}&redirect_uri={redirect_uri}&code_verifier={code_verifier}&client_secret={client_secret}"
    request_headers = { "Content-Type": "application/x-www-form-urlencoded" }
    
    tokens = post(url, headers=request_headers)

    if (tokens.status_code == 200):
        return tokens.json()
    else:
        raise Exception(f"Initial token was not accepted: {tokens.status_code}")