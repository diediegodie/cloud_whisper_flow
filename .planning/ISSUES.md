# CloudWhisper Flow - Issues & Enhancements Log

This file tracks enhancements, improvements, and nice-to-haves discovered during development.
Logged here rather than implemented immediately to avoid scope creep and keep v1.0 focused.

---

## v1.1 Enhancements (Post-Release)

### UI/UX
- [ ] Custom hotkey binding (UI dropdown: F8, F9, Ctrl+Shift+V, etc.)
- [ ] System tray icon with right-click menu (minimize, settings, exit)
- [ ] Dark/light theme toggle in settings
- [ ] Drag window to move (already works, just verify UX)
- [ ] Window size customization (collapsible to tiny icon)

### Features
- [ ] Whisper API fallback (if Google Speech API fails)
- [ ] Clipboard paste option (alternative to text injection)
- [ ] Batch recording (record multiple phrases without closing settings)
- [ ] Voice command support (e.g., "translate to French" mid-recording)
- [ ] History panel (show last 10 transcriptions)

### Stability & Robustness
- [ ] Implement Vosk (offline speech recognition) as full fallback
- [ ] Implement `translators` library support (backup to deep-translator)
- [ ] Retry logic for API timeouts (exponential backoff)
- [ ] Connection monitoring (show offline indicator if no internet)
- [ ] Auto-restart recording on network hiccup

### Performance
- [ ] Cache supported languages (don't reload on each translation)
- [ ] Optimize audio buffer size for faster recognition
- [ ] Lazy-load heavy modules only when needed

### Accessibility & Localization
- [ ] Multi-language UI (French, Spanish, German, Portuguese)
- [ ] Keyboard shortcuts (Alt+S for settings, Alt+Q for quit)
- [ ] Screen reader support (Flet + ARIA tags)

### Advanced Features (v1.2+)
- [ ] Custom pronunciation dictionary (e.g., "LOL" → "Laughing Out Loud")
- [ ] Text formatting (capitalize, uppercase, lowercase buttons)
- [ ] Auto-correct with custom dictionary
- [ ] Recording pause/resume (not just stop)
- [ ] Audio preview (play back recorded audio before transcription)
- [ ] Multi-window support (float multiple recording widgets)

---

## Known Issues & Limitations

### Current Limitations (Accepted for v1.0)
- Text injection doesn't work in all applications (web-based editors may fail)
- No undo/revision system (once typed, can't take it back)
- Recording stops on silence (can't use pauses; use continuous mode)
- No visual waveform (just status indicator)

### API Limitations (Free Tier)
- Google Speech API: ~50 requests/day (unofficial, rate limited)
- Google Translate: ~500k characters/month (web scraping, unstable)
- Both can break if Google changes API structure

### Platform Limitations
- Windows primary support (Linux/Mac support secondary)
- Frameless window may not work on all Windows versions (fallback to standard frame)
- Microphone access requires Windows permission dialog

---

## Deviations & Fixes Applied

This section documents any changes made during development that differ from the original plan.

### Phase 01
- [No deviations yet - awaiting execution]

### Phase 02
- [No deviations yet - awaiting execution]

### Phase 03
- [No deviations yet - awaiting execution]

### Phase 04
- [No deviations yet - awaiting execution]

### Phase 05
- [No deviations yet - awaiting execution]

---

## Testing & Bug Reports

### Reported Issues
- None yet

### Fixed Bugs
- None yet

### Workarounds Applied
- None yet

---

## Post-Release (After v1.0 Ships)

1. Gather user feedback from beta testers
2. Log top 3 feature requests here
3. Address critical bugs first
4. Plan v1.1 with accepted enhancements
5. Repeat cycle

---

## Notes for Future Phases

- Consider migrating from single-file `main.py` to modular structure if it grows >1000 lines
- If threading becomes complex, consider asyncio instead of threading
- If UI becomes more complex, consider migrating to PyQt/Tkinter with better layout control
- Monitor Flet updates for stability improvements (current v0.20+)

