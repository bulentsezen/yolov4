import pyttsx3

def MetniOku(metin):
    okuyucu = pyttsx3.init()
    okuyucu.say(metin)
    okuyucu.runAndWait()


#MetniOku("Hydrogen is the chemical element with the symbol H and atomic number 1. "
#         "Hydrogen is the lightest element. At standard conditions hydrogen is a gas of diatomic molecules having the formula H2. "
#         "It is colorless, odorless, tasteless, non-toxic, and highly combustible")

MetniOku("Hidrojen, sembolü H, atom numarası 1 olan kimyasal bir element. "
         "Standart sıcaklık ve basınç altında renksiz, kokusuz, metalik olmayan, tatsız, oldukça yanıcı ve H₂ olarak bulunan bir diatomik gazdır.")


