from flask import Flask
from flask import make_response, redirect, request
from requests import Request, post

import dotenv, random, string, os
dotenv.load_dotenv(verbose=True)

app = Flask(__name__)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def generate_state(length=30):
  char = string.ascii_letters + string.digits
  rand = random.SystemRandom()
  return ''.join(rand.choice(char) for _ in range(length))

@app.route("/callback")
def callback():
  args = request.args
  cookies = request.cookies

  if args.get("state") != cookies.get("state"):
    return "State does not match. Possible authorization_code injection attempt", 400

  params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": args.get("code")
  }
  
  access_token = post("https://github.com/login/oauth/access_token",
                      params=params)
  part_of_the_access_token = access_token.text[:24]
  print(part_of_the_access_token, end="...\n")

  return "Authorized in GitHub OAuth Server", 200

@app.route("/")
def index():
  return "<html><a href='/oauth'>Zautoryzuj się w GitHub</a></html>"

@app.route("/oauth")
def authorize_with_github():
  random_state = generate_state()
  params = {
    "client_id": CLIENT_ID,
    "redirect_uri": "http://127.0.0.1:5050/callback",
    "scope": "repo user",
    "state": random_state
  }

  authorize = Request("GET", "https://github.com/login/oauth/authorize",
                      params=params).prepare()

  response = redirect(authorize.url)
  response.set_cookie("state", random_state)
  return response

if __name__ == "__main__":
  app.run("127.0.0.1", 5050)
