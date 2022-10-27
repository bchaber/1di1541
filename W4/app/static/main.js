async function update(response) {
  code = response.status
  text = await response.text()
  output = document.getElementById("output")
  if (!output) {
    output = document.createElement("pre")
    output.setAttribute("id", "output")
    document.body.appendChild(output)
  }
  output.innerHTML = "HTTP/1.1 " + code + "\n" + text
}

window.addEventListener("load", function() {
  console.info("DOM loaded!")

  output = document.createElement("pre")
  authorization = document.getElementById("authorization")
  if (authorization) {
    authorization.addEventListener("change", function() {
      fetch("/staff_only", {headers:{"Authorization":authorization.value}}).
        then((response) => update(response))
    })
  } else {
    console.error("Authorization not found")
  }
})
