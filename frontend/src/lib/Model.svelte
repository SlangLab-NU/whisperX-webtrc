<script lang="ts">
  import { initModel } from "../requests";
  import { AvailableModels, connection } from "../store";

  async function handleClick() {
    const model =
      document.querySelector<HTMLSelectElement>("select[name=model]").value;

    let ans = await initModel({ model });
    connection.update((state) => ({
      ...state,
      modelset: ans,
    }));
  }
</script>

<main>
  <h2>Model Parameters:</h2>

  <selectionline>
    <label for="model">Model:</label>

    <select name="model">
      {#each AvailableModels as model}
        <option value={model.value} selected={model.value === "base"}
          >{model.label}</option
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

    <button id="start" on:click={handleClick}>Set</button>
  </selectionline>
</main>

<style>
  main {
    background-color: #00000011;
    padding: 1rem;
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

  button:hover {
    background-color: white;
    color: #535bf2;
    cursor: pointer;
  }
</style>
