import os
import re
import hal
import jwt

from dotenv import load_dotenv
load_dotenv(verbose=True)

JWT_SECRET = os.getenv("JWT_SECRET")

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import HTTPException
from pydantic import BaseModel


class Patient(BaseModel):
  id: str

class AppointmentRequest(BaseModel):
  patient: Patient

app = FastAPI()
slots = {
  "1234": {"id": "1234", "doctor": "mjones", "start": "1400", "end": "1450"},
  "5678": {"id": "5678", "doctor": "mjones", "start": "1600", "end": "1650"},
}

@app.get("/")
def root():
  content = {}
  hal.add_link(content, "doctor:slots", "/doctors/mjones/slots")
  return content

@app.get("/doctors/{doctor}/slots")
def doctors_slot(doctor: str, date: str, status: str):
  if not re.match("^[a-z]+$", doctor):
    raise HTTPException(status_code=400, detail="invalid doctor name")

  if doctor != "mjones":
    raise HTTPException(status_code=404, detail="doctor not found")

  if status != "open":
    raise HTTPException(status_code=400, detail="you can only search slots with 'open' status")

  content = {}

  slot1 = slots["1234"].copy()
  slot2 = slots["5678"].copy()
  hal.add_link(slot1, "slot:book", "/slots/" + slot1["id"])
  hal.add_link(slot2, "slot:book", "/slots/" + slot2["id"])

  hal.embed(content, "openslots", [slot1, slot2])

  return content

@app.post("/slots/{id}")
def create_slot(id, patient: Patient, response: Response):
  if id not in slots:
    raise HTTPException(status_code=404, detail="slot not found")

  if not re.match("^[a-z]+$", patient.id):
    raise HTTPException(status_code=400, detail="invalid patient id")

  doctor = "mjones"
  date = "20221117"

  slot = slots[id].copy()

  content = slot
  hal.add_link(content, "self", "/slots/" + slot["id"] + "/appointment")
  hal.add_link(content, "help", "/help/appointment")

  location = "/slots/" + slot["id"] + "/appointment"
  hal.add_link(content, "appointment:cancel", location)
  hal.add_link(content, "appointment:addtest", "/slots/" + slot["id"] + "/tests")
  hal.add_link(content, "appointment:changetime", "/doctors/" + doctor + "/slots?date=" + date + "&status=open")
  hal.add_link(content, "appointment:updatecontact", "/patients/" + patient.id + "/contactinfo")

  response.headers["Location"] = location
  response.status_code = 201
  return content

@app.delete("/slots/{id}/appointment")
def cancel_appointment(id: str, request: Request):
  if id not in slots:
    raise HTTPException(status_code=404, detail="slot not found")

  if "Authorization" not in request.headers:
    raise HTTPException(status_code=401, detail="no authorization token provided")

  authorization = request.headers["Authorization"]
  if not authorization.startswith("Bearer "):
    raise HTTPException(status_code=400, detail="invalid authorization data")

  token = authorization[len("Bearer "):]
  try:
    decoded = decode(token, JWT_SECRET, algorithms=["HS256"])
    assert decoded["sub"] == "jsmith"
    return "appointment canceled"
  except:
    raise HTTPException(status_code=403, detail="you are unauthorized to cancel the appointment")
