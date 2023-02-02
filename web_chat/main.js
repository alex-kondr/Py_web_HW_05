console.log("Hello world")

const ws = new WebSocket("ws://localhost:8080")

formChat.addEventListener("submit", (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.onopen = (e) => {
    console.log("Hello WebSocket!")
}

ws.onmessage = (e) => {
    text = e.data
    console.log(text)

    if ("1" == "1") {
        text = text + "Hello"
    }

    // const elMsg = document.createElement("div")
    // elMsg.textContent = text
    // subscribe.appendChild(elMsg)
    subscribe.textContent = text
}