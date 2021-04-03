from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from gtts import gTTS
from pathlib import Path
from ctypes import windll
from playsound import playsound
import speech_recognition as sr
import os
import webbrowser

silence = False

def listen():
    try:
        with m as source: audio = r.listen(source)
        value = r.recognize_google(audio, language="es-ES")

        if str is bytes:
            print(u"Dijiste {}".format(value).encode("utf-8"))
        else:
            print("Dijiste ---> {}".format(value))

        return format(value)
    
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        return format("")
    
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        return format("")

def say(paragraph):
    if silence == True:
        return
    else:
        tts = gTTS(paragraph.text, lang = 'es')
        file1 = str("vision.mp3")
        tts.save(file1)
        playsound(file1)
        os.remove(file1)

def checkProtcols(paragraph):
    
    if levenshtein_distance.compare(Statement(paragraph), Statement('Activar protocolo')) > 0.51:
        
        if 'descansa' in paragraph:
            say(Statement("Activando protocolo descansar. Adios Fernando"))
            
            if not windll.powrprof.SetSuspendState(False, False, False):
                print("No se ha podido suspender el sistema.")
            #TODO: Send socket to pc-side 
            
            return
        
        if 'caja fuerte' in paragraph:
            say(Statement("Activando protocolo caja fuerte. Benditos sean los nuevos padres de la patria por permitirnos purgar nuestras almas. Benditos sean los estados unidos, una nación renacida. Liberen a la bestia, salgan a purgar a las calles."))
            
            os.system("shutdown /s")

            return exit()

        if 'trabajo' in paragraph:
            say(Statement("Activando protocolo trabajo. Abriendo: visual studio code, Source tree, Slack y google chrome con la cuenta de su trabajo en google calendar."))
            os.system(r'"C:/Users/Fer/AppData/Local/Programs/Microsoft VS Code/bin/code.cmd"')
            os.system(r'"C:/Users/Fer/AppData/Local/SourceTree/SourceTree.exe"')
            os.system(r'"C:/Users/Fer/AppData/Local/slack/slack.exe"')
            webbrowser.open('https://calendar.google.com/calendar/u/0/r?tab=rc', new=0, autoraise=True)
            return True

        say(Statement('No conozco ese protocolo'))
        return True

def checkActions(paragraph):
    global silence

    if 'silenciar' in paragraph or 'cállate' in paragraph or 'silencio' in paragraph or 'callate' in paragraph or 'callar' in paragraph :
        say(Statement('Okay, me silenciaré hasta que me digas que hable nuevamente.'))
        # Silent the bot
        silence = True
        return True
    
    if 'volvé a hablar' in paragraph or 'podes hablar' in paragraph or 'hablar' in paragraph or 'habla nuevamente' in paragraph:
        silence = False
        # Silent the bot
        say(Statement('Hola Fernando nuevamente, que necesitas?'))
        return True

    if 'buscar' in paragraph or 'podés buscarme' in paragraph or 'Buscar' in paragraph or 'busques' in paragraph:
        say(Statement('¿En donde deseas buscar?'))
        search = listen()

        if 'Google' in search:
            say(Statement('¿Que deseas buscar en Google?'))
            search_title = listen()
            say(Statement('Buscando ' + search_title + ' en Google'))
            webbrowser.open('https://www.google.com/search?q=' + search_title, new=0, autoraise=True)

        if 'YouTube' in search or 'youtube' in search:
            say(Statement('¿Que deseas buscar en Youtube?'))
            search_title = listen()
            say(Statement('Buscando ' + search_title + ' en Youtube'))
            webbrowser.open('https://www.youtube.com/results?search_query=' + search_title, new=0, autoraise=True)
            
        return True

# Initial steps
r = sr.Recognizer()
m = sr.Microphone()

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

# Setup voice
try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    say(Statement('Hola Fernando, ¿como estás?'))

except KeyboardInterrupt:
    pass


# Enter to the conversation
while True:
    input_user = listen()

    response_0 = checkProtcols(input_user)
    response_1 = checkActions(input_user)

    if response_0 == True or response_1 == True:
        learnt = True

    if levenshtein_distance.compare(Statement(input_user), shootWord) > 0.51:
        say(Statement("¿Que debería haber dicho?"))
    
        input_user_correction = listen()
        trainer.train([last_input_user, input_user_correction])
        say(Statement('Genial, gracias'))
        learnt = True

    last_input_user = input_user

    if learnt == False:
        response = chatbot.get_response(input_user)
        say(response)
    
    learnt = False

