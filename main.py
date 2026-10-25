import os
import sys
import time
import socket
import threading
import subprocess
import webbrowser
import eel

from engine.features import playAssistantSound
from engine.command import allCommands, speak, takecommand

def find_available_port(start_port=8000):
    """Finds an available local port starting from start_port."""
    for port in range(start_port, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port

def launch_browser(port):
    """Launch Microsoft Edge, Chrome, or default browser in app mode."""
    time.sleep(1.0)
    url = f"http://localhost:{port}/index.html"
    
    # Candidate browser executable paths on Windows
    candidate_browsers = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    
    launched = False
    for browser_path in candidate_browsers:
        if os.path.exists(browser_path):
            try:
                subprocess.Popen([browser_path, f"--app={url}"])
                print(f"[System]: Interface opened in app mode using {os.path.basename(browser_path)}.")
                launched = True
                break
            except Exception as e:
                print(f"[Browser Launch Warning]: {e}")
                
    if not launched:
        print("[System]: Opening in default browser...")
        webbrowser.open(url)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    www_dir = os.path.join(current_dir, "www")
    
    eel.init(www_dir)

    print("========================================")
    print("       JARVIS AI VOICE ASSISTANT       ")
    print("========================================")
    print("[System]: Initializing systems...")

    # Play startup greeting chime
    playAssistantSound()

    # Find free port
    port = find_available_port(8000)
    print(f"[System]: Starting web interface on http://localhost:{port}/index.html")

    # Launch browser interface in background
    threading.Thread(target=launch_browser, args=(port,), daemon=True).start()

    try:
        eel.start("index.html", mode=None, host='localhost', port=port, block=True)
    except (SystemExit, KeyboardInterrupt):
        print("\n[System]: Jarvis shut down gracefully.")
    except Exception as e:
        print(f"[System Error]: {e}")
