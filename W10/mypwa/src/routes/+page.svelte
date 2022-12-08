<script>
	import Counter from '../lib/Counter.svelte'
	import Offline from '../lib/Offline.svelte'
	import Tasks from '../lib/Tasks.svelte'
  
	import { onMount } from 'svelte';
	import { user, token } from '../store';
	import { authenticated, authorized } from '../store';
	import auth from '../auth_service';
  
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
<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<div class="card">
  <Counter />
</div>

<div class="user">
  <Offline />
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
