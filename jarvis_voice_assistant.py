"""
================================================================================
                    JARVIS AI VOICE ASSISTANT (ALL-IN-ONE)
================================================================================
A complete, standalone voice-controlled AI assistant with speech recognition,
offline text-to-speech, system control, web navigation, and intelligent answers.
================================================================================
"""

import os
import sys
import time
import random
import datetime
import webbrowser
import subprocess
import threading

# Required Third-Party Libraries
try:
    import pyttsx3
except ImportError:
    print("[Error]: pyttsx3 not installed. Run: pip install pyttsx3")
    sys.exit(1)

try:
    import speech_recognition as sr
except ImportError:
    print("[Error]: SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio")
    sys.exit(1)

try:
    import wikipedia
except ImportError:
    wikipedia = None

try:
    import pyautogui
except ImportError:
    pyautogui = None


# ---------------------------------------------------------
# TEXT-TO-SPEECH (TTS) ENGINE
# ---------------------------------------------------------
def init_tts_engine():
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except Exception:
        pass

    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        # voices[0] = Microsoft David (Male), voices[1] = Microsoft Zira (Female)
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    return engine

def speak(text):
    """Speaks text aloud using SAPI5."""
    text = str(text)
    print(f"\n[JARVIS]: {text}")
    try:
        engine = init_tts_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error]: {e}")


