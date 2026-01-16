import speech_recognition as sr
import pyttsx3

# Initialize
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')

engine.setProperty('rate', 140)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


def list_microphones():
    try:
        names = sr.Microphone.list_microphone_names()
        print("Available microphone devices:")
        for i, name in enumerate(names):
            print(f"  [{i}] {name}")
    except Exception as e:
        print("Could not enumerate microphones:", e)


list_microphones()
speak("N Stark AI is now active")


while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                print("Listening timed out (no speech detected)")
                speak("I didn't hear anything. Please try again.")
                continue

        try:
            command = r.recognize_google(audio).lower()
            print("You said:", command)
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("Sorry, I couldn't understand you. Please repeat.")
            continue
        except sr.RequestError as e:
            print("Speech recognition request failed:", e)
            speak("Network error or speech service unavailable")
            continue

        if "your name" in command:
            speak("My name is N Stark AI")

        elif "who am i" in command:
            speak("You are Pankaj, my creator")

        elif "hello" in command:
            speak("Hello Pankaj, nice to hear you")

        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye sir, see you later")
            break

        else:
            speak("Sorry sir, can you repeat that again")

    except KeyboardInterrupt:
        speak("Shutting down. Goodbye")
        break
    except Exception as e:
        print("Unexpected error:", e)
        speak("An unexpected error occurred. Check the console for details")
