const URL = "http://localhost:5000"

export async function initModel(obj: { model: string, language: string }): Promise<{ model: string, language: string }> {
    let response = await fetch(URL + "/initmodel", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(obj),
    })

    let data = await response.json() as { model: string, language: string }
    return data;
}

export async function sendOffer(offer: RTCSessionDescription): Promise<RTCSessionDescription> {
    let response = await fetch(URL + "/offer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(offer),
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


export async function upload(file: File): Promise<string> {
    let formData = new FormData()
    formData.append("file", file)

    let response = await fetch(URL + "/upload", {
        method: "POST",
        body: formData,
    })

    let data = await response.json()
    return data.filename
}

type segment = {
    'avg_logprob': number,
    'compression_ratio': number,
    'end': number,
    'id': number,
    'no_speech_prob': number,
    'seek': number,
    'start': number,
    'temperature': number,
    'text': string,
    'tokens': Array<number>,
}

export async function infer(filename: string): Promise<Array<segment>> {
    let response = await fetch(URL + "/infer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename }),
    })

    let data = await response.json() as Array<segment>
    return data
}