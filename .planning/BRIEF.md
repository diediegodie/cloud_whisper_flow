# CloudWhisper Flow - Project Brief

## Vision
Build a lightweight, desktop "floating dictation widget" that listens to voice input, transcribes it to text, optionally translates it, and types the result into any active application. **100% free and lightweight** - no heavy local AI models required.

## Core Requirements
- **Language:** Python 3.10+
- **UI Framework:** Flet (modern, transparent, frameless floating widget)
- **Distribution:** Standalone `.exe` via `flet pack`
- **Architecture:** Single-process (UI + Logic in one file)
- **Cost:** Free (relies on free Google APIs)
- **Internet:** Required (for STT and translation APIs)

## Key Features
1. **Floating Widget** - Always-on-top window showing app state (Ready/Recording/Thinking)
2. **Global Hotkey Listener** - Trigger recording with F8 (even when minimized)
3. **Voice Recording** - Capture microphone input via `pyaudio`
4. **Cloud Transcription** - Send audio to Google Speech API (free, via `SpeechRecognition`)
5. **Optional Translation** - Translate to target language via Google Translate (free, via `deep-translator`)
6. **Text Injection** - Type result at cursor position using `pyautogui`

## Tech Stack
| Component | Library | Purpose |
|-----------|---------|---------|
| UI | `flet` | Floating widget interface |
| STT | `SpeechRecognition` | Transcribe audio to text |
| Translation | `deep-translator` | Translate text (Google Translate backend) |
| Audio | `pyaudio` | Microphone access |
| Hotkeys | `keyboard` | Global F8 listener |
| Text Input | `pyautogui` | Type text into active window |

## Application Flow
```
1. Idle → Listen for F8 (background thread)
2. F8 Pressed → Start recording
3. Recording → Capture audio, detect silence
4. Audio → Send to Google Speech API
5. Text Received → If translation enabled, translate
6. Result → Type into cursor position
```

## Contingency Options
If free APIs break, have backups:
- **STT**: Vosk (local, offline) or OpenAI Whisper (paid)
- **Translation**: `translators` lib or `googletrans`
- **Audio**: `sounddevice` (if `pyaudio` fails)

## Current Status
- ✅ Specification complete
- ⏳ Implementation not started
- No planning structure yet

## Success Criteria
- v1.0: Single-process app with F8 trigger, STT, optional translation, text injection
- Standalone `.exe` runs on Windows without dependencies
- Recording → transcription → output takes <5 seconds
- Handles multiple languages smoothly
- Clean, minimal UI (floating widget always visible)

## Next Steps
Create development roadmap with 5 phases:
1. Console proof-of-concept (logic validation)
2. Flet UI skeleton (visual widget)
3. Integration (logic + UI threading)
4. Configuration (language settings)
5. Packaging (standalone `.exe`)
