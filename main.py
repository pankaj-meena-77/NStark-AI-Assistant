import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import wikipedia
import json
from datetime import datetime

# ---------------- CONFIG ----------------
wikipedia.set_lang("en")
MEMORY_FILE = "memory.json"

# ---------------- MEMORY ----------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {"user_name": "Pankaj"}
    return {"user_name": "Pankaj"}

memory = load_memory()

# ---------------- SPEAK FUNCTION (WINDOWS SAFE) ----------------
def speak(text):
    print("JARVIS:", text)
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------------- SPEECH RECOGNITION ----------------
r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.8

# ---------------- MIC CALIBRATION ----------------
with sr.Microphone() as source:
    print("Calibrating microphone... stay silent")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Calibration complete")

speak("Jarvis is online and ready")

# ---------------- MAIN LOOP ----------------
while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=7)

        try:
            command = r.recognize_google(audio).lower()
            print("You said:", command)
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            speak("Network error")
            continue

        # ---------------- COMMANDS ----------------
        if "hello" in command:
            speak(f"Hello {memory['user_name']}")

        elif "who am i" in command:
            speak(f"You are {memory['user_name']}")

        elif "your name" in command:
            speak("My name is Jarvis")

        elif "time" in command:
            speak(datetime.now().strftime("The time is %I:%M %p"))

        elif "date" in command:
            speak(datetime.now().strftime("Today is %B %d, %Y"))

        elif "search wikipedia" in command:
            speak("Searching Wikipedia")
            query = command.replace("search wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("Your search is too broad. Please be specific.")
            except wikipedia.exceptions.PageError:
                speak("No result found.")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye. Shutting down.")
            break

        else:
            speak("I am still learning. Please try another command")

    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        break
    except Exception as e:
        print("ERROR:", e)
