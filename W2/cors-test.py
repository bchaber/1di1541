from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
app = Flask(__name__)

@app.route('/', methods=['OPTIONS'])
def options():
    print("[^] Invoked preflight endpoint ")
    response = make_response('', 200)
    response.headers["Access-Control-Allow-Origin"] = "http://friend.company.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('/', methods=['POST'])
def post():
    print("[*] Invoked regular endpoint ")
    response = make_response('{"result":"pong"}', 200)
    response.headers["Access-Control-Allow-Origin"] = "http://friend.company.com"
    return response

@app.route('/', methods=['GET'])
def client():
    return render_template("client.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
