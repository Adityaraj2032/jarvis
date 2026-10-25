import os
import sys
import time
import random
import datetime
import pythoncom
import pyttsx3
import eel
import speech_recognition as sr
import wikipedia
from engine.features import (
    open_website,
    search_google,
    search_youtube,
    open_application,
    take_screenshot,
    adjust_volume
)

# Text-to-Speech Engine Initialization
def init_tts():
    pythoncom.CoInitialize()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    return engine

@eel.expose
def speak(text):
    """Speaks the text aloud and updates the web UI."""
    text = str(text)
    print(f"[Jarvis]: {text}")
    
    try:
        eel.DisplayMessage(text)
        eel.sleep(0.05)
    except Exception as e:
        print(f"[UI Display Error]: {e}")
        
    try:
        engine = init_tts()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error]: {e}")

@eel.expose
def takecommand():
    """Listens for voice input from the user's microphone and converts to text."""
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    
    try:
        with sr.Microphone() as source:
            print("\n[Jarvis]: Listening for voice input...")
            try:
                eel.DisplayMessage("Listening...")
                eel.sleep(0.05)
            except Exception:
                pass
                
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                print("[Jarvis]: Listening timed out.")
                return ""
    except Exception as mic_err:
        print(f"[Microphone Error]: {mic_err}")
        return ""

    try:
        print("[Jarvis]: Recognizing speech...")
        try:
            eel.DisplayMessage("Recognizing...")
            eel.sleep(0.05)
        except Exception:
            pass
            
        query = r.recognize_google(audio, language='en-in')
        print(f"[User]: {query}")
        try:
            eel.DisplayMessage(query)
            eel.sleep(0.05)
        except Exception:
            pass
        return query.lower().strip()
    except sr.UnknownValueError:
        print("[Jarvis]: Could not understand audio.")
        return ""
    except Exception as e:
        print(f"[Speech Recognition Error]: {e}")
        return ""

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Java programmers have to wear glasses? Because they don't C sharp!",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
    "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings!"
]

