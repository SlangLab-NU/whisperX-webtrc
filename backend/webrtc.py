from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRecorder
import uuid, os
import asyncio

pcs = set()

async def offer(sdp, type, filename, on_data_channel_created):
    offer = RTCSessionDescription(sdp, type)
    pc = RTCPeerConnection()
    pc_id = f"PeerConnection({uuid.uuid4()})"
    pcs.add(pc)
    
    @pc.on("datachannel")
    async def on_datachannel(channel):
        on_data_channel_created(channel)
        # Echo message for testing
        @channel.on("message")
        def on_message(message):
            channel.send(message)

    # Prepare local media
    recorder = MediaRecorder(f"data/{filename}")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    async def on_track(track: MediaStreamTrack):
        print(f"Track {track.kind} received, state {track.readyState}")

        if track.kind == "audio":
            recorder.addTrack(track)
            await recorder.start()

        @track.on("ended")
        async def on_ended():
            await recorder.stop()
            os.remove(f"data/{filename}")

    # Handle offer
    await pc.setRemoteDescription(offer)

    # Send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    resp = {
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type,
    }

    return resp
