<script>
  import svelteLogo from './assets/svelte.svg'
  import Counter from './lib/Counter.svelte'
  import Task from './lib/Task.svelte'

  import { onMount } from 'svelte';
  import { authenticated, user, token } from './store';
  import { tasks, user_tasks } from './store';
  import auth from './auth_service';

  let client;
  let newTask;

  onMount(async () => {
    client = await auth.createClient();
    authenticated.set(await client.isAuthenticated());
    user.set(await client.getUser());
    console.log($user)
  });

  function authorize() { auth.authorizeWithPopup(client); console.log($token) }
  function login() { auth.loginWithPopup(client); console.log($user) }
  function logout() { auth.logout(client); }

  function addItem() {
    let updatedTasks = [...$tasks, {
      id: randomString(),
      description: newTask,
      completed: false,
      user: $user.email
    }]

    tasks.set(updatedTasks);
    newTask = "";
  }

  function randomString(length = 7) {
    var chars =
      "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var result = "";
    for (var i = length; i > 0; --i)
      result += chars[Math.round(Math.random() * (chars.length - 1))];
    return result;
  }
</script>

<main>
  <div>
    <a href="https://vitejs.dev" target="_blank" rel="noreferrer"> 
      <img src="/vite.svg" class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer"> 
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div>
  <h1>Vite &lt;3 Svelte</h1>

  <div class="card">
    <Counter />
  </div>

  <div class="user">
    <button>Toggle</button>

    {#if $authenticated}
      <span>&nbsp;&nbsp;{$user.name} ({$user.email})</span>
    {:else}
      <span>&nbsp;</span>
    {/if}

    {#if $authenticated}
      <a href="/#" on:click="{authorize}">Authorize</a>
      <a href="/#" on:click="{logout}">Log out</a>
    {:else}
      <a href="/#" on:click="{login}">Log in</a>
    {/if}
  </div>

  <div class="tasks">
    {#if $authenticated}
      <ul>
      {#each $user_tasks as item (item.id)}
        <Task task="{item}" />
      {/each}
      </ul>
      <input bind:value="{newTask}" placeholder="Enter New Task"/>
      <button on:click="{addItem}">Add Task</button>
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
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
