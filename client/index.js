let socket;

window.onload = () => {
  initializeSockets("http://localhost:8081")
}

const initializeSockets = (host) => {
  socket = io(host);
  subscribeSockets()
}

const subscribeSockets = () => {
  socket.on("connect", () => {
    console.log("Connected!");
  })

  socket.on("message", (data) => {
    console.log("Message from server --> ", data);
  })

  socket.on("avail_devices", async (data) => {
    buildGui(await format_arp(data))
  })

}

const format_arp = async (data) => {
  let pcsArray = []

  let splitted_info = data.split("Tipo")[1]
  let output = splitted_info.split("     din mico")

  for (let [index, item] of output.entries()) {
    if (item.includes("     est tico")) {
      output.splice(index, 1)
    }
  }

  for (let item of output) {
    let ip_addr = item.split("-")[0].slice(0, -2).trim()

    let mac_array = item.split("-")
    mac_array.splice(0, 1);

    let mac_addr = item.split("-")[0].slice(-2) + "-" + mac_array.join("-");
    let status = 'off';

    try {
      await fetch('http://' + ip_addr + ':8080')
      status = 'on'
    } catch (error) {
      status = 'off'
    }

    pcsArray.push({
      status,
      ip_addr,
      mac_addr
    })
  }

  return pcsArray
}

const buildGui = (pcs_array) => {
  for(let _pc of pcs_array) {

    let _tr = document.createElement("tr")

    for(let item of ['status', 'ip_addr', 'mac_addr', '']) {
      let _td = document.createElement("td")
      _td.innerHTML = _pc[item] ? _pc[item] : `<button onclick="choose_device('${_pc["mac_addr"]}', '${_pc["ip_addr"]}', ${(_pc["status"] === 'on')})">Choose</button>`
      
      _tr.append(_td)
    }

    document.getElementById('output').append(_tr)
  }
}

const get_devices = () => {
  document.getElementById('output').innerHTML = `
  <tr>
    <th>Status</th>
    <th>IP</th>
    <th>MAC</th>
    <th>Choose</th>
  </tr>
  `
  socket.emit("on_devices", {})
}

const choose_device = (mac_addr, ip_addr, connected) => {
  if(connected) {
    // Close current sockets
    socket.close()

    // Connect directly to pc
    initializeSockets(`http://${ip_addr}:8080`)

    // Build GUI for pc
    document.getElementById("wopc").style.display = "none"
    document.getElementById("wpc").style.display = "block"

  } else {
    // Ask for wake on lan the pc
    if(confirm("Do you want to wake up this pc?")) {
      send_magic_packet(mac_addr)
      alert("Turning on your pc... Try on 'get devices' when your pc is on to control it")
    } else return;

  }
}

const send_magic_packet = (mac_addr) => {
  socket.emit("on_magic_packet", {
    mac_addr,
  })
}

const sleep = () => {
  socket.emit("action", {
    action: "sleep"
  })
}