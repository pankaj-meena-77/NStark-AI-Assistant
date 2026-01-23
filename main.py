# ================== IMPORTS ==================
from email.mime import text
import speech_recognition as sr
import os
import webbrowser
import wikipedia
import json
import time
import random
import sys
import asyncio
import tempfile
import uuid
from datetime import datetime
import edge_tts
from playsound import playsound


# ================== INTENTS ==================
INTENT_OPEN_CHROME = "OPEN_CHROME"
INTENT_GET_TIME = "GET_TIME"
INTENT_GET_DATE = "GET_DATE"
INTENT_OPEN_YOUTUBE = "OPEN_YOUTUBE"
INTENT_EXIT = "EXIT"
INTENT_UNKNOWN = "UNKNOWN"
INTENT_CLOSE_APP = "CLOSE_APP"


# ================== INTENT DETECTION ==================
def detect_intent(command: str):
    command = command.lower()

    # --- OPEN CHROME / BROWSER ---
    if ("open" in command or "launch" in command or "start" in command) and (
        "chrome" in command or "browser" in command or "google" in command
    ):
        return INTENT_OPEN_CHROME

    # --- OPEN YOUTUBE ---
    if "youtube" in command and ("open" in command or "launch" in command):
        return INTENT_OPEN_YOUTUBE

    # --- TIME ---
    if "time" in command:
        return INTENT_GET_TIME

    # --- DATE ---
    if "date" in command or "day" in command:
        return INTENT_GET_DATE

    # --- EXIT JARVIS ---
    if "exit" in command or "quit" in command:
        return INTENT_EXIT

    # --- CLOSE APP ---
    if "close" in command or "shut" in command:
        return INTENT_CLOSE_APP

    return INTENT_UNKNOWN


# ================== TARGET DETECTION ==================
def detect_target(command: str):
    command = command.lower()

    if "chrome" in command or "browser" in command or "google" in command:
        return "chrome"

    if "youtube" in command:
        return "youtube"

    if "vs code" in command or "vscode" in command or "code" in command:
        return "vscode"

    return None
# ================== ACTION FUNCTIONS ==================
def action_open_chrome():
    speak("Opening Google Chrome")
    os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

def action_get_time():
    speak(datetime.now().strftime("The time is %I:%M %p"))

def action_get_date():
    speak(datetime.now().strftime("Today is %B %d, %Y"))

def action_open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def action_exit():
    speak("Goodbye. Shutting down.")
    sys.exit()

def action_unknown():
    speak(random.choice(fallback_responses))


def action_close_app(target):
    if target == "chrome":
        speak("Closing Google Chrome")
        os.system("taskkill /im chrome.exe /f")

    elif target == "youtube":
        speak("Closing YouTube")
        os.system("taskkill /im chrome.exe /f")

    elif target == "vscode":
        speak("Closing Visual Studio Code")
        os.system("taskkill /im Code.exe /f")

    else:
        speak("I am not sure what you want me to close")




# ================== INTENT DISPATCHER ==================
def handle_intent(intent, command):
    if intent == INTENT_OPEN_CHROME:
        action_open_chrome()

    elif intent == INTENT_GET_TIME:
        action_get_time()

    elif intent == INTENT_GET_DATE:
        action_get_date()

    elif intent == INTENT_OPEN_YOUTUBE:
        action_open_youtube()

    elif intent == INTENT_EXIT:
        action_exit()
    
    elif intent == INTENT_CLOSE_APP:
        target = detect_target(command)
        action_close_app(target)


    else:
        action_unknown()




# ================== PATHS ==================
MUSIC_DIR = "C:\\Users\\ASUS\\Music"

# ================== FALLBACK RESPONSES ==================
fallback_responses = [
    "I am not sure about that yet",
    "Can you rephrase that",
    "I am still learning this",
    "I did not understand clearly"
]

# ================== CONFIG ==================
wikipedia.set_lang("en")
MEMORY_FILE = "memory.json"
ACTIVE_TIME = 50
COMMAND_COOLDOWN = 1.5
DUPLICATE_WINDOW = 2.0
TTS_MUTE_WINDOW = 0.8

last_command_time = 0
LAST_COMMAND_TEXT = ""
last_tts_time = 0

# ================== MEMORY ==================
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"user_name": "Pankaj"}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

# ================== CONTEXT ==================
last_response = ""
last_wiki_query = ""
in_conversation = False

# ================== EDGE-TTS (SAFE) ==================
async def _speak_async(text):
    tmp_file = os.path.join(
        tempfile.gettempdir(),
        f"jarvis_{uuid.uuid4().hex}.mp3"
    )

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"  # 🔥 Natural neural voice
    )

    await communicate.save(tmp_file)
    playsound(tmp_file)

    try:
        os.remove(tmp_file)
    except:
        pass


