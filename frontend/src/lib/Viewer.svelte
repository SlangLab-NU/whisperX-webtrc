<script lang="ts">
  import { get, writable} from "svelte/store";
  import { infer } from "../requests";
  import { connection } from "../store";
  import {ans} from "../store"


  async function makeInference() {
    let { token } = get(connection);
    if (token) {
      let res = await infer(token);
    }
  }
</script>

<main>
  <button on:click={makeInference}>Make Inference</button>
  <ul>
    {#each $ans as item}
      <li class="grid">
        <span class="start_time">{Math.round(100 * item.start) / 100}</span>
        <span class="end_time">{Math.round(100 * item.end) / 100}</span>
        <span class="text">{item.text}</span>
      </li>
    {/each}
  </ul>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    margin-top: 1rem;
  }

  .grid {
    display: grid;
    grid-template-columns: max-content max-content auto;
    grid-auto-rows: auto;
    width: 100%;
    gap: 0.5rem;
  }

  .start_time {
    grid-column: 1;
  }

  .end_time {
    grid-column: 2;
  }

  .text {
    grid-column: 3;
  }
</style>
