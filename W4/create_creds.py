from base64 import b64encode

username = "bartek"
password = "haslo"

credentials = bytes(username + ":" + password, "utf-8")
encoded = b64encode(credentials).decode("utf-8")

print("Authorization: Basic " + encoded)
