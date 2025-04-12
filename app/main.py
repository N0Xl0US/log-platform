from fastapi import FastAPI, Request
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import time

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class User(BaseModel):
    username: str
    email: str

@app.get("/")
def root():
    log = {"endpoint": "/", "timestamp": time.time()}
    producer.send("general-logs", log)
    return {"message": "Welcome to the Log Platform"}

@app.post("/login")
def login(user: User):
    log = {"endpoint": "/login", "user": user.username, "timestamp": time.time()}
    producer.send("auth-logs", log)
    return {"status": "success"}

@app.post("/signup")
def signup(user: User):
    log = {"endpoint": "/signup", "user": user.username, "timestamp": time.time()}
    producer.send("auth-logs", log)
    return {"status": "registered"}

@app.get("/data")
def get_data():
    log = {"endpoint": "/data", "timestamp": time.time()}
    producer.send("general-logs", log)
    return {"data": "Sample data"}

@app.put("/profile")
def update_profile(user: User):
    log = {"endpoint": "/profile", "user": user.username, "timestamp": time.time()}
    producer.send("general-logs", log)
    return {"status": "updated"}