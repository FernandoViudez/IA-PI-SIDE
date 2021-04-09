const { Logger } = require("../../_utils/logger");
const { httpServer } = require("../../index");
const { Client, _evtEmitter } = require("../client/client");
const io = require('socket.io')(httpServer, { cors: { origin: '*', } });
const _config = require("../../config/config.json");

// External libs
const wol = require("wol")
const localDevices = require("local-devices")
const fetch = require("fetch").fetchUrl;

const Sockets = {};
const _Sockets = {};
_Sockets.socket = undefined;

let INITIALIZED = false;

Sockets.initialize = () => {
  if (INITIALIZED) {
    Logger.warn("Sockets already initialized. Ignoring...");
    return;
  }

  INITIALIZED = true;

  _Sockets.connect()
  _Sockets.listenClientLocalEvents()

  Logger.log('Sockets initialized!')
}

_Sockets.connect = () => {
  io.on('connection', _socket => {
    Logger.log("Client connected!");
    _Sockets.socket = _socket
    _Sockets.listenClientEvents()
  });
}

_Sockets.listenClientEvents = () => {

  // From Angular client, when we need to do something on our computer
  _Sockets.socket.on('action', (_data) => {
    Logger.log("On action data --> " + _data);
    Client.emit('action', _data)
  })

  _Sockets.socket.on('get-devices', (_data) => {
    // Emit devices connected to my router
    localDevices().then(async devices => {
      let _devicesCount = 0;

      // Fetch each one and add status property
      for (let _device of devices) {
        let status = 'off';

        fetch("http://" + _device.ip + ":8080", (error, meta, body) => {
          if(error) {            
            _device.status = status;
          } else {
            status = 'on'
    
            _device.status = status;
          }

          _devicesCount++

          if(devices.length == _devicesCount) {
            _Sockets.socket.emit("on-devices", devices);
          }

        })
      }

    })
  })

  _Sockets.socket.on('device-chosen', (_data) => {
    Logger.log("Device Chosen --> ", _data);

    // Initialize client and connect to this device.
    Client.initialize(_data["ip_addr"])
  })

  _Sockets.socket.on('wol-device', (_data) => {
    Logger.log("Waking on lan device with data --> ", _data);

    // Wake on lan lib
    wol.wake(_data["mac_addr"],
      (err, res) => err ? Logger.error("Errored --> " + err) : Logger.log("Response --> ", res))
  })

  _Sockets.socket.on('disconnect', (_data) => {
    Logger.log("Client got disconnected");
  })
}

_Sockets.listenClientLocalEvents = () => {
  _evtEmitter.on('device_awaken', (_data) => {
    // Repeat to client
    Logger.log("Device Waken emitted!");
    _Sockets.socket.emit('device-awaken', _data);
  })
}

Sockets.emit = (evt_name, data) => {
  _Sockets.socket.emit(evt_name, data);
}

module.exports = {
  Sockets,
  _evtEmitter,
}