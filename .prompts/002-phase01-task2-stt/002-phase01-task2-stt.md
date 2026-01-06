# Task 2: Console Script - Audio Recording & STT (Vosk) - CloudWhisper Flow Phase 01

## Objective
Build the first proof-of-concept script: `console_test.py`. This script will record 5 seconds of audio from the microphone and transcribe it to text using **Vosk** (free, offline, local model).

**Context:** Task 1 established the environment. Task 2 validates that STT (Speech-To-Text) works with Vosk offline model. This is the foundation for Phase 01's proof-of-concept.

**Important Change:** Original plan used Google Speech API (paid after free tier). We switched to **Vosk** to maintain "100% free" requirement.

## Scope
- Create `console_test.py` that records 5 seconds of microphone audio
- Send audio to Vosk (offline speech recognition, no internet needed)
- Print transcribed text to console
- Handle errors gracefully (no microphone, model download issues)
- No UI, no translation, no text injection yet (Tasks 3-4)

**Out of scope:** Text translation (Task 3), user configuration (Tasks 4), UI/packaging (Phases 2-5).

## Requirements

### Deliverables
1. **`requirements.txt` UPDATE** - Add vosk:
   ```
   sounddevice==0.4.6
   numpy>=1.21.0
   vosk==0.3.45
   ```
   (Remove `SpeechRecognition` if it was there)

2. **`console_test.py`** - Executable script that:
   - Records 5 seconds of audio from default microphone
   - Passes audio to Vosk speech recognizer
   - Prints transcribed text
   - Handles errors gracefully

3. **Error handling** for:
   - No microphone available
   - Vosk model download/initialization errors
   - Invalid audio (silence, noise)
   - Any other exceptions

4. **Output format** (to console):
   ```
   Recording... (please speak)
   [waits 5 seconds]
   Transcription complete!
   Text: "Hello world this is a test"
   ```

