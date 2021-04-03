from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from gtts import gTTS
from pathlib import Path
from ctypes import windll
import os
import webbrowser
import socket

silence = False

def listen():
    # Wait for input from the angular app

def say(paragraph):
    # Send through sockets the response of the IA

def checkProtcols(paragraph):
    
    if levenshtein_distance.compare(Statement(paragraph), Statement('Activar protocolo')) > 0.51:
        
        if 'descansa' in paragraph:
            say("Activando protocolo descansar. Adios Fernando")
            
            #TODO: Send socket to pc-side 
            
            return True
        
        if 'caja fuerte' in paragraph:
            say("Activando protocolo caja fuerte. Benditos sean los nuevos padres de la patria por permitirnos purgar nuestras almas. Benditos sean los estados unidos, una nación renacida.")

            #TODO: Send socket to pc-side 


        if 'trabajo' in paragraph:
            say("Activando protocolo trabajo. Abriendo: visual studio code, Source tree, Slack y google chrome con la cuenta de su trabajo en google calendar.")
            #TODO: Send socket to pc-side 
            return True

        say(Statement('No conozco ese protocolo'))
        return True

def checkActions(paragraph):
    global silence

    if 'silenciar' in paragraph or 'cállate' in paragraph or 'silencio' in paragraph or 'callate' in paragraph or 'callar' in paragraph :
        say('Okay, me silenciaré hasta que me digas que hable nuevamente.')
        # Silent the bot
        silence = True
        return True
    
    if 'volvé a hablar' in paragraph or 'podes hablar' in paragraph or 'hablar' in paragraph or 'habla nuevamente' in paragraph:
        silence = False
        # Silent the bot
        say('Hola Fernando nuevamente, que necesitas?')
        return True

    if 'buscar' in paragraph or 'podés buscarme' in paragraph or 'Buscar' in paragraph or 'busques' in paragraph:
        say('¿En donde deseas buscar?')
        search = listen()

        if 'Google' in search:
            say('¿Que deseas buscar en Google?')
            search_title = listen()
            say('Buscando ' + search_title + ' en Google')

            # Send sockets
            # 'https://www.google.com/search?q=' + search_title

        if 'YouTube' in search or 'youtube' in search:
            say('¿Que deseas buscar en Youtube?')
            search_title = listen()
            say('Buscando ' + search_title + ' en Youtube')
            # 'https://www.youtube.com/results?search_query=' + search_title
            
        return True


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
learnt = False

say('Hola Fernando, ¿como estás?')

# Enter to the conversation
while True:
    input_user = listen()

    response_0 = checkProtcols(input_user)
    response_1 = checkActions(input_user)

    if response_0 == True or response_1 == True:
        learnt = True

    if levenshtein_distance.compare(Statement(input_user), shootWord) > 0.51:
        say("¿Que debería haber dicho?")
    
        input_user_correction = listen()
        trainer.train([last_input_user, input_user_correction])
        say('Genial, gracias')
        learnt = True

    last_input_user = input_user

    if learnt == False:
        response = chatbot.get_response(input_user)
        say(response.text)
    
    learnt = False


    