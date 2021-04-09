const { Cmd } = require("../controllers/cmd/cmd");
const path = require("path");
const replace = require('replace-in-file')

const Build = {}

Build.initialize = () => {
  //Check process.argv param
  if (process.argv[2] !== 'build') return;

  // Get ipv4 & replace in file
  Build.getHost()
}

Build.getHost = () => {
  Cmd.execute("ipconfig")
  .then(async res => {
    //Get ipv4
    let _indexStr = res.indexOf("IPv4. . . . . . . . . . . . . . : ") + 1;
    let _lastIndex = res.indexOf("M�scara de subred");
    const firsPartIndex = _indexStr + 32;
  
    const ipv4 = res.slice(firsPartIndex, _lastIndex).trim();
  
    await Build.replaceInFile("0.0.0.0", ipv4, "./process.json");
    
    //Build path
    const pathToRoot = path.join(__dirname, '../')
    Cmd.execute(`cd "${pathToRoot}" & pm2 start process.json`)
    .then(res => {
      process.exit(0)
    })
    
  })
}

Build.replaceInFile = async (_strToReplace, _newStr, _fileLocation) => {
  await replace({
    files: _fileLocation,
    from: _strToReplace,
    to: _newStr
  })
}

module.exports = {
  Build
}