let _config = require("../config/config.json")

class Logger {
  _debugMode = false;
  
  constructor({
    debugMode,
  }) {
    this._debugMode = debugMode;
  }

  log(...values) {
    if(!this._debugMode) return;
    console.log(...values);
  }

  warn(...values) {
    if(!this._debugMode) return;
    console.warn(...values);
  }

  error(...values) {
    if(!this._debugMode) return;
    console.error(...values);
  }
}

Logger = new Logger({
  debugMode: _config.USE_CONSOLE
})

module.exports = {
  Logger,
}