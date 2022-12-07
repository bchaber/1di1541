<script>
	import Counter from '../components/Counter.svelte'
	import Tasks from '../components/Tasks.svelte'
  
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

<style>
	h1 {
		text-align: center;
		margin: 0 auto;
	}

	h1 {
		font-size: 2.8em;
		text-transform: uppercase;
		font-weight: 700;
		margin: 0 0 0.5em 0;
	}

	@media (min-width: 480px) {
		h1 {
			font-size: 4em;
		}
	}
</style>

<svelte:head>
	<title>Sapper project template</title>
</svelte:head>

<h1>Svelte + Sapper</h1>

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