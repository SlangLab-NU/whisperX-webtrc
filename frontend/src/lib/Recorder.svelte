<script lang="ts">
  import { connection, updateState } from "../store";
  import { get } from "svelte/store";
  import { createoutboundconnection } from "../webrtc";
  import { ans } from "../store";

  let webrtc: RTCPeerConnection;
  let dataChannel: RTCDataChannel;
  let stream: MediaStream;
  let recordingStartTime: Date | null = null;
  let elapsedTime: string = '00:00';

  async function handleStart() {
    if (get(connection).backendAvailable) {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      [webrtc, dataChannel] = await createoutboundconnection(
        get(connection).token,
        stream,
      );

      dataChannel.onopen = () => {
        dataChannel.onmessage = (event) => {
          console.log("We received a message: ", event.data);
          const messageObject = JSON.parse(event.data);
          const threshold = 0.5;

          ans.update((currentMessages) => {
            if (currentMessages.length > 0) {
              const lastCurrentMessage =
                currentMessages[currentMessages.length - 1];

              if (
                Math.abs(messageObject.start - lastCurrentMessage.start) <
                threshold
              ) {
                // Consider the messages the same if they start within the threshold
                return [...currentMessages.slice(0, -1), messageObject];
              } else if (messageObject.start < lastCurrentMessage.start) {
                // Discard the messageObject if it starts earlier than the last current message
                return currentMessages;
              }
            }
            // Add the new message if there are no previous messages or if it starts later
            return [...currentMessages, messageObject];
          });
        };
      };
      updateState({ webrtc: true });
      recordingStartTime = new Date();
      updateElapsedTime();
    }
  }

  function handleStop() {
    webrtc.close();
    stream.getTracks().forEach((track) => track.stop());
    ans.set([]);
    recordingStartTime = null;
    elapsedTime = '00:00';
  }

  function updateElapsedTime() {
    if (recordingStartTime) {
      const now = new Date();
      const diff = now.getTime() - recordingStartTime.getTime();
      const seconds = Math.floor(diff / 1000) % 60;
      const minutes = Math.floor(diff / 60000);
      elapsedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      setTimeout(updateElapsedTime, 1000);
    }
  }
</script>

<main>
  <subline>
    <button on:click={handleStart} class="start" disabled={$connection.token === ''}>Start</button>
    <button on:click={handleStop} class="stop" disabled={$connection.token === ''}>Stop</button>
    <span>{elapsedTime}</span>
  </subline>
</main>


<!-- <Developer /> -->

<style>
  main {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    margin-top: 1rem;
    width: 100%;
    background-color: #00000011;
    padding: 0.3rem;
    border-radius: 0.3rem;
  }

  button {
    background-color: white;
  }

  subline {
    display: flex;
    flex-direction: row;
    gap: 1rem;
  }

  .start {
    outline: 2px solid #3fb33f;
  }

  .stop {
    outline: 2px solid #b33f40;
  }
</style>
