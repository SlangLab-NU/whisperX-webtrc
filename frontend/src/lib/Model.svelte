<script lang="ts">
  import { initModel } from "../miscellaneous/requests";

  function handleClick() {
    const model =
      document.querySelector<HTMLSelectElement>("select[name=model]").value;
    const temperature = +document.querySelector<HTMLInputElement>(
      "input[name=temperature]"
    ).value;
    const top_p =
      +document.querySelector<HTMLInputElement>("input[name=top_p]").value;
    const chunk_size = +document.querySelector<HTMLInputElement>(
      "input[name=chunk_size]"
    ).value;

    initModel({ model, temperature, top_p, chunk_size });
  }
</script>

<main>
  <h2>Model Parameters</h2>
  <button id="start" on:click={handleClick}>INIT</button>
  <br />
  <label for="model">Select Model:</label>

  <select name="model">
    <option value="tiny">tiny</option>
    <option value="tiny.en">tiny.en</option>
    <option selected value="base">base</option>
    <option value="base.en">base.en</option>
    <option value="small">small</option>
    <option value="small.en">small.en</option>
    <option value="medium">medium</option>
    <option value="medium.en">medium.en</option>
    <option value="large">large</option>
  </select>

  <label for="temperature">Temperature:</label>
  <input
    type="number"
    name="temperature"
    min="0"
    max="1"
    step="0.1"
    value="0.5"
  />

  <label for="top_p">Top P:</label>
  <input type="number" name="top_p" min="0" max="1" step="0.1" value="0.9" />

  <label for="chunks_size">Chunk Size(ms)</label>
  <input
    type="number"
    name="chunk_size"
    min="50"
    max="1000"
    step="50"
    value="100"
  />
  <br />
</main>

<style>
  select {
    border-radius: 0.5rem;
    font-size: large;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  input {
    border-radius: 0.5rem;
    font-size: large;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
</style>
