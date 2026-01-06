# Task 2: Console Script - Audio Recording & STT - CloudWhisper Flow Phase 01

## Objective
Build the first proof-of-concept script: `console_test.py`. This script will record 5 seconds of audio from the microphone and transcribe it to text using Google's free Speech API.

**Context:** Task 1 established the environment (all dependencies installed). Task 2 validates that STT (Speech-To-Text) works with actual microphone input and cloud API integration. This is the foundation for Phase 01's proof-of-concept.

## Scope
- Create `console_test.py` that records 5 seconds of microphone audio
- Send audio to Google Speech API (via `SpeechRecognition` library)
- Print transcribed text to console
- Handle errors gracefully (no microphone, network timeout, API errors)
- No UI, no text injection, no translation yet (those are Tasks 3-4)

**Out of scope:** Text translation (Task 3), user configuration (Tasks 4), UI/packaging (Phases 2-5).

## Requirements

### Deliverables
1. **`console_test.py`** - Executable script that:
   - Records 5 seconds of audio from default microphone
   - Sends audio to Google Speech API
   - Prints transcribed text
   - Handles errors gracefully

2. **Error handling** for:
   - No microphone available
   - API timeout/network errors
   - Invalid audio (silence, noise)
   - Any other exceptions

3. **Output format** (to console):
   ```
   Recording... (please speak)
   [waits 5 seconds]
   Transcription complete!
   Text: "Hello world this is a test"
   ```

