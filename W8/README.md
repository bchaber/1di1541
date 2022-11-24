# Application for authorization with GitHub OAuth server

You have to register your client application in GitHub (login and go to Settings > Developer Settings > OAuth Apps). Set Authorization callback URL to "http://127.0.0.1:5050/callback".
Store CLIENT_ID and CLIENT_SECRET in `.env` in the directory with `gh.py`.
Run the client application with `$ python3 gh.py` and visit http://127.0.0.1:5050/.
After clicking the only link on the page you will be redirected to GitHub for authentication. You can modify "scope" in `authorize_with_github` function to see what permissions you will acquire.
