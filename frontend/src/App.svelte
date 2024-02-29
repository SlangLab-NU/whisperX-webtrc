<script lang="ts">
  import boltLogo from "./assets/bolt.png";
  import greenBoltLogo from "./assets/bolt-green.png";
  import openaiLogo from "./assets/openai.png";
  import Model from "./lib/Model.svelte";
  import Recorder from "./lib/Recorder.svelte";
  import Viewer from "./lib/Viewer.svelte";
  import { connection } from "./store";
</script>

<main>
  <imagediv>
    <img src={openaiLogo} class="logo" alt="Openai Logo" />
    <img
      src={$connection.backendAvailable ? greenBoltLogo : boltLogo}
      class={"logo boltlogo " +
        ($connection.backendAvailable ? "greenshadow" : "")}
      alt="Bolt Logo"
    />
  </imagediv>

  <h1>
    <a
      href="https://github.com/SlangLab-NU/whisperX-webtrc"
      target="_blank"
      rel="noreferrer"
    >
      BoltX
    </a>
    =
    <a
      href="https://github.com/m-bain/whisperX"
      target="_blank"
      rel="noreferrer"
    >
      WhisperX
    </a>
    +
    <a href="https://github.com/aiortc/aiortc" target="_blank" rel="noreferrer">
      Webrtc
    </a>
  </h1>
  <details>
    <summary>Usage</summary>
    <p class="padding_left">
      This project is an improvement over the original <a href="https://github.com/gslaller/whisper-webrtc">Bolt</a> project. It integrates
      WhisperX and use time stamp and sliding window to achieve real time transcription. To use this app, choose your model parameters and click "Set".
      Open the developer menu, click on start, and wait until "connection state changed to connected" appears in the console. Finally after you are connected click on make 
      inference to start transcription. 
    </p>
  </details>

  <Model />
  <Recorder />
  <Viewer />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    place-items: center center;
    margin: 0 auto;
    max-width: 800px;
    margin-top: 0.2rem;
    min-height: 100vh;
  }

  imagediv {
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    gap: 3rem;
  }

  h1 {
    margin-top: 0rem;
  }

  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #000000aa);
  }

  .greenshadow {
    filter: drop-shadow(0 0 2em #3fb33f);
  }

  .twitterlink {
    position: fixed;
    top: 0px;
    left: 0px;
  }

  details {
    width: 100%;
    margin-bottom: 1rem;
  }
  .padding_left {
    padding-left: 1rem;
    text-align: justify;
  }
  .red {
    color: red;
    font-weight: 500;
  }
</style>
