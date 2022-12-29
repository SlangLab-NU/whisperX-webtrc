<script lang="ts">
  export let msg = "Hello World!";
  export let start = false;

  async function handleStart() {
    // get audio stream from getUserMedia
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: false,
    });

    let audio = document.querySelector("audio");
    audio.srcObject = stream;

    let response = await fetch("http://localhost:5000");
    let text = await response.text();
    alert(text);
  }
</script>

<main>
  {#if start}
    <h1>{msg}</h1>
  {:else}
    <h1>Not started</h1>
  {/if}
  <button on:click={handleStart}>Start</button>
  <audio controls autoplay>
    Your browser does not support the audio element.
  </audio>
</main>

<style>
  main {
    color: red;
  }
</style>
