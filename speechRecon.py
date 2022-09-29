import speech_recognition
from gtts import gTTS
from googletrans import Translator, constants
from playsound import playsound
import os

TRANSLATE_TO_LANGUAGE = "pl"
TRANSLATE_FROM_LANGUAGE = "en"

translator = Translator()

print("================================================================")
print(f"Currently translating {constants.LANGUAGES[TRANSLATE_FROM_LANGUAGE]} to {constants.LANGUAGES[TRANSLATE_TO_LANGUAGE]}, speak to translate\n")

#res = translator.translate("Thank You",dest = "polish",src="en")
#print(f"{res.text} \n\n")

recognizer = speech_recognition.Recognizer()

def speak(input,toLang,fromLang):
    res = translator.translate(input,dest = toLang,src=fromLang)
    audio = gTTS(text = res.text,lang = toLang,slow=True)
    filename = "tempTranslation.mp3"
    audio.save(filename)
    playsound(filename)
    os.remove(filename)
    return res.text

while True:
    with speech_recognition.Microphone() as mic:
        
        recognizer.adjust_for_ambient_noise(mic, duration = 0.005)
        audio = recognizer.listen(mic)
        text = recognizer.recognize_google(audio, language = TRANSLATE_FROM_LANGUAGE, show_all = True)
        if len(text) > 0:
            print(f"Recognized:\t {text['alternative'][0]['transcript']}")
            sentence = text['alternative'][0]['transcript']
            #print(len(text['alternative'][0]['transcript'].split(' ')))
            print("translated:\t",speak(sentence, TRANSLATE_TO_LANGUAGE, TRANSLATE_FROM_LANGUAGE))


        recognizer = speech_recognition.Recognizer()
        continue