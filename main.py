import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand.")
except sr.RequestError:
    print("Network error.")
import speech_recognition as sr
import pyttsx3

# Initialize recognizer and speaker
r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

with sr.Microphone() as source:
    print("Speak something...")
    speak("Speak something")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
    speak("You said " + text)

except sr.UnknownValueError:
    print("Sorry, I could not understand.")
    speak("Sorry, I could not understand.")

except sr.RequestError:
    print("Network error.")
    speak("Network error")
