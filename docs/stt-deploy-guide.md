# STT Deployment Guide (for AI Agents)

> This guide is designed for AI coding agents (Claude Code, Cursor, etc.) to automatically install and deploy the FunASR SenseVoice-Small speech recognition model. Follow the steps sequentially and verify each step before proceeding.

## Overview

- **Model**: [FunASR SenseVoice-Small](https://modelscope.cn/models/iic/SenseVoiceSmall) (`iic/SenseVoiceSmall`)
- **Model hub**: ModelScope (`hub="ms"`) -- do NOT use HuggingFace (blocked in China)
- **Model size**: ~900MB on disk
- **Script**: `stt.py` in the project root
- **Input**: WAV audio file (16kHz, mono)
- **Output**: transcribed text (stdout)

## Step 1: Detect Environment

Run these checks and record the results:

```bash
# OS and architecture
uname -s -m

# Python version (requires 3.8+)
python3 --version

# Check for NVIDIA GPU
nvidia-smi 2>/dev/null && echo "CUDA_AVAILABLE=yes" || echo "CUDA_AVAILABLE=no"

# Check for Apple Silicon MPS
python3 -c "import torch; print('MPS_AVAILABLE=' + str(torch.backends.mps.is_available()))" 2>/dev/null || echo "MPS_AVAILABLE=unknown"

# Check FFmpeg
ffmpeg -version 2>/dev/null | head -1 || echo "FFMPEG_MISSING=yes"
```

Based on the results, determine the **target environment**:

| Environment | OS | GPU | Device |
|---|---|---|---|
| **CUDA** | Linux | NVIDIA GPU | `cuda:0` |
| **MPS** | macOS (Apple Silicon) | M1/M2/M3/M4 | `mps` |
| **CPU** | Any | None | `cpu` |

## Step 2: Install FFmpeg

FFmpeg is required to convert WeCom's AMR voice files to WAV.

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# CentOS/RHEL
sudo yum install -y ffmpeg

# Verify
ffmpeg -version | head -1
```

## Step 3: Install Python Dependencies

### Environment A: NVIDIA CUDA (Linux with GPU)

```bash
# Install PyTorch with CUDA support
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install FunASR and ModelScope
pip install funasr modelscope
```

### Environment B: Apple Silicon MPS (macOS)

```bash
# PyTorch for Mac ships with MPS support by default
pip install torch torchaudio

# Install FunASR and ModelScope
pip install funasr modelscope
```

**Important**: After install, set the MPS fallback env var to handle unsupported ops:
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
```
(This is already set automatically in `stt.py`, but useful for manual testing.)

### Environment C: CPU Only

```bash
# CPU-only PyTorch (smaller download)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install FunASR and ModelScope
pip install funasr modelscope
```

## Step 4: Download the Model

The model auto-downloads on first run. To pre-download explicitly:

```bash
python3 -c "
from modelscope import snapshot_download
snapshot_download('iic/SenseVoiceSmall')
print('Model downloaded successfully')
"
```

Default cache location: `~/.cache/modelscope/hub/iic/SenseVoiceSmall/`

**Network note**: The model is hosted on ModelScope (China). If downloading from outside China, ensure network connectivity to `modelscope.cn`. No VPN/proxy is needed within China.

## Step 5: Verify Installation

Run this verification script:

```bash
python3 -c "
import sys, os, io, logging

# Suppress verbose output
logging.disable(logging.CRITICAL)
os.environ['FUNASR_LOG_LEVEL'] = 'ERROR'
os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')

old_out, old_err = sys.stdout, sys.stderr
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

import torch
from funasr import AutoModel

if torch.cuda.is_available():
    device = 'cuda:0'
elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    device = 'mps'
else:
    device = 'cpu'

model = AutoModel(model='iic/SenseVoiceSmall', hub='ms', device=device)

sys.stdout = old_out
sys.stderr = old_err

print(f'Device: {device}')
print(f'Torch: {torch.__version__}')
print('Model loaded: OK')
"
```

Expected output (example for Apple Silicon):
```
Device: mps
Torch: 2.10.0
Model loaded: OK
```

## Step 6: Test with Audio

### Generate test audio (macOS)

```bash
# English
say -o /tmp/test_stt.aiff "Hello, this is a test"
ffmpeg -y -i /tmp/test_stt.aiff -ar 16000 -ac 1 /tmp/test_stt.wav

# Chinese (requires Chinese TTS voice)
say -v "Flo (Chinese (China mainland))" -o /tmp/test_zh.aiff "你好世界"
ffmpeg -y -i /tmp/test_zh.aiff -ar 16000 -ac 1 /tmp/test_zh.wav
```

### Generate test audio (Linux)

```bash
# Use ffmpeg to generate a sine wave as minimal test
ffmpeg -y -f lavfi -i "sine=frequency=440:duration=2" -ar 16000 -ac 1 /tmp/test_tone.wav

# Or use espeak if available
espeak "Hello this is a test" --stdout | ffmpeg -y -i - -ar 16000 -ac 1 /tmp/test_stt.wav
```

### Run STT

```bash
python3 stt.py /tmp/test_stt.wav
```

**Success criteria**: The script outputs recognized text to stdout with exit code 0. Empty output for non-speech audio (like a sine tone) is acceptable.

## Troubleshooting

### `ModuleNotFoundError: No module named 'funasr'`
```bash
pip install funasr
```

### `ModuleNotFoundError: No module named 'torchaudio'`
```bash
pip install torchaudio
```

### Model download hangs or fails
```bash
# Try explicit download with retry
python3 -c "
from modelscope import snapshot_download
snapshot_download('iic/SenseVoiceSmall', revision='master')
"
```

If ModelScope CDN is slow, set a mirror:
```bash
export MODELSCOPE_CACHE=~/.cache/modelscope
```

### MPS RuntimeError on macOS
Ensure the fallback is enabled:
```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
```
This is already handled in `stt.py` but may be needed for standalone testing.

### CUDA out of memory
SenseVoiceSmall is lightweight (~900MB). If GPU memory is still insufficient:
```bash
# Force CPU mode by setting env var before running
CUDA_VISIBLE_DEVICES="" python3 stt.py /path/to/audio.wav
```

## Device Priority in stt.py

The `stt.py` script auto-detects the best available device:

```
CUDA GPU (nvidia-smi) → Apple MPS (Metal) → CPU
```

No manual configuration is needed. The device selection code:

```python
if torch.cuda.is_available():
    device = "cuda:0"
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"
```

## Performance Reference

| Device | ~10s audio inference | Notes |
|---|---|---|
| CUDA (RTX 4090) | ~50-100ms | Fastest |
| Apple MPS (M2) | ~70-200ms | Good for local dev |
| CPU (modern x86) | ~200-600ms | Acceptable |
