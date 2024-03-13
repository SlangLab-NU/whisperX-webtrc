import json
import sys
import time
from fastapi import FastAPI, APIRouter, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import whisper_online
import webrtc
import uvicorn
import asyncio

app = FastAPI()
router = APIRouter(prefix="/transcription")

origins_allowed = ["*"]

with open("authorized_users.txt", "r") as file:
    AUTHORIZED_USERS = set(file.read().splitlines())

sessions = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/ping")
async def ping():
    return {"ping": "pong"}

@router.post("/init")
async def init(item: dict = Body(...)):
    user_id = item["user_id"]
    model = item["model"]
    language = item.get("language", "en") 

    if user_id not in AUTHORIZED_USERS:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        asr = whisper_online.FasterWhisperASR(model_name=model)
        asr.use_vad()
        online = whisper_online.OnlineASRProcessor(asr=asr, tokenizer=None, 
                                                   logfile=sys.stderr,
                                                   buffer_trimming=("segment", 15))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Failed to load model: {str(e)}")

    token = str(uuid4())
    sessions[token] = {
        "user_id": user_id,
        "model": model,
        "language": language,
        "filename": f"{token}.wav",
        "model_instance": online,
        "latest_transcription_time": 0,
        "job": False
    }
    return {"token": token}

@router.post("/offer")
async def offer(item: dict = Body(...)):
    token = item["token"]
    sdp = item["sdp"]
    type = item["type"]
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[token]
    # Define the callback function
    def on_data_channel_created(channel):
        session["webrtcdatachannel"] = channel
    resp = await webrtc.offer(sdp, type, session["filename"], on_data_channel_created)
    return resp

async def transcribe(token: str):
    session = sessions[token]
    def on_message(o):
        if o[0] is not None:
            message = {"start": o[0], "end": o[1], "text": o[2]}
        else:
            message = str(o)
        session["webrtcdatachannel"].send(json.dumps(message))
    # I do not get this time calculation, just got it from whisper-online
    min_chunk = 1.0
    beg = 0
    start = time.time()-beg
    end = 0
    while session["webrtcdatachannel"] and session["webrtcdatachannel"].readyState == "open":
        if session["latest_transcription_time"] > 3600:
            break
        now = time.time() - start
        if now < end+min_chunk:
            time.sleep(min_chunk+end-now)
        end = time.time() - start
        print("load", beg, end)
        a = whisper_online.load_audio_chunk("data/"+session["filename"],beg,end)
        session["model_instance"].insert_audio_chunk(a)
        try:
            o = session["model_instance"].process_iter()
        except AssertionError:
            print("assertion error",file=sys.stderr)
            pass
        else:
            print(o)
            on_message(o)
    
    session["model_instance"].finish()
    session["job"] = False
    session["latest_transcription_time"] = 0


@router.post("/infer")
async def infer(item: dict = Body(...)):
    token = item["token"]
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    if sessions[token]["job"]:
        raise HTTPException(status_code=409, detail="Job Already Exist")
    else:
        sessions[token]["job"] = True
    asyncio.create_task(transcribe(token))
    return {"message": "Transcription started"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
