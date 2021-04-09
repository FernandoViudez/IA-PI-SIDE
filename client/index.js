const socket = io("http://localhost:8080")

socket.on("connect", (_client) => {
  console.log("Connected!");
})

socket.on("on-devices", (_data) => {
  console.log(_data);
})

socket.on("device-awaken", (_data) => {
  console.log("Device connected!");
})

// Call this func at init of your app, to get devices connected into your program
const getDevices = () => {
  socket.emit("get-devices")
}

// Call this function when you device is on, choosing it or after the device wake up
const chooseDevice = (ip_addr) => {
  socket.emit("device-chosen", { ip_addr })
}

// If status is equal to off, then call this func
const wakeDevice = (ip_addr, mac_addr) => {
  socket.emit("wol-device", { mac_addr });
  
  // Initialize client and wait for its connection
  chooseDevice(ip_addr);
}