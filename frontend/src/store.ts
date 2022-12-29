import { writable, derived } from 'svelte/store'
import { ping } from './requests'
import type { ECDHKeyFormat } from 'crypto';

// create enum in typescript
export const AvailableModels = [
    { value: "tiny", label: "Tiny" },
    { value: "tiny.en", label: "Tiny English" },
    { value: "base", label: "Base" },
    { value: "base.en", label: "Base English" },
    { value: "small", label: "Small" },
    { value: "small.en", label: "Small English" },
    { value: "medium", label: "Medium" },
    { value: "medium.en", label: "Medium English" },
    { value: "large", label: "Large" },
];

export const connection = writable<{
    backendAvailable: boolean,
    modelset: string,
    webrtc: boolean,
}>({
    backendAvailable: false,
    modelset: "",
    webrtc: false,
});


let call = () => setTimeout(() => {
    ping().then((res) => {
        if (res) {
            connection.update((value) => ({ ...value, backendAvailable: true }));
        } else {
            call()
        }
    })
}, 1000)
call();


