from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
import json
import uuid
import os
import inspect
from pprint import pprint

pcs = set()


async def offer(sdp, type):
    offer = RTCSessionDescription(sdp, type)
    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            channel.send(message)

    # prepare local media
    recorder = MediaRecorder("data/webrtc.wav")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    async def on_track(track: MediaStreamTrack):
        pprint(dir(track))
        print("Track %s received, state %s", track.kind, track.readyState)

        if track.kind == "audio":
            recorder.addTrack(track)
            # for i in range(10000):
            #     frame = await track.recv()
            #     x = frame.to_ndarray()


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
