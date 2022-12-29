import { sendOffer } from "./requests"

export async function createoutboundconnection(stream: MediaStream): Promise<RTCPeerConnection> {
    return new Promise((resolve, reject) => {
        console.log("creating outbound connection")
        let peer = new RTCPeerConnection({
            iceServers: [
                {
                    urls: "stun:stun.l.google.com:19302"
                }
            ]
        })
        peer.addTrack((stream.getAudioTracks())[0], stream)

        peer.createOffer().then(offer => {
            peer.setLocalDescription(offer)
        })

        peer.onconnectionstatechange = () => {
            console.log("connection state changed to " + peer.connectionState)
        }


        peer.onicecandidate = async (event) => {
            if (peer.iceGatheringState === "complete") {
                let SDP = peer.localDescription;
                if (SDP !== null) {

                    sendOffer(SDP).then(async answer => {
                        await peer.setRemoteDescription(answer)
                        resolve(peer)
                    });
                }
            }
        };

    });
}