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
      });

      let audio = document.querySelector("audio");
      audio.srcObject = stream;
      webrtc = await createoutboundconnection(stream);

      dataChannel = webrtc.createDataChannel("upstream", { ordered: true });
      dataChannel.onopen = () => {
        console.log("data channel open");
        dataChannel.send("ping");
        dataChannel.onmessage = (event) => {
          console.log("We recieved a message: ", event.data);
        };
      };
      connection.update((state) => ({
        ...state,
        webrtc: true,
      }));
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
  <button on:click={handleStart} class="start">Start</button>
  <button on:click={handleStop} class="stop">Stop</button>
  <audio controls autoplay>
    Your browser does not support the audio element.
  </audio>
</main>

<style>
  main {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .start {
    outline: 2px solid #3fb33f;
  }

  .stop {
    outline: 2px solid #b33f40;
  }
</style>
