# CloudWhisper Flow - Development Guidelines

## Code Standards

### Python Style
- Follow PEP 8 (Python Enhancement Proposal 8)
- Use 4-space indentation (not tabs)
- Keep lines under 100 characters when possible
- Use descriptive variable names (e.g., `target_language` not `tl`)
- Add docstrings to all functions and classes

### Comments
- Only comment non-obvious logic
- Use comments to explain *why*, not *what*
- Bad: `x = x + 1  # Increment x`
- Good: `retry_count += 1  # Exponential backoff on API timeout`

### Error Handling
- Always wrap API calls in try/except
- Log errors (print to console for debugging)
- Never let exceptions crash the app without user feedback
- Show user-friendly error messages (not stack traces)

### Threading Safety
- Use simple state machine (IDLE → RECORDING → PROCESSING → IDLE)
- Avoid race conditions: only modify state in main thread
- Use threading events for signaling (e.g., `stop_recording_event.set()`)

## Testing Strategy

### Manual Testing (No Automated Tests)
- **Phase 1**: Record 5 seconds, check console output
- **Phase 2**: Run UI, drag window, close cleanly
- **Phase 3**: Press F8, record, watch UI change color
- **Phase 4**: Change language, verify translation
- **Phase 5**: Run .exe on clean Windows, verify all features

### Edge Cases to Test
- Rapid F8 presses (should ignore mid-processing)
- Microphone unplugged (should show error)
- No internet (API timeout, should show error)
- Speaking while already processing (should queue or ignore)
- App closed during recording (should clean up threads)

## Debugging

### Console Output
- Development: `print()` statements for debugging
- Production: No debug output (clean console)
- Phase 1 script has verbose output; main.py should be silent unless errors

### Logs
- Consider adding simple file logging if issues are hard to reproduce
- Log location: `CloudWhisperFlow_debug.log` in app directory
- Not required for v1.0, but useful for troubleshooting

## Dependency Management

### requirements.txt
```
flet>=0.20.0
SpeechRecognition==3.10.0
deep-translator==1.11.4
pyaudio==0.2.13
keyboard>=0.13.5
pyautogui>=0.9.53
```

### Pinned Versions
- Pin SpeechRecognition and deep-translator (stable versions)
- Allow minor version flexibility for others (e.g., `flet>=0.20.0`)
- Test before upgrading

## Configuration (config.json)

### Default Structure
```json
{
  "target_language": "Spanish",
  "source_language": "English",
  "hotkey": "F8"
}
```

### Load on Startup
```python
import json
import os

config_path = "config.json"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
else:
    config = {
        "target_language": "Spanish",
        "source_language": "English",
        "hotkey": "F8"
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
```

### Save on Change
```python
def save_config():
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
```

## Commit Strategy

No frequent commits during development (this is a monolithic single-file app).
Commit only at:
- Phase completion (SUMMARY created)
- Significant milestone (e.g., v1.0 release)
- Major bug fix

**Commit messages:**
- `Phase 01: Console test script and dependency validation`
- `Phase 03: Threading integration and F8 hotkey`
- `v1.0 Release: Standalone CloudWhisperFlow.exe ready`

## Known Bugs & Workarounds

### `pyaudio` Installation
- **On Mac**: May need `brew install portaudio` first
- **On Linux**: May need system libraries (ALSA, PulseAudio)
- **Workaround**: Swap `pyaudio` for `sounddevice` if needed

### Google Speech API Rate Limiting
- **Symptom**: "API error: 50x Server Error"
- **Cause**: Exceeded free tier quota
- **Workaround**: Wait 24 hours, or implement Vosk fallback

### Flet Frameless Windows on Some Windows Versions
- **Symptom**: Window shows frame despite `frameless=True`
- **Cause**: Flet/Flutter limitation on older Windows
- **Workaround**: Use standard frame as fallback (less elegant but functional)

## Build & Release Checklist

Before final release:
- [ ] All 5 phases complete
- [ ] main.py runs without errors in dev
- [ ] requirements.txt complete and tested
- [ ] icon.ico created (32x32 or 64x64)
- [ ] `flet pack main.py --icon icon.ico` succeeds
- [ ] .exe tested on clean Windows machine
- [ ] All features functional in .exe (F8, STT, translation, text injection)
- [ ] RELEASE.md written with clear instructions
- [ ] Git commit: "v1.0 Release"

## Performance Optimization (Not v1.0)

For future versions, if performance becomes an issue:
- Cache language list (don't reload from API)
- Pre-compile regex patterns (if used)
- Consider lazy-loading heavy modules (e.g., `pyautogui`)

**Not priority for v1.0** - this is a lightweight desktop app, not a high-traffic service.

## Accessibility

- Floating widget should be visible and moveable
- Settings should be simple (no complex nested menus)
- Error messages should be clear
- Future: Keyboard-only navigation (if needed)

Not a priority for v1.0, but good to keep in mind.
