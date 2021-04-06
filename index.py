import socketio
import threading
import os
from aiohttp import web
from wakeonlan import send_magic_packet

def init():
  initializeSocketServer()

def initializeSocketServer():
  sio = socketio.AsyncServer(cors_allowed_origins="*")
  app = web.Application()
  sio.attach(app)

  @sio.event
  async def connect(sid, environ):
    print("connect ", sid)

  @sio.event
  async def message(sid, data):
    global client_sio
    client_sio.emit("action", {"action": "sleep"})
  
  @sio.event
  async def on_devices(sid, data):
    output = runCmd("arp -a")
    await sio.emit("avail_devices", output)
    
  @sio.event
  async def on_magic_packet(sid, data):
    return send_magic_packet(data["mac_addr"])

  @sio.event
  async def disconnect(sid):
    print('disconnect ', sid)

  if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8081)

def runCmd(cmd):
  stream = os.popen(cmd)
  output = stream.read()
  return output

def runInThread(cb, _args):
  thr = threading.Thread(target=cb, args=_args)
  thr.start()

init()