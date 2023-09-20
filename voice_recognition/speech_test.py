import speech_recognition as sr



recognize = sr.Recognizer()

#obtener sonido del micrófono
mic = sr.Microphone()

print("hello")

while True:
    
    with mic as source:
        audio = recognize.listen(source)
    #audio cogido del micrófono se reconoce en google
    words = recognize.recognize_google(audio) 
    print(words)
    
    
    
