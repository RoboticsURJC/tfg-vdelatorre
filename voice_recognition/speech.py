import speech_recognition as sr
from datetime import date
from time import sleep


recognize = sr.Recognizer()
mic = sr.Microphone()

print("hello")

while True:
    try:
        with mic as source:
            audio = recognize.listen(source)
        words = recognize.recognize_google(audio) 
        print(words)
        
        if words == "today":
            print(date.today())

        if words == "exit":
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            break
    except:
        print("so much noise")
    
