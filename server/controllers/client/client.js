const io = require("socket.io-client")
const _evtEmitter = new (require('events').EventEmitter)();
const { Logger } = require("../../_utils/logger")

const Client = {}
const _Client = {}

let INITIALIZED = false;

_Client.socket = undefined;
_Client.connected = false

Client.initialize = (ip_addr) => {
  if(INITIALIZED) {
    Logger.warn("Client already initialized. Ignoring...");
    return
  }

  INITIALIZED = true

  _Client.connect(ip_addr)

}

_Client.connect = (ip_addr) => {
  _Client.socket = io("http://" + ip_addr + ":8080")
  _Client.subscribeSockets(ip_addr)
}

_Client.subscribeSockets = (ip_addr) => {
  _Client.socket.on("connect", (_socket) => {
    Logger.log("Connected to remote pc server!");
    _Client.connected = true;

    // Send event to local server
    _evtEmitter.emit('device_awaken', { ip_addr })
  })
}

Client.emit = (event_name, data) => {
  if(!_Client.connected) return;
  _Client.socket.emit(event_name, data)
}

module.exports = { 
  Client,
  _evtEmitter
}