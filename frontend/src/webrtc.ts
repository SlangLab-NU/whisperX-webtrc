import { sendOffer } from "./requests"

export async function createoutboundconnection(stream: MediaStream): Promise<[RTCPeerConnection, RTCDataChannel]> {
    let peer = new RTCPeerConnection({
        iceServers: [
            {
                urls: "stun:stun.l.google.com:19302"
            }
        ]
    })
    peer.addTrack((stream.getAudioTracks())[0], stream)
    let channel = peer.createDataChannel("datachannel")

    peer.createOffer().then(offer => {
        peer.setLocalDescription(offer)

    })

    peer.onconnectionstatechange = () => {
        console.log("connection state changed to " + peer.connectionState)
    }


    peer.onicecandidate = (event) => {
        if (event.candidate) {
            let SDP = peer.localDescription;
            if (SDP !== null) {

                sendOffer(SDP).then(answer => {
                    peer.setRemoteDescription(answer)
                });
            }
        }
    };

    return [peer, channel]
}