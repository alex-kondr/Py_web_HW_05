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
    jsonTable = JSON.parse(e.data)
    console.log(jsonTable)
    subscribe.textContent = ''

    jsonTable.forEach(function(item) {

        const elMsg = document.createElement("div")
        elMsg.textContent = item
        subscribe.appendChild(elMsg)

    })
}