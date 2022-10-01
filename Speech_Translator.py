import speech_recognition # 3.8.1
from gtts import gTTS  # 2.2.4
from googletrans import Translator, constants  # 3.1.0a0
from playsound import playsound  # 1.2.2
# pyAudio 0.2.12
import os

TRANSLATE_TO_LANGUAGE = "pl"
TRANSLATE_FROM_LANGUAGE = "en"
LANG_DETECTION =  False


translator = Translator()
recognizer = speech_recognition.Recognizer()



def translate(input,toLang,fromLang):
    if LANG_DETECTION:
        res = translator.translate(input, dest = toLang)
    else:
        res = translator.translate(input,dest = toLang,src=fromLang)
    return res.text

def speak(inputText, language):
    audio = gTTS(text = inputText,lang = language,slow=True)
    filename = "tempTranslation.mp3"
    audio.save(filename)
    playsound(filename)
    os.remove(filename)

    
def main():
    global recognizer
    global translator
    print("================================================================")
    if LANG_DETECTION:
        print(f"Currently translating any detected language to {constants.LANGUAGES[TRANSLATE_TO_LANGUAGE]}, speak to translate\n")
    else:
        print(f"Currently translating {constants.LANGUAGES[TRANSLATE_FROM_LANGUAGE]} to {constants.LANGUAGES[TRANSLATE_TO_LANGUAGE]}, speak to translate\n")
    while True:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.001)
            audio = recognizer.listen(mic)
            if LANG_DETECTION:
                text = recognizer.recognize_google(audio, show_all = True)
            else:
                text = recognizer.recognize_google(audio, language = TRANSLATE_FROM_LANGUAGE, show_all = True)
            if len(text) > 0:
                sentence = text['alternative'][0]['transcript']
                print(f"    -Recognized:\t {sentence}")
                if LANG_DETECTION:
                    print(f"Language Detected = ",translator.detect(sentence))

                translation = translate(sentence, TRANSLATE_TO_LANGUAGE, TRANSLATE_FROM_LANGUAGE)
                commandTranslation = translation
                if TRANSLATE_TO_LANGUAGE != "en":
                    commandTranslation = translate(sentence, 'en', TRANSLATE_FROM_LANGUAGE)
                
                print(f" {TRANSLATE_TO_LANGUAGE} -translated:\t",translation)
                speak(translation,TRANSLATE_TO_LANGUAGE)
                print("- - - - - - - - - - - - - - - - - -")

                if commandTranslation in COMMAND_PHRASES:
                    command = COMMAND_PHRASES[commandTranslation]
                    if command == 0:
                        print("\n=== STOP COMMAND SENT ===\n")
                        break
                    else:
                        COMMAND_PHRASES[commandTranslation]()
                    

            continue

def change_output_language():
    print("\n=== CHANGE OUTPUT LANGUAGE COMMAND SENT ===")
    global TRANSLATE_TO_LANGUAGE
    langTrans = ""
    langToCode = {v: k for k, v in constants.LANGUAGES.items()}
    attempts = 0
    while langTrans.lower() not in langToCode:
        print("\nENTER VALID LANGUAGE")
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.001)
            audio = recognizer.listen(mic)
            if LANG_DETECTION:
                text = recognizer.recognize_google(audio, show_all = True)
            else:
                text = recognizer.recognize_google(audio, language = TRANSLATE_FROM_LANGUAGE, show_all = True)
            if len(text) > 0:
                sentence = text['alternative'][0]['transcript']
                langTrans = translate(sentence, 'en', TRANSLATE_FROM_LANGUAGE)
                print(f"Attempt to swtich language to:\t {langTrans.upper()}")
        attempts = attempts + 1
        if attempts > 7:
            print("\n====NO VALID LANGUAGE DETECTED, RETURNING ====\n")
            return

    newLang = langToCode[langTrans.lower()]
    TRANSLATE_TO_LANGUAGE = newLang
    print(f"CHANGED TO {langTrans.upper()} - {TRANSLATE_TO_LANGUAGE}")
    print("\n==========================================\n")


def change_input_language():
    print("\n=== CHANGE INPUT LANGUAGE COMMAND SENT ===")
    global TRANSLATE_FROM_LANGUAGE
    langTrans = ""
    langToCode = {v: k for k, v in constants.LANGUAGES.items()}
    attempts = 0
    while langTrans.lower() not in langToCode:
        print("\nENTER VALID LANGUAGE")
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.001)
            audio = recognizer.listen(mic)
            if LANG_DETECTION:
                text = recognizer.recognize_google(audio, show_all = True)
            else:
                text = recognizer.recognize_google(audio, language = TRANSLATE_FROM_LANGUAGE, show_all = True)
            if len(text) > 0:
                sentence = text['alternative'][0]['transcript']
                langTrans = translate(sentence, 'en', TRANSLATE_FROM_LANGUAGE)
                print(f"Attempt to swtich language to:\t {langTrans.upper()}")
        attempts = attempts + 1
        if attempts > 7:
            print("\n====NO VALID LANGUAGE DETECTED, RETURNING ====\n")
            return

    newLang = langToCode[langTrans.lower()]
    TRANSLATE_FROM_LANGUAGE = newLang
    print(f"CHANGED TO {langTrans.upper()} - {TRANSLATE_FROM_LANGUAGE}")
    print("\n=========================================\n")


COMMAND_PHRASES = {
    "stop program" : 0,
    "shutdown program" : 0,
    "halt program" : 0,
    "change output language": change_output_language,
    "change input language": change_input_language
}

main()