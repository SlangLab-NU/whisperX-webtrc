const URL = `/api`;

export async function initModel(obj: { user_id: string, model: string, language: string }): Promise<{ token: string }> {
    let response = await fetch(URL + "/init", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(obj),
    })

    let data = await response.json() as { token: string }
    return data;
}

export async function sendOffer(token: string, sdp: string, type: string): Promise<RTCSessionDescription> {
    let response = await fetch(URL + "/offer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ token, sdp, type }),
    })
    let data = await response.json() as RTCSessionDescription
    return data
}

export async function ping(): Promise<boolean> {
    let response = await fetch(URL + "/ping")
    let data = await response.json()
    if (data.ping === "pong") {
        return true
    }
    return false
}

type Segment = {
    avg_logprob: number,
    compression_ratio: number,
    end: number,
    id: number,
    no_speech_prob: number,
    seek: number,
    start: number,
    temperature: number,
    text: string,
    tokens: Array<number>,
}

export async function infer(token: string): Promise<Array<Segment>> {
    let response = await fetch(URL + "/infer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
    })

    let data = await response.json() as Array<Segment>
    return data
}
