function clear_output() {
  output = document.getElementById("output")
  if (output)
    output.innerText = ""
}

async function update(response) {
  code = await response.status
  text = await response.text()
  output = document.getElementById("output")

  if (!output) {
    output = document.createElement("span")
    output.setAttribute("id", "output")
    document.body.appendChild(output)
  }

  output.innerText = "Current job finished in " + text + "%"

  return (code == 200) ? text : "ERR"
}

async function check_with_ajax_polling() {
  await fetch("/check?mode=ajax")
        .then((response) => update(response));
}

async function check_with_long_polling(state, errors) {
  if (errors < 5) {
  await fetch("/check?mode=long&state=" + state, {signal:window.ctl.signal})
        .then((response) => update(response))
        .then((state)  => { check_with_long_polling(state, errors) })
        .catch((error) => { check_with_long_polling(state, errors + 1) })
  } else {
    console.error("Too many errors")
  }
}


window.addEventListener("load", function() {
  form = document.getElementById("form")
  if (form) {
    form.addEventListener("submit", function(event) {
      event.preventDefault()
      fetch(form.action, {method:"post"})
      .then((response) => response.text())
      .then((text) => console.info(text))
    })
  }

  ajax_polling = document.getElementById("ajax-polling")
  if (ajax_polling) {
    console.info("Ajax polling active");
    ajax_polling.addEventListener("click", function(event) {
      event.preventDefault()
      clear_output()

      if (window.tid) {
        console.info("Stopped interval timer")
        window.clearInterval(window.tid)
        window.tid = undefined
        ajax_polling.innerText = "start"
      } else {
        console.info("Started interval timer")
        window.tid = window.setInterval(check_with_ajax_polling, 500)
        ajax_polling.innerText = "stop"
      }
    })
  }

  long_polling = document.getElementById("long-polling")
  if (long_polling) {
    console.info("Long polling active");
    long_polling.addEventListener("click", function(event) {
      event.preventDefault()
      clear_output()

      if (window.ctl && window.ctl.signal.aborted == false) {
        console.info("Stopped infinite request loop")
        window.ctl.abort()
        long_polling.innerText = "start"
      } else {
        console.info("Started infinite request loop")
        window.ctl = new AbortController()
        check_with_long_polling("0", 0)
        long_polling.innerText = "stop"
      }
    })
  }
})
