const socket = io("http://localhost:8080")

let _int;

socket.on("connect", (_client) => {
  console.log("Connected!");

  getDevices();

  _int = setInterval(() => {
    getDevices()
  }, 30000)

})

socket.on("on-devices", (_data) => {
  console.log(_data);
  buildGUIDevices(_data)
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
  clearInterval(_int)
  buildGUIDeviceSelected()
}

// If status is equal to off, then call this func
const wakeDevice = (ip_addr, mac_addr) => {
  socket.emit("wol-device", { mac_addr });
  
  // Initialize client and wait for its connection
  chooseDevice(ip_addr);
}

const buildGUIDevices = (devices) => {
  let GUI = document.getElementById("gui");

  if(GUI) {
    GUI.innerHTML = "";
  } else {
    GUI = document.createElement("div")
    GUI.id = 'gui';
  }

  const table = document.createElement("table");
  const tr = document.createElement("tr");
  tr.innerHTML = "<th>IP</th><th>MAC</th><th>STATUS</th>"

  table.append(tr)

  for(let device of devices) {
    const _tr = document.createElement("tr");
    _tr.innerHTML = `
    <td>${device.ip}</td>
    <td>${device.mac}</td>
    <td>${device.status}</td>
    <td><button onclick="${
      device.status == 'on' ? 
      'chooseDevice('+ "'" + device.ip + "'" +')' : 
      'wakeDevice('+ "'" + device.mac + "'" +'")'}">${device.status == 'on' ? 'Connect to this device' : 'Turn on by WOL'}</button></td>`
    table.append(_tr);
  }

  GUI.append(table);
  document.body.append(GUI);
}

const buildGUIDeviceSelected = () => {
  let GUI = document.getElementById("gui");

  if(GUI) {
    GUI.innerHTML = "";
  } else {
    GUI = document.createElement("div")
    GUI.id = 'gui';
  }

  // Code your content here

  GUI.innerHTML = `
    <button onclick="onSleep()">Sleep device</buton>
    <button onclick="onShutdown()">Shutdown device</buton>
    
    <br>
    <br>
    
    <input id="googleSearch">
    <button onclick="onGoogleSearch()">Search on google</buton>
    
    <br>
    <br>
    
    <input id="youtubeSearch">
    <button onclick="onYoutubeSearch()">Search on youtube</buton>
    

    <button>TBD</buton>
    <button>TBD</buton>
    <button>TBD</buton>
  `


  GUI.append(table);
  document.body.append(GUI);
}