### Success Criteria
- ✅ `console_test.py` created in project root
- ✅ Script runs: `python console_test.py`
- ✅ Records 5 seconds of audio (shows "Recording..." message)
- ✅ Sends to Google Speech API
- ✅ Prints transcribed text correctly
- ✅ Handles microphone errors (prints clear message, doesn't crash)
- ✅ Handles API errors (prints clear message, doesn't crash)
- ✅ Clean code with docstring and comments on non-obvious logic

### Testing Procedure
```bash
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
4. ✅ Disconnect internet → should show timeout error

---

## Technical Implementation Details

### Libraries Used
- **`sounddevice`** - Records audio from microphone
- **`numpy`** - Handles audio data as arrays
- **`speech_recognition`** - Sends audio to Google Speech API, gets text back

### Recording Setup
Use `sounddevice` to capture 5 seconds of audio at 16kHz (standard for speech recognition):

```python
import sounddevice as sd
import numpy as np

# Parameters
DURATION = 5  # seconds
SAMPLE_RATE = 16000  # Hz (standard for speech recognition)

# Record audio
audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
sd.wait()  # Wait for recording to complete

# audio_data is now a numpy array
```

### Convert to SpeechRecognition Format
`SpeechRecognition` expects `AudioData` objects. Create one from numpy array:

```python
import speech_recognition as sr

# Create recognizer
recognizer = sr.Recognizer()

# Convert numpy array to WAV bytes
# (There are multiple ways; below is straightforward)
# Option: Use scipy.io.wavfile or io.BytesIO
# Simpler option: just pass audio_data directly to recognizer.recognize_google()

# Actually, speech_recognition can work with raw audio:
# audio = sr.AudioData(audio_data.tobytes(), SAMPLE_RATE, 2)
```

**Note:** The exact conversion depends on `speech_recognition` version. May need to:
- Convert numpy array to bytes
- Create `AudioData` object
- Pass to `recognize_google()`

### Google Speech API Call
```python
try:
    text = recognizer.recognize_google(audio)
    print(f"Text: {text}")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"API Error: {e}")
```

### Error Handling Strategy
Wrap in try/except to catch:
- `sounddevice` errors (no microphone)
- `speech_recognition` errors (API timeout, unknown audio)
- Network errors
- Any unexpected exceptions

Print user-friendly messages, not stack traces.

---

## Code Structure Recommendation

```python
"""
CloudWhisper Flow - Console Test Script (Phase 01, Task 2)
Records 5 seconds of audio and transcribes to text using Google Speech API.
"""

import sounddevice as sd
import numpy as np
import speech_recognition as sr

# Constants
DURATION = 5
SAMPLE_RATE = 16000

def record_audio(duration=DURATION, sample_rate=SAMPLE_RATE):
    """Record audio from microphone."""
    # Implementation here
    pass

def transcribe_audio(audio_data):
    """Send audio to Google Speech API and get text."""
    # Implementation here
    pass

def main():
    """Main flow: Record → Transcribe → Print."""
    try:
        print("Recording for 5 seconds... (please speak)")
        audio = record_audio()
        
        print("Transcribing...")
        text = transcribe_audio(audio)
        
        print(f"Transcription complete!")
        print(f"Text: {text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

---

## Potential Issues & Workarounds

### Issue: `sounddevice` hangs during recording
- **Cause**: Audio device not responding
- **Fix**: Add timeout or let it timeout naturally (5 sec recording)
- **Fallback**: Check if microphone is connected/enabled

### Issue: Google Speech API rejects audio
- **Cause**: Bad audio format, wrong sample rate
- **Standard**: 16kHz mono is widely supported
- **Debug**: Print audio array stats (shape, dtype, min/max values)

### Issue: "Could not understand audio" (silent recording)
- **Expected**: Script should handle gracefully
- **Output**: Should print "Could not understand audio" and exit cleanly
- **Not a failure**: This is expected error handling

### Issue: Network timeout
- **Cause**: Internet connection slow/down
- **Timeout value**: `SpeechRecognition` has default timeout (~10s)
- **Error message**: Print "Network error: API timeout"

### Issue: Multiple microphones/audio devices
- **Current approach**: Use default device (usually the right one)
- **Advanced**: Could add `--device` command-line arg (Task 4)
- **For now**: Keep simple, use default

---

## Output Specification

Create `SUMMARY.md` in the `.prompts/002-phase01-task2-stt/` folder with:

### Required Sections
1. **One-liner** - Substantive summary
   - Example: "Console proof-of-concept complete: Records 5 seconds, transcribes via Google Speech API, handles errors gracefully"

2. **Status** - ✅ (success) or ❌ (failed)

3. **What Was Done**
   - Created `console_test.py`
   - Implemented 5-second audio recording with sounddevice
   - Integrated Google Speech API via SpeechRecognition
   - Added error handling for microphone/network/API errors

4. **Testing Results**
   - Test 1: Spoke clearly → [show transcribed text]
   - Test 2: Stayed silent → [show "no audio" handling]
   - Test 3: Microphone error test → [show error message]
   - Any other tests run

5. **Code Quality**
   - Docstring present
   - Comments on non-obvious logic
   - Code is readable and follows PEP 8

6. **Decisions Made**
   - Any code structure decisions (function names, parameter choices)
   - Any workarounds applied
   - Otherwise: "None - straightforward implementation"

7. **Blockers**
   - Any issues encountered and unresolved
   - Otherwise: "None - ready for Task 3"

8. **Next Step**
   - "Execute Task 3: Add Translation (English → Spanish)"

---

## Instructions for Execution

1. **Review requirements**: Understand what the script needs to do
2. **Implement functions**: `record_audio()`, `transcribe_audio()`, `main()`
3. **Test locally**: Run `python console_test.py` and speak into microphone
4. **Handle errors**: Ensure script doesn't crash on errors
5. **Clean up**: Remove debug prints, ensure output is user-friendly
6. **Document**: Add docstring and comments
7. **Create SUMMARY.md**: Fill template with results
8. **Git status**: `console_test.py` will be ready to commit

---

## Important Notes

- **No translation yet**: Task 2 is ONLY audio recording + STT. Translation is Task 3.
- **Sounddevice advantage**: Works with Python 3.12+, no C++ compilation needed (unlike pyaudio)
- **Google API is free**: No authentication needed. Uses free tier (rate limited but sufficient for v1.0)
- **5 seconds is arbitrary**: Could be longer/shorter; 5 is chosen for quick testing

---

## Quality Checklist (Before Declaring Success)

- [ ] `console_test.py` file created in project root
- [ ] Script runs without errors: `python console_test.py`
- [ ] Records 5 seconds of audio (user sees "Recording..." message)
- [ ] Sends audio to Google Speech API
- [ ] Prints transcribed text (actual speech translated to text)
- [ ] Handles no-microphone error gracefully
- [ ] Handles API timeout error gracefully
- [ ] Handles silent/unclear audio gracefully (UnknownValueError)
- [ ] Code has docstring at top
- [ ] Non-obvious logic has comments
- [ ] Output is user-friendly (no stack traces in error cases)
- [ ] SUMMARY.md created with all required sections
- [ ] Testing results documented (at least 2 test runs)
- [ ] Next step clearly states "Execute Task 3"

---

## Output Location

Save summary to: `.prompts/002-phase01-task2-stt/SUMMARY.md`

This summary will be reviewed before moving to Task 3 (Translation).

---

## Phase 01 Progress

- ✅ Task 1: Environment setup (COMPLETE)
- 🔄 **Task 2: Audio Recording & STT (THIS TASK)**
- ⏳ Task 3: Translation (blocked on Task 2)
- ⏳ Task 4: Output & Cleanup (blocked on Task 3)

After Task 2 complete, all pieces of Phase 01 proof-of-concept will be ready to integrate.
