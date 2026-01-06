"""
CloudWhisper Flow - Console Test Script (Phase 01, Task 2)
Supports microphone recording (--seconds) and WAV file input (--file). Uses Vosk offline.
"""

import argparse
import sounddevice as sd
import numpy as np
import vosk
import json
import sys
import wave
import subprocess
import tempfile
import os
from deep_translator import GoogleTranslator

# Defaults
DEFAULT_DURATION = 5
DEFAULT_SAMPLE_RATE = 16000
MODEL_PATH = "model"  # default model directory (place language models under ./model or specify --model-path)


def record_audio(duration=DEFAULT_DURATION, sample_rate=DEFAULT_SAMPLE_RATE):
    """Record audio from microphone. Returns bytes (PCM16) and sample_rate."""
    try:
        print(f"Recording for {duration} seconds... (please speak)", file=sys.stderr)
        audio_data = sd.rec(
            int(sample_rate * duration),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        # Convert float32 [-1,1] to int16 PCM
        int16 = (audio_data.flatten() * 32767).astype(np.int16)
        return int16.tobytes(), sample_rate
    except Exception as e:
        print(f"Recording error: {e}", file=sys.stderr)
        return None, None


def load_wav_file(path):
    """Load WAV file and return raw PCM16 bytes and sample_rate."""
    try:
        with wave.open(path, "rb") as wf:
            sr = wf.getframerate()
            nch = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())
            # If sampwidth is 2 bytes (16-bit), use as-is; otherwise, try to convert
            if sampwidth != 2:
                print(
                    f"Unsupported WAV sample width: {sampwidth*8} bits", file=sys.stderr
                )
                return None, None
            if nch > 1:
                # Convert interleaved stereo to mono by taking first channel
                data = np.frombuffer(frames, dtype="<i2")
                data = data.reshape(-1, nch)[:, 0].astype(np.int16)
                return data.tobytes(), sr
            return frames, sr
    except FileNotFoundError:
        print(f"WAV file not found: {path}", file=sys.stderr)
        return None, None
    except Exception as e:
        print(f"Error reading WAV file: {e}", file=sys.stderr)
        return None, None


def convert_mp3_to_wav(src_path):
    """Convert MP3 to 16kHz mono WAV using ffmpeg; returns wav path or None."""
    try:
        if not src_path.lower().endswith(".mp3"):
            return src_path
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp.name
        tmp.close()
        cmd = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            src_path,
            "-ar",
            str(DEFAULT_SAMPLE_RATE),
            "-ac",
            "1",
            tmp_path,
        ]
        subprocess.run(cmd, check=True)
        return tmp_path
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}", file=sys.stderr)
        return None


def load_model(path=MODEL_PATH):
    try:
        return vosk.Model(path)
    except Exception as e:
        print(
            f"Vosk model not found or failed to load at '{path}': {e}", file=sys.stderr
        )
        print(
            "Download a small English model from https://alphacephei.com/vosk/models and unzip into ./model",
            file=sys.stderr,
        )
        return None


def transcribe_pcm_bytes(pcm_bytes, sample_rate, model):
    try:
        rec = vosk.KaldiRecognizer(model, sample_rate)
        # Process in one chunk (for small files); chunking can be added if needed
        rec.AcceptWaveform(pcm_bytes)
        res = rec.FinalResult()
        obj = json.loads(res)
        return obj.get("text", "")
    except Exception as e:
        print(f"Transcription error: {e}", file=sys.stderr)
        return None


def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}", file=sys.stderr)
        return None


def main():
    p = argparse.ArgumentParser(description="Console STT test (Vosk).")
    p.add_argument(
        "--seconds",
        "-s",
        type=int,
        default=DEFAULT_DURATION,
        help="Recording seconds for microphone",
    )
    p.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to WAV file to transcribe instead of recording",
    )
    p.add_argument(
        "--translate-target",
        "-t",
        type=str,
        help="Translate transcription to target language (e.g., es)",
    )
    p.add_argument(
        "--model-path",
        type=str,
        default=MODEL_PATH,
        help="Path to Vosk model directory",
    )
    args = p.parse_args()

    # Load model
    model = load_model(args.model_path)
    if model is None:
        sys.exit(3)

    if args.file:
        # Support MP3 by converting to WAV inside the container using ffmpeg
        temp_wav = None
        file_path = args.file
        if file_path.lower().endswith(".mp3"):
            temp_wav = convert_mp3_to_wav(file_path)
            if temp_wav is None:
                sys.exit(4)
            file_path = temp_wav
        pcm, sr = load_wav_file(file_path)
        if pcm is None:
            if temp_wav:
                try:
                    os.remove(temp_wav)
                except Exception:
                    pass
            sys.exit(4)
        print("Processing file...", file=sys.stderr)
        text = transcribe_pcm_bytes(pcm, sr, model)
        if temp_wav:
            try:
                os.remove(temp_wav)
            except Exception:
                pass
    else:
        pcm, sr = record_audio(duration=args.seconds, sample_rate=DEFAULT_SAMPLE_RATE)
        if pcm is None:
            sys.exit(2)
        print("Transcribing...", file=sys.stderr)
        text = transcribe_pcm_bytes(pcm, sr, model)

    if text is None:
        print("Transcription failed.", file=sys.stderr)
        sys.exit(1)

    if text.strip() == "":
        print("No transcription detected.")
        sys.exit(2)

    print("Transcription complete!")
    print(f"Text: {text}")

    if args.translate_target:
        tr = translate_text(text, args.translate_target)
        if tr:
            print(f"Translation ({args.translate_target}): {tr}")


if __name__ == "__main__":
    main()
