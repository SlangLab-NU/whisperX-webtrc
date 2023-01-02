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
      href="https://github.com/gslaller/whisper-webrtc"
      target="_blank"
      rel="noreferrer"
    >
      Bolt
    </a>
    =
    <a
      href="https://github.com/openai/whisper"
      target="_blank"
      rel="noreferrer"
    >
      Whisper
    </a>
    +
    <a href="https://github.com/aiortc/aiortc" target="_blank" rel="noreferrer">
      Webrtc
    </a>
  </h1>
  <details>
    <summary>Overview</summary>
    <p class="padding_left">
      This project is a derivate of the openai's whisper project. The audio
      chunks are transmitted in realtime with webrtc and the model is extended
      so it can cache the previous computed tokens, hence making the application
      more efficient and viable for real time applicationsviable for real time
      inference. Docker image is also available.
    </p>
  </details>

  <Model />
  <Recorder />
  <Viewer />
  <p class="twitterlink">
    <a href="https://twitter.com/gslaller" target="_blank" rel="noreferrer"
      >twitter:@gslaller</a
    >
    {#if !$connection.backendAvailable}
      <span class="red">CANNOT REACH BACKEND</span>
    {/if}
  </p>
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
