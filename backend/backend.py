from pprint import pprint
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import webrtc
import uvicorn

app = FastAPI()

origins_allowed = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def main():
    return {"ping": "pong"}

@app.post("/initmodel")
async def initmodel(item: dict = Body(...)):
    chunk_size = item["chunk_size"]
    model = item["model"]

    return {"model": model}

@app.post("/offer")
async def offer(item: dict = Body(...)):
    sdp = item["sdp"]
    type = item["type"]
    resp = await webrtc.offer(sdp, type)
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)