<script>
  import { tasks } from "../store";
  export let task = {};

  let checked;

  function taskDone() {
    console.log(checked);

    let updatedTasks = $tasks.map((currentTask) => {
      if (currentTask.id === task.id) {
        currentTask.completed = checked;
        return currentTask;
      }
      return currentTask;
    });

    tasks.set(updatedTasks);
  }
</script>

<main>
  <li><input type="checkbox" bind:checked={checked} on:change={taskDone} />
    <span class:completed={task.completed}>{task.description}</span>
  </li>
</main>