def speak(text):
    global last_response, last_tts_time
    last_response = text
    print("JARVIS:", text)

    try:
        asyncio.run(_speak_async(text))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_speak_async(text))

    last_tts_time = time.time()

# ================== SPEECH RECOGNITION ==================
r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.8

# ================== WAKE WORD ==================
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            return False

    try:
        text = r.recognize_google(audio).lower()
        print("Heard:", text)
        return text.strip() == "jarvis"
    except:
        return False


def listen_command():
    since = time.time() - last_tts_time
    if since < TTS_MUTE_WINDOW:
        time.sleep(TTS_MUTE_WINDOW - since + 0.05)

    with sr.Microphone() as source:
        print("Listening for command...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = r.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except:
        return ""

# ================== MIC CALIBRATION ==================
with sr.Microphone() as source:
    print("Calibrating microphone... stay silent")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Calibration complete")

speak("Jarvis is online and ready")

# ================== MAIN LOOP ==================
while True:
    try:
        if not listen_for_wake_word():
            continue

        speak("Yes,  sir")
        active_until = time.time() + ACTIVE_TIME
        in_conversation = True

        while time.time() < active_until:
            command = listen_command()
            if not command:
                continue

            intent = detect_intent(command)
            handle_intent(intent, command)


            current_time = time.time()

            if command == LAST_COMMAND_TEXT and current_time - last_command_time < DUPLICATE_WINDOW:
                continue

            if current_time - last_command_time < COMMAND_COOLDOWN:
                continue

            last_command_time = current_time
            LAST_COMMAND_TEXT = command
            active_until = time.time() + ACTIVE_TIME

            LAST_COMMAND_TEXT = command
            active_until = time.time() + ACTIVE_TIME

            intent = detect_intent(command)
            handle_intent(intent, command)


            # ========== COMMANDS ==========
            # if "restart jarvis" in command:
            #     speak("Restarting")
            #     python = sys.executable
            #     os.execl(python, python, *sys.argv)

            # elif "hello" in command:
            #     speak(f"Hello {memory['user_name']}")

            # elif "open chrome" in command:
            #     speak("Opening Google Chrome")
            #     os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

            # elif "close chrome" in command:
            #     speak("Closing Google Chrome")
            #     os.system("taskkill /im chrome.exe /f")

            # elif "open vs code" in command:
            #     speak("Opening Visual Studio Code")
            #     os.startfile("C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

            # elif "close vs code" in command:
            #     speak("Closing Visual Studio Code")
            #     os.system("taskkill /im Code.exe /f")

            # elif "play music" in command:
            #     songs = os.listdir(MUSIC_DIR)
            #     if songs:
            #         speak("Playing music")
            #         os.startfile(os.path.join(MUSIC_DIR, songs[0]))
            #     else:
            #         speak("No music files found")

            # elif "stop music" in command:
            #     speak("Stopping music")
            #     os.system("taskkill /im wmplayer.exe /f")

            # elif "who am i" in command:
            #     speak(f"You are {memory['user_name']}")

            # elif "your name" in command:
            #     speak("My name is Jarvis")

            # elif "time" in command:
            #     speak(datetime.now().strftime("The time is %I:%M %p"))

            # elif "date" in command:
            #     speak(datetime.now().strftime("Today is %B %d, %Y"))

            # elif "remember that" in command:
            #     fact = command.replace("remember that", "").strip()
            #     if fact:
            #         memory["note"] = fact
            #         save_memory(memory)
            #         speak("I will remember that")
            #     else:
            #         speak("What should I remember")

            # elif "what do you remember" in command:
            #     note = memory.get("note")
            #     speak(note if note else "I do not remember anything yet")

            # elif "search wikipedia" in command:
            #     query = command.replace("search wikipedia", "").strip()
            #     if query:
            #         speak("Searching Wikipedia")
            #         try:
            #             last_wiki_query = query
            #             speak(wikipedia.summary(query, sentences=2))
            #         except:
            #             speak("No result found")

            # elif "tell me more" in command:
            #     if last_wiki_query:
            #         speak(wikipedia.summary(last_wiki_query, sentences=4))
            #     else:
            #         speak("There is nothing to continue")

            # elif "repeat that" in command:
            #     speak(last_response if last_response else "There is nothing to repeat")

            # elif "open youtube" in command:
            #     speak("Opening YouTube")
            #     webbrowser.open("https://www.youtube.com")

            # elif "close youtube" in command:
            #     speak("Closing YouTube")
            #     os.system("taskkill /f /im chrome.exe")

            # elif "sleep" in command:
            #     speak("Going to sleep")
            #     break

            # elif "exit" in command or "quit" in command or "stop" in command:
            #     speak("Goodbye. Shutting down.")
            #     sys.exit()

            # else:
            #     speak(random.choice(fallback_responses))

        speak("I am going to sleep now")
        in_conversation = False

    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        break
