import jwt # python3 -m pip install pyjwt

sekret = "to samo co w JWT_SECRET"
dane = {"username":"lelum"}

zeton = jwt.encode(dane, sekret, "HS256")
print("Authorization: Bearer " + zeton)
