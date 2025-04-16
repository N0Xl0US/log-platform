from fastapi import FastAPI, Request, HTTPException, Response
from pydantic import BaseModel, EmailStr
from kafka import KafkaProducer
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import json
import time

app = FastAPI()

# Prometheus metrics
REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class User(BaseModel):
    username: str
    email: EmailStr

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    try:
        response = await call_next(request)
        status = str(response.status_code)
        REQUEST_COUNTER.labels(
            method=method,
            endpoint=path,
            status=status
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=path
        ).observe(time.time() - start_time)
        
        return response
    except Exception as e:
        REQUEST_COUNTER.labels(
            method=method,
            endpoint=path,
            status="500"
        ).inc()
        raise

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    log = {"endpoint": "/", "timestamp": time.time()}
    producer.send("general-logs", log)
    return {"message": "Welcome to the Log Platform"}

@app.get("/data")
def get_data():
    log = {"endpoint": "/data", "timestamp": time.time()}
    producer.send("general-logs", log)
    return {"data": "Sample data"}

@app.post("/login")
def login(user: User):
    if not user.username or len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Invalid username")
    
    log = {
        "endpoint": "/login",
        "user": user.username,
        "timestamp": time.time(),
        "status": "success"
    }
    producer.send("auth-logs", log)
    return {"status": "success"}

@app.post("/signup")
def signup(user: User):
    if not user.username or len(user.username) > 50:
        raise HTTPException(status_code=400, detail="Invalid username length")
    
    log = {
        "endpoint": "/signup",
        "user": user.username,
        "timestamp": time.time(),
        "status": "success"
    }
    producer.send("auth-logs", log)
    return {"status": "registered"}

@app.put("/profile")
def update_profile(user: User):
    if not user.username or len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Invalid username")
    
    log = {
        "endpoint": "/profile",
        "user": user.username,
        "timestamp": time.time(),
        "status": "success"
    }
    producer.send("general-logs", log)
    return {"status": "updated"}