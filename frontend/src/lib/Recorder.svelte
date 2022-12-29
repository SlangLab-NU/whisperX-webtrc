<script lang="ts">
  import { connection } from "../store";
  import { get } from "svelte/store";
  import { createoutboundconnection } from "../webrtc";

  let webrtc: RTCPeerConnection;
  let dataChannel: RTCDataChannel;
  let stream: MediaStream;

  async function handleStart() {
    let { backendAvailable, modelset } = get(connection);

    if (backendAvailable && modelset !== "") {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false,
      });

      let audio = document.querySelector("audio");
      audio.srcObject = stream;
      [webrtc, dataChannel] = await createoutboundconnection(stream);
    }
  }

  function handleStop() {
    webrtc.close();
    stream.getTracks().forEach((track) => track.stop());
    let audio = document.querySelector("audio");
    audio.srcObject = null;
  }
</script>

<main>
  <button on:click={handleStart}>Start</button>
  <button on:click={handleStop}>Stop</button>
  <audio controls autoplay>
    Your browser does not support the audio element.
  </audio>
</main>

<style>
  main {
    color: red;
  }
</style>
