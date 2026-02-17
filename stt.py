#!/usr/bin/env python3
"""Voice STT using FunASR SenseVoice-Small from ModelScope."""
import sys
import re
import os
import io

model = None

def get_model():
    global model
    if model is None:
        # Suppress all FunASR/ModelScope verbose output during model loading
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        try:
            import logging
            logging.disable(logging.CRITICAL)
            os.environ["FUNASR_LOG_LEVEL"] = "ERROR"
            from funasr import AutoModel
            try:
                import torch
                device = "cuda:0" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
            model = AutoModel(model="iic/SenseVoiceSmall", hub="ms", device=device)
            logging.disable(logging.NOTSET)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    return model

def transcribe(audio_path):
    m = get_model()
    # Suppress progress bar output during inference
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        res = m.generate(input=audio_path)
    finally:
        sys.stderr = old_stderr
    if not res or not res[0].get("text"):
        return ""
    text = res[0]["text"]
    # Strip SenseVoice special tags like <|zh|><|NEUTRAL|><|Speech|><|woitn|>
    text = re.sub(r"<\|[^|]*\|>", "", text).strip()
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: stt.py <audio_file>", file=sys.stderr)
        sys.exit(1)
    result = transcribe(sys.argv[1])
    print(result)
