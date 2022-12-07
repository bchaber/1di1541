<script>
  import Counter from './lib/Counter.svelte'
  import Tasks from './lib/Tasks.svelte'

  import { onMount } from 'svelte';
  import { user, token } from './store';
  import { authenticated, authorized } from './store';
  import auth from './auth_service';

  let client;

  onMount(async () => {
    client = await auth.createClient();
    authenticated.set(await client.isAuthenticated());
    token.set(await client.getTokenSilently({
      authorizationParams: {
        audience: 'http://localhost:3001',
        scope: 'read:tasks write:tasks'
      }
    }));
    authorized.set($token !== undefined);
    user.set(await client.getUser());
  });

  function authorize() { auth.authorizeWithPopup(client) }
  function login() { auth.loginWithPopup(client) }
  function logout() { auth.logout(client); }
</script>

<main>
  <h1>Vite &lt;3 Svelte</h1>

  <div class="card">
    <Counter />
  </div>

  <div class="user">
    {#if $authenticated}
      <span>&nbsp;&nbsp;{$user.name} ({$user.email})</span>
    {:else}
      <span>&nbsp;</span>
    {/if}

    {#if $authenticated}
      {#if $authorized}
        <span>Authorized</span>
      {:else}
        <a href="/#" on:click="{authorize}">Authorize access to API</a>
      {/if}
      <a href="/#" on:click="{logout}">Log out</a>
    {:else}
      <a href="/#" on:click="{login}">Log in</a>
    {/if}
  </div>

  <div class="tasks">
    {#if $authenticated}
      <Tasks/>
    {/if}
  </div>

  <p>
    Check out <a href="https://github.com/sveltejs/kit#readme" target="_blank" rel="noreferrer">SvelteKit</a>, the official Svelte app framework powered by Vite!
  </p>

  <p class="read-the-docs">
    Click on the Vite and Svelte logos to learn more
  </p>
</main>

<style>
  .read-the-docs {
    color: #888;
  }
</style>
