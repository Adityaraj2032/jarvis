import os
import threading
import webbrowser
import subprocess
import pyautogui
import wikipedia
from playsound import playsound

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def playAssistantSound():
    """Play the assistant startup sound asynchronously."""
    sound_file = os.path.join(BASE_DIR, "www", "assests", "audio", "hmrakibulislamsawon-opening-523508.mp3")
    if os.path.exists(sound_file):
        def _play():
            try:
                playsound(sound_file)
            except Exception as e:
                print(f"[Sound Error] {e}")
        threading.Thread(target=_play, daemon=True).start()
    else:
        print(f"[Sound Warning] Sound file not found: {sound_file}")

def open_website(url):
    """Open a URL in the default web browser."""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"[Browser Error] {e}")
        return False

def search_google(query):
    """Search Google for a given query."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return open_website(search_url)

def search_youtube(query):
    """Search YouTube or play a video directly."""
    yt_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    return open_website(yt_url)

def open_application(app_name):
    """Launch common Windows desktop applications."""
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
        elif "explorer" in app_name or "files" in app_name:
            subprocess.Popen(["explorer.exe"])
            return "Opening File Explorer"
        elif "camera" in app_name:
            subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
            return "Opening Camera"
        elif "task manager" in app_name:
            subprocess.Popen(["taskmgr.exe"])
            return "Opening Task Manager"
        else:
            # Try to launch directly
            subprocess.Popen([app_name], shell=True)
            return f"Launching {app_name}"
    except Exception as e:
        return f"Could not launch {app_name}: {e}"

def take_screenshot():
    """Take a screenshot and save it to the user's Pictures or desktop folder."""
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
        return filepath
    except Exception as e:
        print(f"[Screenshot Error] {e}")
        return None

def adjust_volume(action):
    """Control system audio volume."""
    try:
        if action == "up":
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increased"
        elif action == "down":
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume decreased"
        elif action == "mute":
            pyautogui.press("volumemute")
            return "Volume muted"
    except Exception as e:
        print(f"[Volume Error] {e}")
        return "Could not adjust volume"
