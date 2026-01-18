
from email.mime import text
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import wikipedia
import json
import time
from datetime import datetime

# ---------------- CONFIG ----------------
wikipedia.set_lang("en")
MEMORY_FILE = "memory.json"
ACTIVE_TIME = 50  # seconds Jarvis stays awake after wake word

# ---------------- MEMORY ----------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"user_name": "Pankaj"}

memory = load_memory()

# ---------------- CONTEXT MEMORY ----------------
last_response = ""
last_wiki_query = ""

# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    global last_response
    last_response = text

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

# ---------------- WAKE WORD ----------------
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        audio = r.listen(source, phrase_time_limit=4)

    try:
        wake_text = r.recognize_google(audio).lower()
        print("Heard:", wake_text)
        return "jarvis" in wake_text
    except:
        return False

def listen_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source, timeout=5, phrase_time_limit=7)

    try:
        command = r.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# ---------------- MIC CALIBRATION ----------------
with sr.Microphone() as source:
    print("Calibrating microphone... stay silent")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Calibration complete")

speak("Jarvis is online and ready")

# ---------------- MAIN LOOP ----------------
while True:
    try:
        # ---- WAKE MODE ----
        if not listen_for_wake_word():
            continue

        speak("Yes?")
        active_until = time.time() + ACTIVE_TIME

        # ---- ACTIVE MODE ----
        while time.time() < active_until:
            command = listen_command()
            if not command:
                continue

            active_until = time.time() + ACTIVE_TIME

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
                query = command.replace("search wikipedia", "").strip()
                if not query:
                    speak("What should I search on Wikipedia?")
                    continue

                speak("Searching Wikipedia")
                try:
                    last_wiki_query = query
                    result = wikipedia.summary(query, sentences=2)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError:
                    speak("Your search is too broad. Please be specific.")
                except wikipedia.exceptions.PageError:
                    speak("No result found.")
                except Exception:
                    speak("Something went wrong while searching Wikipedia.")

            elif "tell me more" in command:
                if last_wiki_query:
                    try:
                        result = wikipedia.summary(last_wiki_query, sentences=4)
                        speak(result)
                    except:
                        speak("I cannot fetch more details.")
                else:
                    speak("There is nothing to continue.")

            elif "repeat that" in command:
                if last_response:
                    speak(last_response)
                else:
                    speak("There is nothing to repeat.")

            elif "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif "sleep" in command:
                speak("Going to sleep")
                break

            elif "exit" in command or "quit" in command or "stop" in command:
                speak("Goodbye. Shutting down.")
                exit()

            else:
                speak("I am still learning")

        speak("I am going to sleep now")

    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        break
    except Exception as e:
        print("ERROR:", e)
