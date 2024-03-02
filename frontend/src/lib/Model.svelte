<script lang="ts">
  import { initModel } from "../requests";
  import { connection, updateState } from "../store";
  import AvailableModels from "../models.json";
  import AvailableLangs from "../lang.json";
  import { get } from "svelte/store";

  let tempModel = get(connection).model;
  let tempLang = get(connection).language;

  let userInteracted = false;

  $: shouldFetch = !userInteracted ||
    ($connection.language !== tempLang || $connection.model !== tempModel);

  $: langNotSelectable = tempModel.endsWith(".en");

  async function handleSubmit() {
    let {token} = await initModel({
      user_id: "",
      model: tempModel,
      language: tempLang,
    });
    updateState({token});
  }

  function handleModelChange(event: Event) {
    userInteracted = true;
    tempModel = (event.target as HTMLSelectElement).value;
  }

  function handleLangChange(event: Event) {
    userInteracted = true;
    tempLang = (event.target as HTMLSelectElement).value;
  }
</script>

<main>
  <h2>Model Parameters:</h2>
  <selectionline>
    <label for="model">Model:</label>
    <select name="model" on:change={handleModelChange}>
      {#each AvailableModels as model}
        <option value={model.value} selected={model.value === tempModel}
          >{model.label}</option
        >
      {/each}
    </select>

    <label for="lang">Language:</label>
    <select
      name="lang"
      disabled={langNotSelectable}
      on:change={handleLangChange}
    >
      {#each AvailableLangs as lang}
        <option
          value={lang.value}
          selected={lang.value === (langNotSelectable ? "en" : tempLang)}
          >{lang.label}</option
        >
      {/each}
    </select>

    <label for="temperature">Temperature:</label>
    <input
      type="number"
      name="temperature"
      min="0"
      max="1"
      step="0.1"
      value="0.0"
      disabled
    />

    <button on:click={handleSubmit} disabled={!shouldFetch}>Set</button>
  </selectionline>
</main>

<style>
  main {
    background-color: #00000011;
    padding: 1rem;
    padding-top: 0.2rem;
    border-radius: 0.3rem;
  }

  button:hover {
    background-color: white;
    color: #535bf2;
    cursor: pointer;
  }

  button:disabled {
    background-color: #00000011;
    color: #00000011;
    cursor: not-allowed;
  }

  select {
    border-radius: 0.5rem;
    font-size: large;
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  input {
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    border-radius: 0.5rem;
    font-size: large;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  selectionline {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
    font-weight: 500;
  }

  button {
    background-color: #535bf2;
    color: white;
    font-weight: 600;
  }
</style>
