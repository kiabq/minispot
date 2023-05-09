from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import get, post, head
from dotenv import dotenv_values
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
async def read_root():
    # TODO:
    # - Set access_token and refresh_token after first call
    # using an initial code.
    # - Create a method (or middleware maybe?) that will update the access_token
    # (using the refresh_token) once it has expired
    tokens = await create_initial_token()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    request_url = "https://api.spotify.com/v1/me/player/currently-playing"
    request_headers = { "Authorization": f"Bearer {access_token}" }
    val = get(request_url, headers=request_headers)

    return {
        "message": val.json()
    }

async def refresh_token():
    return None

async def create_initial_token():
    callback_uri = "https://accounts.spotify.com/api/token"
    client_id = dotenv_values(".env")["client_id"]
    grant_type = "authorization_code"
    initial_code = dotenv_values(".env")["initial_code"]
    redirect_uri = dotenv_values(".env")["redirect_uri"]
    code_verifier = "code"
    client_secret = dotenv_values(".env")["client_secret"]

    url = f"{callback_uri}?client_id={client_id}&grant_type={grant_type}&code={initial_code}&redirect_uri={redirect_uri}&code_verifier={code_verifier}&client_secret={client_secret}"
    request_headers = { "Content-Type": "application/x-www-form-urlencoded" }
    
    tokens = post(url, headers=request_headers)

    if (tokens.status_code == 200) :
        return tokens.json()
    else:
        raise Exception(f"Unexpected response from server: {tokens.status_code}")