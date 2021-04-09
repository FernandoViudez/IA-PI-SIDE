const exec = require('child_process').exec;
const { Logger } = require("../../_utils/logger");

const Cmd = {}
const _Cmd = {}

let INITIALIZED = false;

Cmd.initialize = () => {
  if (INITIALIZED) {
    Logger.warn("Cmd walready initialized. Ignoring...");
    return;
  }

  INITIALIZED = true;

  Logger.log('Action initialized!')
}

Cmd.execute = (command) => {
  return new Promise((resolve, reject) => {
    let _response = "empty response";
  
    const _func = (error, stdout, stderr) => {
      if (stdout !== '') {
        Logger.log('---------stdout: ---------\n' + stdout);
        resolve(stdout);
      }
      if (stderr !== '') {
        Logger.log('---------stderr: ---------\n' + stderr);
        resolve(_response);
      }
      if (error !== null) {
        Logger.log('---------exec error: ---------\n[' + error + ']');
        resolve(_response);
      }
    }
  
    exec(command, _func);
  });
}

module.exports = {
  Cmd
}