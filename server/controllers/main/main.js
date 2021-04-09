const { Logger } = require("../../_utils/logger");
const { Build } = require("../../_utils/build");
const { Sockets } = require("../socket/socket");
const { Cmd } = require("../cmd/cmd");

const Main = {}
let INITIALIZED = false;

Main._initialize = () => {
  if (INITIALIZED) {
    Logger.warn("Main already initialized. Ignoring...");
    return;
  }

  INITIALIZED = true;

  //Initialize Cmd
  Cmd.initialize()

  //Initialize build
  Build.initialize() // Runs only when param build is provided

  // Initialize sockets
  Sockets.initialize()
}

Main._initialize()