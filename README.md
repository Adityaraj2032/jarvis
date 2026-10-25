# Jarvis - AI Voice & Desktop Assistant

An intelligent, full-featured AI Voice Assistant built with Python, Eel, Web Technologies (HTML5/CSS3/JS), SiriWave, and SAPI5 TTS speech engine.

---

## 🚀 Features

- **🎙️ Voice Recognition**: Real-time microphone listening via Google Speech Recognition API & Web Speech API fallback.
- **🔊 Natural Voice Output**: Offline Windows SAPI5 TTS (`pyttsx3`) with Microsoft David & Zira voices.
- **🌐 Web Navigation & Search**:
  - *"Open YouTube"* / *"Play [song name] on YouTube"*
  - *"Open Google"* / *"Search Google for [query]"*
  - *"Open GitHub"*, *"Open ChatGPT"*, *"Open WhatsApp"*, *"Open Spotify"*, *"Open Netflix"*, *"Open Reddit"*
- **📚 Wikipedia Knowledge Base**:
  - *"Who is [person]"* / *"What is [topic]"* / *"Wikipedia [term]"* (reads concise summaries aloud).
- **💻 Desktop System Control**:
  - *"Open Notepad"*, *"Open Calculator"*, *"Open CMD"*, *"Open Paint"*, *"Open Camera"*, *"Open File Explorer"*, *"Open Task Manager"*
  - *"Volume Up"*, *"Volume Down"*, *"Mute"*
  - *"Take Screenshot"* (saves automatically to your Pictures/Desktop directory)
- **⏰ Clock & Calendar**:
  - *"What time is it?"*, *"What is today's date?"*
- **💬 Smart Conversational AI**:
  - Greetings (*"Hello"*, *"Good morning"*, *"How are you?"*, *"Who are you?"*, *"Tell me a joke"*)
  - Graceful exit (*"Goodbye"*, *"Exit"*, *"Shutdown"*)
- **🎨 Sci-Fi Cyberpunk UI**:
  - 3D particle sphere rotating core
  - Animated SiriWave soundwave visualizer
  - Interactive commands & help guide modal
  - Dual Input: Voice (Microphone button or `Ctrl+J`) or Typing in the text bar.

---

## 📂 Project Structure

```
jarvis/
├── main.py                     # Main Eel application entry point
├── jarvis_voice_assistant.py   # Standalone All-In-One Voice Assistant script
├── run_jarvis.bat              # 1-Click launcher
├── requirements.txt            # Python dependencies
├── engine/
│   ├── command.py              # Voice commands router, TTS (speak), STT (takecommand)
│   └── features.py             # App launching, web searches, screenshot, volume
└── www/
    ├── index.html              # Futuristic Jarvis Core & SiriWave UI
    ├── main.js                 # Frontend event listeners, Eel exposed functions
    ├── script (1).js           # 3D Particle canvas visualizer
    ├── style.css               # Cyberpunk styling, glowing effects, animations
    └── assests/
        ├── audio/              # Jarvis startup chime
        └── vendore/            # Local libraries (Textillate, SiriWave, fonts)
```

---

## 🏃‍♂️ How to Run

### Method 1: 1-Click Launcher (Recommended)
Simply double-click:
```
run_jarvis.bat
```

### Method 2: Command Line
Open PowerShell or Command Prompt in the project folder and run:
```powershell
.\envjarvis\Scripts\python.exe main.py
```
Or for the standalone console voice assistant:
```powershell
.\envjarvis\Scripts\python.exe jarvis_voice_assistant.py
```

---

## 🎙️ Keyboard Shortcut
- Press **Ctrl + J** at any time in the app to immediately activate voice listening!
