from pygame import mixer  # Load the pygame library
import time
from playsound import playsound

from gtts import gTTS

tts = gTTS("Gün Doğmadan Neler Doğar, Güneş Girmeyen Eve Doktor Girer, Gülü Seven Dikenine Katlanır", lang="tr")
tts.save("mrb.mp3")

#playsound("mrb.mp3")

mixer.init()
mixer.music.load('mrb.mp3')
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)