### Success Criteria
- ✅ `requirements.txt` updated (vosk added)
- ✅ `pip install vosk` completes successfully
- ✅ `console_test.py` created in project root
- ✅ Script runs: `python console_test.py`
- ✅ Records 5 seconds of audio (shows "Recording..." message)
- ✅ Vosk transcribes audio locally
- ✅ Prints transcribed text correctly
- ✅ Handles microphone errors (prints clear message, doesn't crash)
- ✅ Clean code with docstring and comments

### Testing Procedure
```bash
# Update requirements with vosk
pip install vosk

# Run the script
python console_test.py

# Expected output:
# Recording for 5 seconds... (please speak)
# [waits ~5 seconds while you speak]
# Transcription complete!
# Text: "Your transcribed speech here"
```

**Test scenarios:**
1. ✅ Speak clearly for 5 seconds → should transcribe correctly
2. ✅ Stay silent for 5 seconds → should transcribe as empty or very short text
3. ✅ Unplug microphone before running → should show clear error (no microphone)

---

## Technical Implementation Details

### Libraries Used
- **`vosk`** - Offline speech recognition (free, local model)
- **`sounddevice`** - Records audio from microphone
- **`numpy`** - Handles audio data as arrays

### Why Vosk?
- **Free:** No API costs, no rate limits
- **Offline:** No internet required, fully local
- **Lightweight:** ~50MB model (auto-downloaded on first run)
- **Python 3.12+ compatible:** Works without C++ compilation issues
- **Trade-off:** Accuracy is lower than cloud APIs (Google, Whisper), but acceptable for v1.0

### Recording Setup
Use `sounddevice` to capture 5 seconds of audio at 16kHz:

```python
import sounddevice as sd
import numpy as np

# Parameters
DURATION = 5  # seconds
SAMPLE_RATE = 16000  # Hz (standard for speech recognition)

# Record audio
audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
sd.wait()  # Wait for recording to complete

# audio_data is now a numpy array (shape: (num_samples, 1))
```

### Vosk Initialization & Transcription
```python
import vosk
import json

# Initialize recognizer
recognizer = vosk.KaldiRecognizer(vosk.Model.from_file(...), SAMPLE_RATE)

# Process audio
recognizer.AcceptWaveform(audio_bytes)
result = json.loads(recognizer.Result())

# Extract text from result
if "result" in result and result["result"]:
    text = " ".join([word["conf"] for word in result["result"]])
else:
    text = ""  # Silence or no speech detected
```

**Important:** Vosk downloads model on first run (~50MB). May take a minute on first execution.

### Error Handling Strategy
Wrap in try/except to catch:
- `sounddevice` errors (no microphone)
- `vosk` model errors (download failure)
- Audio data errors (wrong format)
- Any unexpected exceptions

Print user-friendly messages, not stack traces.

---

## Code Structure Recommendation

```python
"""
CloudWhisper Flow - Console Test Script (Phase 01, Task 2)
Records 5 seconds of audio and transcribes to text using Vosk (offline).
"""

import sounddevice as sd
import numpy as np
import vosk
import json
import sys

# Constants
DURATION = 5
SAMPLE_RATE = 16000

def record_audio(duration=DURATION, sample_rate=SAMPLE_RATE):
    """Record audio from microphone. Returns numpy array."""
    try:
        print(f"Recording for {duration} seconds... (please speak)")
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
        sd.wait()
        return audio_data.flatten()  # Flatten to 1D array
    except Exception as e:
        print(f"Recording error: {e}")
        return None

def transcribe_audio(audio_data):
    """Transcribe audio using Vosk (offline)."""
    try:
        # Initialize Vosk model
        model = vosk.Model.from_file()  # Auto-downloads on first run
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        
        # Convert numpy array to bytes for Vosk
        audio_bytes = (audio_data * 32767).astype(np.int16).tobytes()
        
        # Process audio in chunks
        recognizer.AcceptWaveform(audio_bytes)
        result_str = recognizer.FinalResult()
        
        # Extract text from JSON result
        result = json.loads(result_str)
        if "result" in result:
            return " ".join([word["conf"] for word in result["result"]])
        return ""
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def main():
    """Main flow: Record → Transcribe → Print."""
    try:
        audio = record_audio()
        if audio is None:
            return
        
        print("Transcribing...")
        text = transcribe_audio(audio)
        
        if text:
            print(f"Transcription complete!")
            print(f"Text: {text}")
        else:
            print("No speech detected or transcription failed")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Potential Issues & Workarounds

### Issue: Vosk model download hangs or fails
- **Cause**: Network issue or disk space issue
- **Fix**: Check internet connection, ensure >200MB free disk space
- **Manual download**: Download model separately if needed

### Issue: Audio quality too low or too high
- **Cause**: Microphone volume settings or audio clipping
- **Debug**: Print audio array stats (min/max values)
- **Standard**: 16kHz mono is widely supported

### Issue: "Could not understand audio" (silent recording)
- **Expected**: Script should handle gracefully
- **Output**: Should print "No speech detected" and exit cleanly
- **Not a failure**: This is expected error handling

### Issue: Vosk not found after pip install
- **Cause**: Virtual environment issue or install failure
- **Fix**: `pip install --upgrade vosk`
- **Verify**: `python -c "import vosk; print(vosk.__version__)"`

---

## Output Specification

Create `SUMMARY.md` in the `.prompts/002-phase01-task2-stt/` folder with:

### Required Sections
1. **One-liner** - Substantive summary
   - Example: "Console STT proof-of-concept complete: Records 5 seconds, transcribes via Vosk (offline), handles errors gracefully"

2. **Status** - ✅ (success) or ❌ (failed)

3. **What Was Done**
   - Updated `requirements.txt` with vosk
   - Created `console_test.py`
   - Implemented 5-second audio recording with sounddevice
   - Integrated Vosk offline speech recognition
   - Added error handling

4. **Testing Results**
   - Test 1: Spoke clearly → [show transcribed text]
   - Test 2: Stayed silent → [show handling]
   - Test 3: Microphone error test → [show error message]
   - Vosk model download time (first run)

5. **Code Quality**
   - Docstring present
   - Comments on non-obvious logic
   - Code is readable and follows PEP 8

6. **Decisions Made**
   - Vosk vs. alternatives (why Vosk chosen)
   - Any workarounds applied
   - Otherwise: "None - straightforward implementation"

7. **Blockers**
   - Any issues encountered and unresolved
   - Otherwise: "None - ready for Task 3"

8. **Next Step**
   - "Execute Task 3: Add Translation (English → Spanish using deep-translator)"

---

## Instructions for Execution

1. **Update requirements.txt**: Add `vosk==0.3.45`
2. **Install vosk**: `pip install vosk` (will also download model on first run)
3. **Implement functions**: `record_audio()`, `transcribe_audio()`, `main()`
4. **Test locally**: Run `python console_test.py` and speak into microphone
5. **Handle errors**: Ensure script doesn't crash on errors
6. **Clean up**: Remove debug prints, ensure output is user-friendly
7. **Document**: Add docstring and comments
8. **Create SUMMARY.md**: Fill template with results
9. **Git status**: `console_test.py` and updated `requirements.txt` will be ready to commit

---

## Important Notes

- **No translation yet**: Task 2 is ONLY audio recording + STT. Translation is Task 3.
- **Vosk is offline**: No internet needed. Model auto-downloads on first run (~50MB).
- **5 seconds is arbitrary**: Could be longer/shorter; 5 is chosen for quick testing.
- **Vosk accuracy**: Good for most use cases. Future versions can add Whisper Local (better) if needed.
- **First run delay**: Model download may take 1-2 minutes on first run.

---

## Quality Checklist (Before Declaring Success)

- [ ] `requirements.txt` updated with vosk
- [ ] `pip install vosk` completes successfully
- [ ] `console_test.py` file created in project root
- [ ] Script runs without errors: `python console_test.py`
- [ ] Records 5 seconds of audio (user sees "Recording..." message)
- [ ] Vosk model initializes (downloads on first run if needed)
- [ ] Prints transcribed text (actual speech converted to text)
- [ ] Handles no-microphone error gracefully
- [ ] Handles silent/unclear audio gracefully
- [ ] Code has docstring at top
- [ ] Non-obvious logic has comments
- [ ] Output is user-friendly (no stack traces in error cases)
- [ ] SUMMARY.md created with all required sections
- [ ] Testing results documented (at least 2 test runs)
- [ ] Next step clearly states "Execute Task 3"

---

## Output Location

Save summary to: `.prompts/002-phase01-task2-stt/SUMMARY.md`

---

## Phase 01 Progress

- ✅ Task 1: Environment setup (COMPLETE - sounddevice, numpy, etc.)
- 🔄 **Task 2: Audio Recording & STT with Vosk (THIS TASK)**
- ⏳ Task 3: Translation (blocked on Task 2)
- ⏳ Task 4: Output & Cleanup (blocked on Task 3)

After Task 2 complete, all pieces of Phase 01 proof-of-concept will be ready to integrate.
