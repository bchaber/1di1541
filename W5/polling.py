from flask import Flask
from flask import make_response, render_template
from flask import request

from datetime import datetime
from random import randint
from redis import StrictRedis
from time import sleep
from sys import exit

app = Flask(__name__)
db = StrictRedis("127.0.0.1", decode_responses=True)

# check if the database is available
try:
  db.echo("ping")
except:
  print("ERROR communicating with Redis database.")
  print("Start Redis instance first. Exiting.")
  exit(1)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/job", methods=["POST"])
def job():
  if db.get("status") == "busy":
    return "Busy!", 200

  workload = request.form.get("workload", "10")
  try:
    w = int(workload)
    w = 1 if w < 0 else w
    t = 0

    db.set("status", "busy")

    while t < w:
      sleep(randint(1, 3))
      t += 1
      db.set("progress", int(100 * t/w))
    db.set("status", "idle")

  except:
    return "Error while processing the job", 400

  timestamp = datetime.now().strftime("%H:%M:%S")
  return "[" + timestamp + "] Done!"

@app.route("/check")
def check():
  mode  = request.args.get("mode", "ajax")
  state = request.args.get("state", "0")

  if mode == "ajax":
    status = db.get("status") or "idle"
    progress = db.get("progress") or "??"
    return progress

  if mode == "long":
    status = db.get("status") or "idle"
    progress = db.get("progress") or "0"
    try:
      while progress == state:
        sleep(1)
        progress = db.get("progress") or "0"
      return progress
    except:
      return "Error while checking progress", 400

  return "Unknown mode " + mode, 400

if __name__ == "__main__":
  app.run("0.0.0.0", port=5050)
