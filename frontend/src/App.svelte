<script lang="ts">
  import boltLogo from "./assets/bolt.png";
  import openaiLogo from "./assets/openai.png";
  import Model from "./lib/Model.svelte";
  import Recorder from "./lib/Recorder.svelte";
  import State from "./lib/State.svelte";
</script>

<main>
  <imagediv>
    <img src={openaiLogo} class="logo" alt="Openai Logo" />
    <img src={boltLogo} class="logo boltlogo" alt="Bolt Logo" />
  </imagediv>
  <p class="twitterlink">
    BY: <a href="https://twitter.com/gslaller" target="_blank" rel="noreferrer"
      >twitter:@gslaller</a
    >
  </p>
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
  <p>
    This project is a derivate of the openai's whisper project. The audio chunks
    are transmitted in realtime with webrtc and the model is extended so it can
    cache the previous computed tokens, hence making the application more
    efficient and viable for real time applicationsviable for real time
    inference. Docker image is also available.
  </p>

  <State />

  <Model />
  <Recorder />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    place-items: center center;
    margin: 0 auto;
    max-width: 800px;
    margin-top: 0.2rem;
    height: 100%;
  }

  .twitterlink {
    margin-top: -1.2rem;
  }

  imagediv {
    margin-top: 1rem;
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
  .logo.boltlogo:hover {
    filter: drop-shadow(0 0 2em #5855ffaa);
  }
</style>
