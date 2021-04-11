const onSleep = () => {
  socket.emit("action",{
    action: "sleep"
  })
}

const onShutdown = () => {
  socket.emit("action",{
    action: "shutdown"
  })
}

const onGoogleSearch = () => {
  socket.emit("action",{
    action: "googleSearch",
    data: {
      extra: document.getElementById("googleSearch")
    }
  })
}

const onYoutubeSearch = () => {
  socket.emit("action",{
    action: "youtubeSearch",
    data: {
      extra: document.getElementById("youtubeSearch")
    }
  })
}