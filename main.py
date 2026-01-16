import speech_recognition as sr
import pyttsx3
from datetime import datetime

# ---------------- INITIALIZE ----------------
r = sr.Recognizer()

# 🔧 LISTENING TUNING (IMPORTANT)
r.energy_threshold = 300
r.dynamic_energy_threshold = False
r.pause_threshold = 1.0
r.non_speaking_duration = 0.7

def speak(text):
    print("JARVIS:", text)
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------------- MEMORY ----------------
memory = {
    "user_name": "Pankaj"
}

# ---------------- MIC CALIBRATION (ONCE) ----------------
with sr.Microphone() as source:
    print("Calibrating microphone... please stay silent")
    r.adjust_for_ambient_noise(source, duration=1.2)
    print("Calibration complete")

speak("Jarvis is online and ready")

# ---------------- MAIN LOOP ----------------
while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(
                source,
                timeout=3,
                phrase_time_limit=4
            )

        try:
            command = r.recognize_google(audio).lower()
            print("You said:", command)
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("Please say that again clearly")
            continue
        except sr.RequestError:
            speak("Network error")
            continue

        # ---------------- COMMANDS ----------------

        if "hello" in command:
            speak(f"Hello {memory['user_name']}, nice to hear you")

        elif "who am i" in command:
            speak(f"You are {memory['user_name']}")

        elif "your name" in command:
            speak("My name is Jarvis")

        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        elif "what is the date" in command:
            today = datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {today}")

        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye. Shutting down.")
            break

        else:
            speak("I am still learning. Please try another command")

    except sr.WaitTimeoutError:
        continue
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        break
