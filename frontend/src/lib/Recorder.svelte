<script lang="ts">
  import { connection, updateState } from "../store";
  import { get } from "svelte/store";
  import { createoutboundconnection } from "../webrtc";
  import { upload } from "../requests";
  import Developer from "./Developer.svelte";

  let webrtc: RTCPeerConnection;
  let dataChannel: RTCDataChannel;
  let stream: MediaStream;

  async function handleStart() {
    if (get(connection).backendAvailable) {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      let audio = document.querySelector("audio");
      audio.srcObject = stream;
      [webrtc, dataChannel] = await createoutboundconnection(stream);

      //dataChannel = webrtc.createDataChannel("upstream", { ordered: true });
      dataChannel.onopen = () => {
        dataChannel.onmessage = (event) => {
          console.log("We recieved a message: ", event.data);
        };
      };
      updateState({ webrtc: true });
    }
  }

  let filename: string;

  function handleStop() {
    webrtc.close();
    stream.getTracks().forEach((track) => track.stop());
    let audio = document.querySelector("audio");
    audio.srcObject = null;
  }

  async function handleDrop(event: DragEvent) {
    event.preventDefault();
    let file = event.dataTransfer.files[0];
    filename = await upload(file);
    updateState({ filename });
  }

  let content: "File" | "Mic" = "Mic";
</script>

<main>
  <button
    class={content === "File" ? "outline" : ""}
    on:click={() => (content = "File")}>Upload File</button
  >
  <content>
    {#if content === "File"}
      <dropzone
        on:drop={handleDrop}
        on:dragstart|preventDefault={() => {}}
        on:dragover|preventDefault={() => {}}
      >
        {#if filename}
          {filename}
        {:else}
          Drop a file here
        {/if}
      </dropzone>
    {:else}
      <subline>
        <button on:click={handleStart} class="start">Start</button>
        <button on:click={handleStop} class="stop">Stop</button>
        <audio controls autoplay>
          Your browser does not support the audio element.
        </audio>
      </subline>
    {/if}
  </content>
  <button
    class={content === "Mic" ? "outline" : ""}
    on:click={() => (content = "Mic")}>Microphone</button
  >
</main>
<Developer />

<style>
  main {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    margin-top: 1rem;
    width: 100%;
    background-color: #00000011;
    padding: 0.3rem;
    border-radius: 0.3rem;
  }

  button {
    background-color: white;
  }

  content {
    flex-grow: 1;
    border-radius: 0.5rem;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
  }

  .outline {
    outline: 2px solid #3f3fb3;
  }

  dropzone {
    outline: 2px dashed #3f3fb3;
    padding: 1rem;
    width: 100%;
    border-radius: 0.5rem;
    text-align: center;
  }

  subline {
    display: flex;
    flex-direction: row;
    gap: 1rem;
  }

  .start {
    outline: 2px solid #3fb33f;
  }

  .stop {
    outline: 2px solid #b33f40;
  }
</style>
