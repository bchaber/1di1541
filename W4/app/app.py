from os import getenv
from jwt import decode
from base64 import b64decode

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

from dotenv import load_dotenv
load_dotenv(verbose=True)

JWT_SECRET = getenv("JWT_SECRET")
SECRET_CREDENTIALS = getenv("SECRET_CREDENTIALS")

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

def valid_token(authorization):
  token = authorization[len("Bearer "):]
  try:
    decoded = decode(token, JWT_SECRET, algorithms=["HS256"])
    return decoded["user"] == "lelum"
  except:
    return False

def valid_creds(authorization):
  credentials = authorization[len("Basic "):]
  decoded = b64decode(credentials).decode("utf-8")
  return decoded == SECRET_CREDENTIALS

@app.route("/staff_only")
def staff_only():
  authorization = request.headers.get("Authorization", "")
  if authorization.startswith("Basic "):
    if valid_creds(authorization):
      return "Authorized using BASIC"
  if authorization.startswith("Bearer "):
    if valid_token(authorization):
      return "Authorized using TOKEN"
  return "Get out!", 401
