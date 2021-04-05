from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from flask import Flask, jsonify, request

# Global vars
last_input_user = ""
levenshtein_distance = ""
shootWord = ""
trainer = ""
chatbot = ""
learnt = False

def init():
  initializeIA()
  initializeFlask()

def initializeFlask():
  app = Flask(__name__)

  subscribeEndPoints(app)
  
  if __name__ == '__main__':
    app.run(debug=True, port=8080)

def subscribeEndPoints(app):
  
  @app.route('/talk-ia', methods=["POST"])
  def talkToIa():
    global learnt

    if learnt == False:
      response = sayToIA(request.json["message"])
    else:
      response = trainIA(request.json["message"])
    
    return jsonify({
      "message": response
    })

def initializeIA():
  global chatbot
  global trainer
  global levenshtein_distance
  global shootWord

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
  
def sayToIA(input_user):
  global learnt
  global last_input_user

  if levenshtein_distance.compare(Statement(input_user), shootWord) > 0.51:
    learnt = True
    return "¿Que debería haber dicho?"

  last_input_user = input_user

  return chatbot.get_response(input_user).text

def trainIA(newWordToLearn):
  global learnt
  global last_input_user

  trainer.train([last_input_user, newWordToLearn])
  learnt = False
  return 'Genial, gracias'

init()