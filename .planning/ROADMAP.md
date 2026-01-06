# CloudWhisper Flow - Roadmap

## Overview
5-phase development roadmap from proof-of-concept to shipped v1.0. Each phase delivers incremental value and validates assumptions before building the next layer.

## Milestone: v1.0 Release
Target: Working, packaged desktop app with voice-to-text, optional translation, and text injection.

---

## Phase 01: Foundation & Proof-of-Concept
**Goal:** Validate all core logic without UI distractions. Prove STT→Translation→Output flow works.

**Deliverables:**
- `console_test.py` - Records 5 seconds of audio, transcribes, translates, prints result
- All dependencies installed and working
- Error handling for API failures
- Local fallback strategy documented

**Scope:** Logic only, no UI
**Estimated Size:** Small (2-3 tasks)
**Dependencies:** None
**Success Criteria:**
- Console script records microphone input
- Google Speech API transcribes successfully
- Translation works (or gracefully skips)
- Output printed to console

---

## Phase 02: Flet UI Skeleton
**Goal:** Build the visual widget. Frameless, transparent, always-on-top floating window.

**Deliverables:**
- Basic Flet app with floating window
- Status label (Ready/Recording/Processing)
- Progress indicator
- Settings button (non-functional for now)
- Window stays on top of other applications

**Scope:** UI structure only, no logic integration yet
**Estimated Size:** Small (2-3 tasks)
**Dependencies:** Phase 01 (conceptual, not code)
**Success Criteria:**
- App launches with floating widget
- Window is frameless and transparent
- Stays on top of other windows
- Graceful window close

---

## Phase 03: Integration & Threading
**Goal:** Connect logic from Phase 01 to UI from Phase 02. Add global hotkey listener.

**Deliverables:**
- F8 hotkey listener running in background thread
- Recording triggered by F8 press
- UI updates during recording (color changes: Red=Recording, Yellow=Processing)
- STT/Translation/Output logic runs without freezing UI
- Clean shutdown on app exit

**Scope:** Threading, state management, visual feedback
**Estimated Size:** Medium (3-4 tasks)
**Dependencies:** Phases 01 & 02
**Success Criteria:**
- F8 starts/stops recording
- UI responds in real-time (no freezing)
- Status changes: Ready → Recording → Processing → Ready
- Text appears at cursor position after processing

---

## Phase 04: User Configuration
**Goal:** Make app usable for different languages. Add settings UI.

**Deliverables:**
- Expandable settings panel (click gear icon)
- Dropdown for target language (FR, ES, DE, PT, IT, JA, ZH, etc.)
- Save user preferences (JSON config file)
- Load preferences on startup
- Language selection persists across sessions

**Scope:** Settings UI, config persistence, language selection
**Estimated Size:** Small (2-3 tasks)
**Dependencies:** Phases 01-03
**Success Criteria:**
- Settings panel toggles open/closed
- Language dropdown populated
- User selection saved and restored
- Default language: English

---

## Phase 05: Packaging & Distribution
**Goal:** Create standalone `.exe` with bundled dependencies.

**Deliverables:**
- `flet pack main.py --icon icon.ico` produces working `.exe`
- Icon created (simple design)
- Test `.exe` on clean Windows machine (or VM)
- README with install instructions
- Release checklist documented

**Scope:** Packaging, testing, distribution prep
**Estimated Size:** Small (2 tasks)
**Dependencies:** Phases 01-04
**Success Criteria:**
- `.exe` runs on Windows 10/11 without Python installed
- Microphone access granted (permission dialog)
- App functions identically to dev version

---

## Known Risks & Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| Google API rate-limits or breaks | Medium | Phase 01 tests fallback to Vosk; document alternatives |
| `pyaudio` fails to install (Mac/Linux) | Medium | Phase 01 documents `sounddevice` swap |
| Flet frameless windows behave differently on Windows | Low | Phase 02 tests on actual Windows; fallback to standard frame if needed |
| Text injection doesn't work in specific apps | Low | Phase 03 documents app incompatibilities; `pyautogui` has known limitations |
| Audio recording quality issues | Low | Phase 01 tests with different audio settings |

---

## Phase Checklist

- [ ] Phase 01: Foundation (console_test.py complete, all APIs validated)
- [ ] Phase 02: UI Skeleton (Flet window working, stays on top)
- [ ] Phase 03: Integration (F8 hotkey works, threading stable, UI updates in real-time)
- [ ] Phase 04: Configuration (settings persist, language dropdown functional)
- [ ] Phase 05: Packaging (`.exe` builds, runs on clean Windows)
- [ ] v1.0 Release (all phases complete, tested, documented)

---

## Tracking & Milestones

**v1.0 Shipped:** Phases 01-05 complete
**Next iteration (v1.1):** Enhancements logged in ISSUES.md during execution
- Custom hotkey binding (not hardcoded F8)
- Whisper API integration (fallback if Google breaks)
- Clipboard paste option (alternative to text injection)
- System tray icon
- Dark/light theme toggle