# ---------------------------------------------------------
# SPEECH RECOGNITION (STT) ENGINE
# ---------------------------------------------------------
def take_command():
    """Listens via microphone and returns recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Status]: Listening...")
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        print("[Status]: Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"[YOU]: {query}")
        return query.lower().strip()
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"[STT Error]: {e}")
        return ""


# ---------------------------------------------------------
# HELPER ACTIONS
# ---------------------------------------------------------
def search_google(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)

def search_youtube(query):
    yt_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(yt_url)

def open_app(app_name):
    app_name = app_name.lower()
    try:
        if "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad"
        elif "calc" in app_name or "calculator" in app_name:
            subprocess.Popen(["calc.exe"])
            return "Opening Calculator"
        elif "cmd" in app_name or "command prompt" in app_name:
            subprocess.Popen(["cmd.exe"])
            return "Opening Command Prompt"
        elif "paint" in app_name or "mspaint" in app_name:
            subprocess.Popen(["mspaint.exe"])
            return "Opening Paint"
        elif "camera" in app_name:
            subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
            return "Opening Camera"
        elif "explorer" in app_name or "files" in app_name:
            subprocess.Popen(["explorer.exe"])
            return "Opening File Explorer"
        elif "task manager" in app_name:
            subprocess.Popen(["taskmgr.exe"])
            return "Opening Task Manager"
        else:
            subprocess.Popen([app_name], shell=True)
            return f"Launching {app_name}"
    except Exception as e:
        return f"Could not launch application: {e}"

def take_screenshot():
    if not pyautogui:
        return "PyAutoGUI is not installed."
    try:
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        if not os.path.exists(pictures_dir):
            pictures_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        
        count = 1
        filepath = os.path.join(pictures_dir, f"jarvis_screenshot_{count}.png")
        while os.path.exists(filepath):
            count += 1
            filepath = os.path.join(pictures_dir, f"jarvis_screenshot_{count}.png")
            
        pyautogui.screenshot(filepath)
        return f"Screenshot saved to {filepath}"
    except Exception as e:
        return f"Error taking screenshot: {e}"


# ---------------------------------------------------------
# COMMAND PROCESSOR
# ---------------------------------------------------------
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Java programmers have to wear glasses? Because they don't C sharp!",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
    "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings!"
]

def process_command(query):
    if not query:
        return

    # Greetings
    if any(greet in query for greet in ["hello jarvis", "hi jarvis", "hey jarvis", "hello", "hi"]):
        responses = [
            "Hello sir! How can I assist you today?",
            "Greetings, sir! Jarvis is at your service.",
            "Hello! Systems are primed and ready."
        ]
        speak(random.choice(responses))

    elif "how are you" in query:
        speak("I am functioning at peak efficiency, sir! How are you doing today?")

    elif "who are you" in query or "what is your name" in query:
        speak("I am Jarvis, your personal AI voice assistant.")

    elif "what can you do" in query or "help" in query:
        speak("I can open websites, search Google and YouTube, launch Windows apps, tell the time and date, check Wikipedia, take screenshots, and tell jokes!")

    elif "thank you" in query or "thanks" in query:
        speak("You are always welcome, sir!")

    elif "joke" in query:
        speak(random.choice(JOKES))

    # Time & Date
    elif "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}, sir.")

    elif "date" in query or "day" in query:
        now = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {now}, sir.")

    # Media & Searches
    elif "play" in query and "youtube" in query:
        song = query.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        speak(f"Playing {song} on YouTube.")
        search_youtube(song)

    elif "youtube" in query:
        term = query.replace("open youtube", "").replace("search on youtube", "").replace("youtube", "").strip()
        if term:
            speak(f"Searching YouTube for {term}.")
            search_youtube(term)
        else:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "google" in query or "search for" in query:
        term = query.replace("search on google", "").replace("search for", "").replace("google", "").strip()
        if term:
            speak(f"Searching Google for {term}.")
            search_google(term)
        else:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

    elif "open github" in query:
        speak("Opening GitHub.")
        webbrowser.open("https://www.github.com")

    elif "open chatgpt" in query:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chatgpt.com")

    elif "open whatsapp" in query:
        speak("Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com")

    elif "open spotify" in query:
        speak("Opening Spotify.")
        webbrowser.open("https://open.spotify.com")

    elif "open netflix" in query:
        speak("Opening Netflix.")
        webbrowser.open("https://open.netflix.com")

    # Wikipedia Knowledge
    elif "who is" in query or "what is" in query or "tell me about" in query or "wikipedia" in query:
        term = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        if term and wikipedia:
            speak(f"Searching Wikipedia for {term}...")
            try:
                results = wikipedia.summary(term, sentences=2)
                speak("According to Wikipedia: " + results)
            except Exception:
                speak(f"Could not find direct summary. Searching Google for {term}.")
                search_google(term)
        else:
            speak("What would you like me to look up?")

    # System Applications
    elif "open notepad" in query:
        speak(open_app("notepad"))

    elif "open calculator" in query or "open calc" in query:
        speak(open_app("calculator"))

    elif "open cmd" in query or "open command prompt" in query:
        speak(open_app("cmd"))

    elif "open paint" in query:
        speak(open_app("paint"))

    elif "open camera" in query:
        speak(open_app("camera"))

    elif "open file explorer" in query or "open explorer" in query:
        speak(open_app("explorer"))

    elif "open task manager" in query:
        speak(open_app("task manager"))

    # Screenshot & Controls
    elif "screenshot" in query:
        speak("Taking screenshot now, sir.")
        res = take_screenshot()
        speak("Screenshot taken and saved.")

    elif "volume up" in query:
        if pyautogui:
            for _ in range(5):
                pyautogui.press("volumeup")
            speak("Volume increased.")

    elif "volume down" in query:
        if pyautogui:
            for _ in range(5):
                pyautogui.press("volumedown")
            speak("Volume decreased.")

    elif "mute" in query:
        if pyautogui:
            pyautogui.press("volumemute")
            speak("Volume muted.")

    # Exit
    elif any(exit_cmd in query for exit_cmd in ["exit", "quit", "goodbye", "bye jarvis", "shutdown", "stop"]):
        speak("Shutting down systems. Goodbye sir, have a great day!")
        time.sleep(1)
        sys.exit(0)

    # Fallback
    else:
        speak(f"Searching Google for {query}, sir.")
        search_google(query)


# ---------------------------------------------------------
# MAIN EXECUTION LOOP
# ---------------------------------------------------------
def main():
    print("=" * 60)
    print("           JARVIS AI VOICE ASSISTANT           ")
    print("=" * 60)
    print("[1] Voice Mode: Speak through your microphone")
    print("[2] Text Mode: Type commands directly")
    print("=" * 60)
    
    speak("Hello sir! Jarvis is online and ready for your commands.")

    while True:
        try:
            print("\nOptions: Press [ENTER] to speak, or type your command (or 'exit' to quit):")
            user_input = input(">> ").strip()

            if user_input == "":
                # Voice mode
                query = take_command()
                if query:
                    process_command(query)
                else:
                    speak("I didn't hear anything, sir. Please try again.")
            else:
                # Text mode
                process_command(user_input.lower())

        except (KeyboardInterrupt, SystemExit):
            speak("Goodbye, sir!")
            break
        except Exception as e:
            print(f"[Error]: {e}")

if __name__ == "__main__":
    main()
