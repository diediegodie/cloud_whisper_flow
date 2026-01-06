# CloudWhisper Flow - Development Stack

## Technology Choices

### Language & Framework
- **Python 3.10+**: Lightweight, fast to develop, great for scripting and desktop apps
- **Flet**: Flutter wrapper for Python; creates modern, frameless, always-on-top windows perfectly suited for floating widgets

### Core Libraries

| Library | Purpose | Why Chosen |
|---------|---------|-----------|
| `SpeechRecognition` | Audio → Text (STT) | Free Google Web Speech API, no authentication needed |
| `deep-translator` | Text → Text (Translation) | Free Google Translate backend, robust and reliable |
| `pyaudio` | Microphone access | Industry standard, integrates with SpeechRecognition |
| `keyboard` | Global hotkey detection | Works even when app is minimized; Linux/Mac/Windows compatible |
| `pyautogui` | Text injection (typing) | Simple, reliable cursor position text injection |
| `flet` | UI framework | Beautiful floating widgets, frameless windows, cross-platform potential |

### Installation Command
```bash
pip install flet SpeechRecognition deep-translator pyaudio keyboard pyautogui
```

## Architecture

### Single-Process Design
All logic (UI + transcription + translation + input) runs in one Python file (`main.py`).

**Rationale:**
- Simple to package as `.exe`
- Easy to debug and maintain
- No inter-process communication overhead
- Minimal resource usage

### Threading Model
- **Main Thread**: Flet UI (must stay responsive)
- **Hotkey Thread**: Background F8 listener (non-blocking)
- **Recording Thread**: Audio capture (blocked during recording, OK)
- **Worker Thread**: STT + Translation (async, UI stays responsive)

**State Machine:**
```
IDLE --[F8 pressed]--> RECORDING
RECORDING --[F8 released / silence]--> PROCESSING
PROCESSING --[done]--> IDLE
```

## API Usage (Free Tier)

### Google Speech API
- Free tier: Limited requests per day (~50)
- No authentication needed (uses `SpeechRecognition` library wrapper)
- Rate limit behavior: Returns errors if exceeded
- **Fallback**: Vosk (local, offline)

### Google Translate (via deep-translator)
- Free tier: ~500k characters/month
- Web scraping API (unofficial, not documented by Google)
- Stability: Generally reliable, but not guaranteed
- **Fallback**: `translators` library (supports Bing, Yandex, Alibaba, Baidu)

## Packaging

### Flet Pack Command
```bash
flet pack main.py --icon icon.ico --name CloudWhisperFlow
```

Produces: `dist/CloudWhisperFlow.exe` (~80-100 MB)

**Bundled by Flet:**
- Python runtime
- All dependencies (if in requirements.txt)
- Flet framework

**Result:** Standalone executable, no Python installation required on user machine.

## File Structure

```
cloud_whisper_flow_v1/
├── .planning/                   # Planning artifacts
│   ├── BRIEF.md
│   ├── ROADMAP.md
│   └── phases/
│       ├── 01-foundation/
│       ├── 02-ui-skeleton/
│       ├── 03-integration/
│       ├── 04-configuration/
│       └── 05-packaging/
├── main.py                      # Main app (Flet UI + Logic)
├── console_test.py              # Phase 01: Logic validation
├── ui_skeleton.py               # Phase 02: UI prototype
├── requirements.txt             # Dependencies
├── config.json                  # User settings (created on first run)
├── icon.ico                     # App icon
├── RELEASE.md                   # Distribution & troubleshooting
└── dist/
    └── CloudWhisperFlow.exe     # Final standalone app
```

## Development Workflow

### Phase 1: Console Testing
- Validate logic without UI
- Test all API integrations
- Prove recorder → transcriber → translator → output works

### Phase 2: UI Skeleton
- Build Flet floating widget
- Test frameless, always-on-top behavior
- Create placeholder for settings

### Phase 3: Integration
- Connect logic (Phase 1) to UI (Phase 2)
- Add F8 hotkey listener
- Implement threading to keep UI responsive
- Test text injection

### Phase 4: Configuration
- Add language selector
- Persist settings to config.json
- Verify translation respects language choice

### Phase 5: Packaging
- Create icon
- Run `flet pack`
- Test `.exe` on clean Windows
- Create RELEASE.md for distribution

## Known Limitations & Workarounds

### `pyaudio` Installation Issues
- **Problem**: Fails to install on some systems (especially Mac/Linux)
- **Workaround**: Use `sounddevice` library instead (slight code change needed)

### Text Injection (`pyautogui`)
- **Limitation**: Doesn't work in all applications (e.g., web-based text editors may have issues)
- **Workaround**: Phase 04 can add "Clipboard Paste" option as alternative

### Google APIs Rate Limiting
- **Problem**: Free tier may hit rate limits if recording frequently
- **Workaround**: Implement local Vosk fallback (Phase 01 contingency)

### Frameless Windows on Linux
- **Problem**: Flet frameless windows behave differently on Linux
- **Status**: This app targets Windows primarily; Linux support is secondary

## Performance Targets

| Operation | Target Time |
|-----------|------------|
| F8 pressed → Recording starts | <100ms |
| Recording (5 sec audio) | 5 sec |
| Recording → STT API | <2 sec (network dependent) |
| Translation | <1 sec |
| Text injection | Instant |
| **Total end-to-end** | **~8-10 sec** |

## Security Considerations

### API Keys
- **Current**: No API keys needed (free tier)
- **If upgraded** (e.g., Whisper API): Store keys in `config.json` (or environment variable, never hardcoded)

### Microphone Access
- Windows shows permission dialog on first run
- User must approve mic access

### Text Injection
- `pyautogui` can type anywhere (potential for accidental input)
- Mitigation: Always show visual feedback (UI state) before injecting

## Future Enhancements (v1.1+)

- Custom hotkey binding (not hardcoded F8)
- Whisper API integration (paid, but more reliable)
- Clipboard paste option (alternative to text injection)
- System tray icon
- Dark/light theme toggle
- Multi-language UI (currently English only)
- Keyboard shortcut for settings
- Batch processing (record multiple phrases without closing)
