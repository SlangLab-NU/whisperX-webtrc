<script lang="ts">
  import { connection } from "../store";

  $: modelset = $connection.modelset;
  $: webrtc = $connection.webrtc;
  $: backendAvailable = $connection.backendAvailable;
</script>

<main>
  <backend>
    {#if backendAvailable}
      <span class="green">BACKEND ACK</span>
    {:else}
      <span class="red">BACKEND NOT PINGABLE</span>
    {/if}
  </backend>
  <modelset>
    {#if !!modelset}
      <span class="green">MODEL ACK</span>
    {:else}
      <span class="red">MODEL NOT SET</span>
    {/if}
  </modelset>
  <webrtc>
    {#if webrtc}
      <span class="green">WEBRTC ACK</span>
    {:else}
      <span class="red">WEBRTC NOT SET</span>
    {/if}
  </webrtc>
</main>

<style>
  main {
    display: flex;
    height: 2rem;
    gap: 2rem;
  }

  .red {
    color: #b33f40;
    font-weight: 500;
  }

  .green {
    color: #3fb33f;
    font-weight: 500;
  }
</style>
