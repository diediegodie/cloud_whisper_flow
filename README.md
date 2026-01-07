CloudWhisper Flow — Run & Test Guide

Purpose

This repo contains a console proof-of-concept for offline speech-to-text (Vosk) with optional translation. The main test harness is console_test.py which records from the microphone or processes WAV/MP3 files, transcribes with a local Vosk model, and can translate the result via deep_translator.

Quick prerequisites

- Python 3.8+ (venv recommended)
- ffmpeg (for MP3 → WAV conversion)
- A Vosk model unpacked into ./model or supply an absolute path via --model-path. Example on this machine:
  /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model
- Install Python deps: pip install -r requirements.txt

Key CLI usage

- Record from microphone (default 5s) and translate using language name:
  python console_test.py --lang English --model-path /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model

- Process an audio file and translate using ISO code:
  python console_test.py --file ./audio/sample.wav --translate-target en --model-path /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model

Arguments

- --seconds / -s: recording duration for microphone (default 5)
- --file / -f: path to WAV or MP3 to process (MP3s are converted via ffmpeg)
- --translate-target / -t: language code (e.g., en, pt) for translation
- --lang / -l: language name (e.g., English, Portuguese). Convenience mapping to common ISO codes when --translate-target is not provided
- --model-path: path to Vosk model directory (default: ./model)

Run flow (what the script does)

1. Load Vosk model from --model-path (script exits non-zero if model missing).
2. If --file provided: accept WAV or convert MP3→WAV (ffmpeg); load PCM bytes.
3. Otherwise: record audio from microphone using sounddevice (record, wait, stop to free resources).
4. Transcribe PCM bytes with Vosk and print "Transcription complete!" + the text.
5. If translation requested (via --translate-target or --lang), call deep_translator.GoogleTranslator and print formatted simulated output to console (placeholder for GUI automation).
6. Ensure audio stream is stopped and temporary files (converted WAV) are removed before exiting.

Docker notes

- The Docker configuration in this repo was used for earlier tests; the container often bundles ffmpeg and can mount the model directory. If you previously ran successfully in Docker but not locally, ensure the same model path is available on the host or pass --model-path with the absolute container path.
- Microphone passthrough into containers requires additional host audio bridge configuration; prefer file-based tests inside the container.

Troubleshooting

- ERROR: "Folder 'model' does not contain model files" — download a Vosk model from https://alphacephei.com/vosk/models and unzip into ./model, or run with --model-path pointing to the unpacked model directory.
- If recording hangs or audio resources remain open: verify sounddevice can access audio devices and that the script calls sd.stop(); prefer file-based testing if host audio is unavailable.
- If translation fails: ensure deep-translator is installed and the host has internet access (GoogleTranslator uses network calls).

Verification checklist

1. Confirm model exists: ls /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model/
2. Test file path translation: python console_test.py --file <file.wav> --translate-target en --model-path /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model/
3. Test recording (if host audio available): python console_test.py --seconds 5 --model-path /home/diego/documentos/github/projetos/cloud_whisper_flow_v1/model
4. Confirm script exits and no leftover audio processes (ps aux | grep python; check for stuck sounddevice handles).