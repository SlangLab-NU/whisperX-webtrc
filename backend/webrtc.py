from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
import json
import uuid
import os

pcs = set()

async def offer(sdp, type):
    offer = RTCSessionDescription(sdp, type)

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)


    # prepare local media
    recorder = MediaRecorder(os.path.join(os.getcwd(), "demo-instruct.wav"))

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("datachannel")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        print("Track %s received", track.kind)

        if track.kind == "audio":
            recorder.addTrack(track)

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    resp =  {
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type,
    }

    return resp
