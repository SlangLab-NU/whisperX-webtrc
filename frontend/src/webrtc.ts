import { sendOffer } from "./requests";

export async function createoutboundconnection(token: string, stream?: MediaStream): Promise<[RTCPeerConnection, RTCDataChannel]> {
    return new Promise((resolve, reject) => {
        console.log("creating outbound connection");
        let peer = new RTCPeerConnection({
            iceServers: [
                {
                    urls: "stun:stun.l.google.com:19302",
                },
            ],
        });

        if (stream !== undefined) {
            peer.addTrack(stream.getAudioTracks()[0], stream);
        }

        let channel = peer.createDataChannel("datachannel", { ordered: true });
        channel.onopen = () => {
            console.log("data channel opened");
        };

        peer.createOffer().then((offer) => {
            peer.setLocalDescription(offer);
        });

        peer.onconnectionstatechange = () => {
            console.log("connection state changed to " + peer.connectionState);
        };

        peer.onicecandidate = async (event) => {
            if (peer.iceGatheringState === "complete") {
                let sdp = peer.localDescription;
                if (sdp !== null) {
                    let answer = await sendOffer(token, sdp.sdp, sdp.type );
                    await peer.setRemoteDescription(answer);
                    resolve([peer, channel]);
                }
            }
        };
    });
}
