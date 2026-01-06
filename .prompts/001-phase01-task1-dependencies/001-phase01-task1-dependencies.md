# Task 1: Environment Setup & Dependencies - CloudWhisper Flow Phase 01

## Objective
Set up the development environment for CloudWhisper Flow. Create `requirements.txt` with Phase 01 libraries and verify all dependencies install and import correctly.

**Context:** This is the first task in Phase 01 (Foundation & Proof-of-Concept). It establishes the foundation for the proof-of-concept console script that will validate STT, translation, and output logic before moving to UI development.

## Scope
- Create `requirements.txt` with pinned versions for 3 core libraries
- Install dependencies using pip
- Verify imports work (no runtime errors)
- Document any installation quirks discovered

**Out of scope:** Building the actual console script (Task 2), language model training, or API authentication (all APIs are free tier, no keys needed).

## Requirements

### Deliverables
1. **`requirements.txt`** file in project root with exact content:
   ```
   SpeechRecognition==3.10.0
   deep-translator==1.11.4
   sounddevice==0.4.6
   numpy>=1.21.0
   ```

2. **Installation verification**: Run `pip install -r requirements.txt` successfully

3. **Import verification**: All four libraries import without errors:
   - `import speech_recognition`
   - `from deep_translator import GoogleTranslator`
   - `import sounddevice`
   - `import numpy`

### Success Criteria
- ✅ `requirements.txt` file exists with exact pinned versions (including numpy)
- ✅ `pip install -r requirements.txt` completes without errors
- ✅ All four libraries import successfully
- ✅ No warnings or deprecation notices from imports (warnings OK, errors NOT OK)
- ✅ Virtual environment is activated (noted in output)

### Testing Procedure
After installation, run these commands to verify:
```bash
# Check requirements.txt exists and has correct content
cat requirements.txt

# Verify pip install
pip install -r requirements.txt

# Verify imports
python -c "import speech_recognition; print('✓ speech_recognition')"
python -c "from deep_translator import GoogleTranslator; print('✓ deep_translator')"
python -c "import sounddevice; print('✓ sounddevice')"
python -c "import numpy; print('✓ numpy')"
```

All four should print `✓` messages with no errors.

## Context & References

**Project context:**
- **Project:** CloudWhisper Flow - Lightweight desktop dictation widget
- **Language:** Python 3.10+
- **Architecture:** Single-process app (UI + Logic in one file)
- **Goal:** Prove core logic works (STT → Translation → Output)

**Phase 01 overview:**
This is Phase 1 of 5. Phase 01 is "Foundation & Proof-of-Concept". Task 1 is the first of 4 tasks.

**Why these libraries?**
- `SpeechRecognition` - Wraps free Google Web Speech API (no auth needed)
- `deep-translator` - Translates using free Google Translate backend (no auth needed)
- `sounddevice` - Modern, cross-platform audio input/output library (Python 3.12+ compatible, replaces pyaudio)
- `numpy` - Required by sounddevice for audio array handling

All are free, lightweight, and reliable for v1.0. Fallback alternatives are documented in the project brief if APIs break.

## Potential Issues & Workarounds

### Issue: `sounddevice` installation
`sounddevice` is well-maintained and generally installs cleanly on Windows/Mac/Linux.
- If issues occur, it's usually a missing system library (ALSA on Linux, for example)
- Install errors will be clear; follow error message guidance

### Issue: Import errors after installation
- Verify venv is activated: `which python` should show venv path
- Verify pip targets correct venv: `which pip` should show venv path
- Try: `pip install --upgrade pip` then reinstall

### Issue: Network timeout during install
- PyPI may be slow; retry with timeout flag: `pip install --default-timeout=1000 -r requirements.txt`
- Or use alternative index: `pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt`

## Output Specification

Create `SUMMARY.md` in the `.prompts/001-phase01-task1-dependencies/` folder with:

### Required Sections
1. **One-liner** - Substantive summary (not just "Task completed")
   - Example: "Environment setup complete: All 4 Phase 01 libraries installed and verified (SpeechRecognition, deep-translator, sounddevice, numpy)"

2. **Status** - ✅ (success) or ❌ (failed)

3. **What Was Done**
   - Created `requirements.txt` with 4 pinned library versions (sounddevice replacing pyaudio for Python 3.12+ compatibility)
   - Installed via `pip install -r requirements.txt`
   - Verified all 4 imports work

4. **Installation Results**
   - List each library and install status: ✅ SpeechRecognition 3.10.0
   - Include any warnings or quirks discovered
   - Python version used

5. **Verification Results**
   - Show test commands run and results
   - All four import tests should show ✓
   - If any import failed: show error details

6. **Decisions Needed**
   - If any library failed: Decision needed on workaround strategy
   - Otherwise: "None - ready for Task 2"

7. **Blockers**
   - Any unresolved installation issues
   - Network issues during install
   - Note: "None" if all succeeded

8. **Next Step**
   - "Execute Task 2: Build console_test.py (Audio Recording & STT with sounddevice)"

## Instructions for Execution

1. **Ensure venv is active**: User reports venv is already active. Verify: `which python` should show venv path.

2. **Create requirements.txt**: Write the exact file with 3 pinned versions (no extras, exact formatting).

3. **Install**: Run `pip install -r requirements.txt` with output captured.

4. **Verify imports**: Run the 3 import test commands. Capture output and any errors.

5. **Document quirks**: Note any warnings, version conflicts, or platform-specific issues.

6. **Create SUMMARY.md**: Fill template with results and decisions needed.

7. **Git status**: Note what files were created (`requirements.txt`) for user to commit when ready.

## Important Notes

- **No venv creation needed**: User reports venv is already active. Just create requirements.txt and install.
- **Exact versions matter**: Pin exactly as specified (3.10.0, 1.11.4, 0.4.6, >=1.21.0). These are stable, tested versions.
- **API keys not needed**: All libraries use free APIs. No authentication setup needed.
- **Sounddevice is the primary choice**: More reliable and modern than pyaudio. Already accounts for Python 3.12+ compatibility issue discovered during setup.

## Quality Checklist (Before Declaring Success)

- [x] `requirements.txt` file created in project root
- [x] File contains exactly 3 lines (pinned versions, no comments, no extras)
- [x] `pip install -r requirements.txt` runs to completion
- [ ] No dependency conflicts reported by pip
- [ ] All 4 import tests pass (speech_recognition, deep_translator, sounddevice, numpy)
- [ ] SUMMARY.md created with all required sections
- [ ] One-liner is substantive (describes what was done, not just "completed")
- [ ] Next step clearly states "Execute Task 2"

---

## Output Location

Save summary to: `.prompts/001-phase01-task1-dependencies/SUMMARY.md`

This summary will be reviewed by user before moving to Task 2.
