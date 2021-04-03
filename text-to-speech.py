from gtts import gTTS
from playsound import playsound

def say(paragraph):
    tts = gTTS(paragraph, lang='es-us')
    tts.save("tmp-audio.mp3")
    playsound("tmp-audio.mp3")

say('Holaaaaaaa Fernandoooooooooo')
