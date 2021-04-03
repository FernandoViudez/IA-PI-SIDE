from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from gtts import gTTS
from pathlib import Path
from ctypes import windll
from aiohttp import web
import os
import webbrowser
import socketio

# Global vars
silence = False
sio = False
chatbot = False
trainer = False
last_input_user = False
shootWord = False
levenshtein_distance = False

def init():
  initializeIA()
  initializeSockets()

def initializeSockets():
  global sio

  sio = socketio.AsyncServer(cors_allowed_origins="*")
  app = web.Application()
  sio.attach(app)

  @sio.event
  async def connect(sid, environ):
    print("connect ", sid)
    await sayToClient('Hola Fernando, ¿como estás?')

  @sio.event
  async def on_client_message(sid, msj):
    print("message from client --> ", msj)
    await sayToIA(msj)

  @sio.event
  async def disconnect(sid):
    print('disconnect ', sid)

  if __name__ == '__main__':
    web.run_app(app, host="localhost", port=8081)

def initializeIA():
  global chatbot
  global trainer
  global last_input_user
  global shootWord
  global levenshtein_distance

  chatbot = ChatBot(
    'Vision',
  )

  trainer = ListTrainer(chatbot)

  trainer.train([
    'Hola',
    'Hola, como estás hoy Fernando?',
    'Bien'
  ])

  levenshtein_distance = LevenshteinDistance('ESP')
  shootWord = Statement('No deberías haber dicho eso')
  last_input_user = ""

async def sayToClient(paragraph):
  global sio

  print("Saying '" + paragraph + "' to client...")

  # Send socket to angular with the text to reproduce
  return await sio.emit('on_server_message', paragraph)

async def sayToIA(input_user):
  global last_input_user
  global chatbot

  learnt = False
  # response_0 = checkProtcols(input_user)
  # response_1 = checkActions(input_user)

  # if response_0 == True or response_1 == True:
  #     learnt = True

  # if levenshtein_distance.compare(Statement(input_user), shootWord) > 0.51:
  #     sayToClient("¿Que debería haber dicho?")
      

  last_input_user = input_user

  if learnt == False:
      # response = chatbot.get_response(input_user) # Problems with this!!
      await sayToClient("Holaaaa")

init()