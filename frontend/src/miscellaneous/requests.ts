const URL = "http://localhost:5000"

export async function initModel(obj: { model: string, temperature: number, top_p: number, chunk_size: number }): Promise<void> {
    let response = await fetch(URL + "/initmodel", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(obj),
    })

    let data = await response.json()
    return data.name
}

export async function sendOffer(obj: { offer: RTCSessionDescription }): Promise<RTCSessionDescription> {
    let response = await fetch(URL + "/offer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(obj),
    })
    let data = await response.json() as RTCSessionDescription
    return data
}