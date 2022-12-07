<script lang="ts"> // based on https://github.com/vinayakkulkarni/s-offline
  import { offline } from '../store';
  function updateOnlineStatus() {
      offline.set(!navigator.onLine)
  };
</script>
  
<svelte:window
  on:load={updateOnlineStatus}
  on:online={updateOnlineStatus}
  on:offline={updateOnlineStatus}
/>
  
  {#if $offline}
    <slot name="offline"><span class="offline">You're offline</span></slot>
  {:else}
    <slot name="online"><span class="online">You're online</span></slot>
  {/if}

<style>
  .offline { color: rgb(255,62,0) }
  .online  { color: rgb(39, 214, 140) }
</style>