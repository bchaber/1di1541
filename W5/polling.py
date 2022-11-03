from flask import Flask
from flask import render_template
from flask import request

from datetime import datetime
from random import randint
from redis import StrictRedis
from time import sleep
from sys import exit

redis_url = "redis://127.0.0.1"
app = Flask(__name__)
app.config["REDIS_URL"] = redis_url
db = StrictRedis.from_url(redis_url, decode_responses=True)

# check if the database is available
try:
  db.echo("ping")
except:
  print("ERROR communicating with Redis database.")
  print("Start Redis instance first. Exiting.")
  exit(1)

from flask import url_for
from flask_sse import sse
app.register_blueprint(sse, url_prefix="/stream")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/sse")
def server_sent_events():
  return render_template("sse.html")

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
      sse.publish(db.get("progress"), type="msg")
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

@app.route("/reset", methods=["POST"])
def reset():
  db.set("progress", "??")
  db.set("status", "idle")
  return "Reset completed"

if __name__ == "__main__":
  app.run("0.0.0.0", port=5050)
