<script>
	import { stores } from '@sapper/app';
	const { preloading, page, session } = stores();
  import { tasks } from '../store';
  import { token } from '../store';
  import { user }  from '../store';
  import { authorized } from '../store';

  let newTaskDescription;

  token.subscribe(value => {
    if (value) {
      fetch("http://localhost:3001/tasks", {
        method: "GET",
        headers: {
          'Authorization': 'Bearer ' + $token,
          'Content-Type': 'application/json'
        }
      })
      .then((response) => response.json())
      .then((data) => tasks.set(data));
    }
  });

  function checkTask(task) {
    let updatedTasks = $tasks.map((currentTask) => {
      if (currentTask.id === task.id) {
        currentTask.completed = task.checked;
        return currentTask;
      }
      return currentTask;
    });

    tasks.set(updatedTasks);
  }

  function addTask() {
    let newTask = {
      id: randomString(),
      description: newTaskDescription,
      completed: false,
      user: $user.email
    }

    let updatedTasks = [...$tasks, newTask]

    fetch("http://localhost:3001/tasks", {
      method: "POST",
      headers: {
        'Authorization': 'Bearer ' + $token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newTask)
    })
    tasks.set(updatedTasks);
    newTaskDescription = "";
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
  <ul>
    {#each $tasks as task (task.id)}
    <li>
      <input type="checkbox" bind:checked={task.checked} on:change={() => checkTask(task)} />
      <span class:completed={task.completed}>{task.description}</span>
    </li>
    {/each}
    </ul>
  
    <input bind:value="{newTaskDescription}" placeholder="Enter New Task"/>
    <button on:click="{addTask}" disabled="{$authorized === false}">Add Task</button>
</main>

<style>
  ul li { font-size: larger; list-style: none }
  input { font-size: larger }
</style>