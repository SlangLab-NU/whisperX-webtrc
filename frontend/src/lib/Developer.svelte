<script lang="ts">
  import { createoutboundconnection } from "../webrtc";

  let msg = "";

  let webrtc: RTCPeerConnection;
  let dataChannel: RTCDataChannel;

  async function createConnection() {
    [webrtc, dataChannel] = await createoutboundconnection();
  }

  function handleSubmit() {
    dataChannel.send(msg);
    msg = "";
  }
</script>

<developer>
  <h1>Developer</h1>
  <input type="text" placeholder="message to the backend" bind:value={msg} />
  <button on:click={handleSubmit}>Submit</button>
  <button on:click={createConnection}>Create Connection</button>
  <p>When you are done, click the "Next" button.</p>
</developer>

<style>
  developer {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
    width: 100%;
    background-color: #00000011;
    padding: 0.3rem;
    border-radius: 0.3rem;
  }
</style>
