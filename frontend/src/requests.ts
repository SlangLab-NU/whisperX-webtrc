const URL = "http://localhost:5000"

export async function initModel(obj: { model: string }): Promise<string> {
    let response = await fetch(URL + "/initmodel", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(obj),
    })

    let data = await response.json()
    return data.model
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
