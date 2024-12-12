from fastapi import FastAPI, APIRouter, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import whisperx
import webrtc
import uvicorn
import asyncio
import aiofiles.os

app = FastAPI()
router = APIRouter(prefix="/transcription")

origins_allowed = ["*"]

with open("authorized_users.txt", "r") as file:
    AUTHORIZED_USERS = set(file.read().splitlines())

device = "cuda"
sessions = {}
# global model
model_instance = None
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
        if not model_instance:
            model_instance = whisperx.load_model(model, device)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load model: {str(e)}")

    token = str(uuid4())
    sessions[token] = {
        "user_id": user_id,
        "model": model,
        "language": language,
        "filename": f"{token}.wav",
        "model_instance": model_instance,
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
    def on_message(message):
        #print(message)
        session["webrtcdatachannel"].send(message)

    while session["webrtcdatachannel"] and session["webrtcdatachannel"].readyState == "open":
        if session["latest_transcription_time"] > 3600:
            break
        result = session["model_instance"].transcribe(
            "data/" + session["filename"],
            language=session["language"],
            webrtcsend_method=on_message,
            start_time = session["latest_transcription_time"]
        )
        if result and len(result['segments']) > 1:
            # Update the session with the latest transcription result
            session["latest_transcription_time"] = result['segments'][-1]["start"]
        await asyncio.sleep(1)
    session["job"] = False
    session["latest_transcription_time"] = 0

async def async_file_exists(path: str) -> bool:
    return await aiofiles.os.path.exists(path)

async def wait_for_file(path: str, timeout: int = 5, interval: int = 1, additional_delay: int = 3):
    """
    Wait for the file to exist up to `timeout` seconds.
    Check every `interval` seconds.
    Once the file exists, wait an additional `additional_delay` seconds.
    """
    total_wait = 0
    while total_wait < timeout:
        if await async_file_exists(path):
            await asyncio.sleep(additional_delay)  # Wait additional seconds after file is detected
            return True
        await asyncio.sleep(interval)
        total_wait += interval
    return False

@router.post("/infer")
async def infer(item: dict = Body(...)):
    token = item["token"]
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if sessions[token].get("job"):
        raise HTTPException(status_code=409, detail="Job Already Exists")

    audio_file_path = f"data/{token}.wav"
    file_ready = await wait_for_file(audio_file_path)
    if not file_ready:
        raise HTTPException(status_code=408, detail="Audio file not ready within expected time")

    sessions[token]["job"] = True
    asyncio.create_task(transcribe(token))
    return {"message": "Transcription started"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
