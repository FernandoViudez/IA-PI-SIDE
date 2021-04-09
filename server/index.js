const _config = require("./config/config.json")
const _app = require("express")();
const httpServer = require("http").Server(_app);
const cors = require("cors");
const { Logger } = require("./_utils/logger")

_app.use(cors())

httpServer.listen(process.env.PORT || _config.DEFAULT_SERVER_PORT, () => {
  Logger.log(`Server listening on port ${process.env.PORT || _config.DEFAULT_SERVER_PORT}`);
  
  // Require main module
  require('./controllers/main/main');

})

module.exports = {
  _app,
  httpServer,
}