def _run_command_pipeline(message=1):
    """Worker function that processes commands without blocking the Eel event loop."""
    try:
        eel.ShowWave()
        eel.sleep(0.05)
    except Exception:
        pass

    if message == 1 or message is None or str(message).strip() == "":
        query = takecommand()
    else:
        query = str(message).lower().strip()

    print(f"[Processing Command]: {query}")

    if not query:
        speak("I didn't catch that, sir. Please try again.")
        time.sleep(1)
        try:
            eel.ShowHood()
        except Exception:
            pass
        return

    # 1. Greetings & Conversation
    if any(greet in query for greet in ["hello jarvis", "hi jarvis", "hey jarvis", "hello", "hi"]):
        responses = [
            "Hello sir! How can I assist you today?",
            "Greetings, sir! Systems are primed and ready.",
            "Hello! I am listening. What can I do for you?"
        ]
        speak(random.choice(responses))

    elif "how are you" in query:
        speak("I am functioning at peak efficiency, sir! How are you doing today?")

    elif "who are you" in query or "what is your name" in query:
        speak("I am Jarvis, your personal AI voice assistant. Always ready to assist you.")

    elif "what can you do" in query or "help" in query:
        speak("I can open websites, search YouTube and Google, tell time and date, check Wikipedia, open desktop applications, take screenshots, and tell jokes!")

    elif "who created you" in query or "who made you" in query:
        speak("I was created to be your intelligent AI companion, powered by Python and modern web technology.")

    elif "thank you" in query or "thanks" in query:
        speak("You are most welcome, sir! It is my pleasure to assist.")

    elif "tell me a joke" in query or "joke" in query:
        speak(random.choice(JOKES))

    # 2. Time & Date
    elif "time" in query:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"Sir, the current time is {current_time}.")

    elif "date" in query or "day" in query:
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}, sir.")

    # 3. Web Navigation & Searches
    elif "play" in query and "youtube" in query:
        song = query.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        speak(f"Playing {song} on YouTube, sir.")
        search_youtube(song)

    elif "youtube" in query:
        search_term = query.replace("open youtube", "").replace("search on youtube", "").replace("youtube", "").strip()
        if search_term:
            speak(f"Searching YouTube for {search_term}.")
            search_youtube(search_term)
        else:
            speak("Opening YouTube, sir.")
            open_website("https://www.youtube.com")

    elif "open google" in query:
        speak("Opening Google, sir.")
        open_website("https://www.google.com")

    elif "google" in query or "search for" in query or "search on google" in query:
        term = query.replace("search on google", "").replace("search google for", "").replace("search for", "").replace("google", "").strip()
        if term:
            speak(f"Searching Google for {term}.")
            search_google(term)
        else:
            speak("Opening Google.")
            open_website("https://www.google.com")

    elif "open github" in query:
        speak("Opening GitHub, sir.")
        open_website("https://www.github.com")

    elif "open chatgpt" in query:
        speak("Opening ChatGPT, sir.")
        open_website("https://chatgpt.com")

    elif "open whatsapp" in query:
        speak("Opening WhatsApp Web, sir.")
        open_website("https://web.whatsapp.com")

    elif "open spotify" in query:
        speak("Opening Spotify, sir.")
        open_website("https://open.spotify.com")

    elif "open netflix" in query:
        speak("Opening Netflix, sir.")
        open_website("https://open.netflix.com")

    elif "open instagram" in query:
        speak("Opening Instagram, sir.")
        open_website("https://www.instagram.com")

    elif "open facebook" in query:
        speak("Opening Facebook, sir.")
        open_website("https://www.facebook.com")

    elif "open twitter" in query or "open x" in query:
        speak("Opening X, sir.")
        open_website("https://www.x.com")

    elif "open reddit" in query:
        speak("Opening Reddit, sir.")
        open_website("https://www.reddit.com")

    # 4. Wikipedia / Knowledge
    elif "who is" in query or "what is" in query or "tell me about" in query or "wikipedia" in query:
        term = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        if term:
            speak(f"Searching Wikipedia for {term}...")
            try:
                results = wikipedia.summary(term, sentences=2)
                speak("According to Wikipedia: " + results)
            except Exception as e:
                print(f"[Wikipedia Warning]: {e}")
                speak(f"I couldn't find a direct summary, so let me search Google for {term}.")
                search_google(term)
        else:
            speak("What topic would you like me to look up, sir?")

    # 5. System Applications
    elif "open notepad" in query:
        speak(open_application("notepad"))

    elif "open calculator" in query or "open calc" in query:
        speak(open_application("calculator"))

    elif "open cmd" in query or "open command prompt" in query:
        speak(open_application("cmd"))

    elif "open paint" in query:
        speak(open_application("paint"))

    elif "open camera" in query:
        speak(open_application("camera"))

    elif "open file explorer" in query or "open explorer" in query:
        speak(open_application("explorer"))

    elif "open task manager" in query:
        speak(open_application("task manager"))

    # 6. Volume & Controls
    elif "volume up" in query or "increase volume" in query:
        speak(adjust_volume("up"))

    elif "volume down" in query or "decrease volume" in query or "lower volume" in query:
        speak(adjust_volume("down"))

    elif "mute" in query or "unmute" in query:
        speak(adjust_volume("mute"))

    elif "take screenshot" in query or "screenshot" in query:
        speak("Taking screenshot now, sir.")
        saved_path = take_screenshot()
        if saved_path:
            speak("Screenshot successfully saved to your Pictures folder.")
        else:
            speak("Sorry sir, I was unable to capture the screenshot.")

    # 7. Exit / Shutdown
    elif any(exit_cmd in query for exit_cmd in ["exit", "quit", "goodbye", "bye jarvis", "shutdown", "stop"]):
        speak("Shutting down systems. Goodbye, sir. Have a wonderful day!")
        time.sleep(1)
        os._exit(0)

    # 8. Fallback Smart Web Search
    else:
        speak(f"I am searching for {query} on Google, sir.")
        search_google(query)

    # Return UI back to ready core view after a brief pause
    time.sleep(1.2)
    try:
        eel.ShowHood()
    except Exception:
        pass

@eel.expose
def allCommands(message=1):
    """Spawns the command execution asynchronously so UI never hangs."""
    eel.spawn(_run_command_pipeline, message)
