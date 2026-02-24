# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

```bash
# Activate conda environment
conda activate mlx

# Install dependencies
pip install -U mlx-audio soundfile numpy argparse gradio fastapi uvicorn

# Download models (one-time)
python test/hg-download.py

# Web UI (Gradio) - 5 tabs interface
python webui.py --port 7860

# API Server (FastAPI) - REST endpoints + Web Demo
python server.py
# Then open: http://localhost:7860/demo

# CLI Menu - Interactive command line
python main.py

# Legacy test scripts
python test/qwen3tts.py -m base        # Predefined voice (Aiden)
python test/qwen3tts.py -m clone       # Voice cloning with ref_audio
python test/qwen3tts.py -m custom      # Custom speaker + emotion instruction
python test/qwen3tts.py -m design      # Voice design from text description
python test/chatterbox.py              # Storytelling with emotion tags
```

## Architecture

This is a text-to-speech synthesis workspace using Apple's MLX framework with three primary modes:

### Three Modes

| Mode | Purpose | Entry Point |
|------|---------|-------------|
| **Custom Voice** | Preset speakers + emotion control | `CustomVoice` tab / `/api/v1/custom-voice` |
| **Voice Design** | Natural language voice descriptions | `VoiceDesign` tab / `/api/v1/voice-design` |
| **Voice Clone** | Clone from reference audio | `VoiceClone` tab / `/api/v1/base/clone` |

### Models

| Model | Purpose | Key Method |
|-------|---------|------------|
| **Chatterbox-Turbo-FP16** | Expressive storytelling + voice cloning | `generate(text, ref_audio)` |
| **Qwen3-TTS-12Hz-1.7B-Base-bf16** | Production TTS with predefined voices | `generate(text, voice, language)` |
| **Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16** | Emotion-controlled speech | `generate_custom_voice(text, speaker, language, instruct)` |
| **Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16** | Custom voice from description | `generate_voice_design(text, language, instruct)` |

### Model Variants

| Variant | Size | RAM Usage | Quality |
|---------|------|-----------|---------|
| **Pro (1.7B)** | ~5-6GB | Best quality, slower |
| **Lite (0.6B)** | ~2-3GB | Faster, good quality |

### Speakers by Language

| Language | Speakers |
|----------|----------|
| **English** | Ryan, Aiden, Ethan, Chelsie, Serena, Vivian |
| **Chinese** | Vivian, Serena, Uncle_Fu, Dylan, Eric |
| **Japanese** | Ono_Anna |
| **Korean** | Sohee |

### Data Flow

```
load_model(folder_name) → model.generate*(...) → list(results) →
  np.array(results[0].audio) → sf.write(filename, model.sample_rate)
```

### Models Location

All models are stored in the `models/` directory:

- `models/Chatterbox-Turbo-FP16/` - Expressive storytelling model
- `models/Qwen3-TTS-12Hz-1.7B-Base-bf16/` - Base model with predefined speakers
- `models/Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16/` - Custom voice model with speaker + emotion control
- `models/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16/` - Voice design from text description

## API Reference

### Custom Voice Endpoints
```
POST /api/v1/custom-voice/generate    # Generate speech with speaker + emotion
GET  /api/v1/speakers                 # List available speakers
GET  /api/v1/languages                # List available languages
```

### Voice Design Endpoints
```
POST /api/v1/voice-design/generate    # Generate voice from description
```

### Voice Clone Endpoints
```
POST /api/v1/base/clone               # Clone voice from reference audio
POST /api/v1/base/clone/stream        # Stream cloned voice output
```

### Voice Prompt Endpoints
```
POST /api/v1/base/create-prompt       # Create voice prompt
POST /api/v1/base/generate-with-prompt # Generate with existing prompt
GET  /api/v1/prompts/{id}             # Get prompt by ID
DELETE /api/v1/prompts/{id}           # Delete prompt
```

### Utility Endpoints
```
POST /api/v1/base/transcribe          # Speech-to-text transcription
GET  /api/v1/health                   # Health check
GET  /api/v1/health/models            # Check loaded models
GET  /demo                            # Serve static web demo
GET  /                                # Redirects to /demo
```

### Static Web Demo

The `static/` folder contains a production-ready web interface:
- **Location**: `http://localhost:7860/demo` (when running `server.py`)
- **Features**: 3 tabs (Custom Voice, Voice Design, Voice Clone) + Settings
- **Files**: `index.html`, `styles.css`, `app.js`
- **i18n**: Supports English and Chinese (switchable in UI)

## Directory Structure

```
mlx_test/
├── models/                    # All models stored here
│   ├── Chatterbox-Turbo-FP16/
│   ├── Qwen3-TTS-12Hz-1.7B-Base-bf16/
│   ├── Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16/
│   └── Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16/
├── output/                    # Legacy output directory
├── outputs/                   # New scripts output directory
│   ├── CustomVoice/
│   ├── VoiceDesign/
│   └── Clones/
├── voices/                    # Saved voice profiles
│   └── saved/                 # server.py creates this
├── voice_ref/                 # Reference audio files (WAV/M4A)
├── static/                    # Web demo files
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── test/                      # Legacy test scripts
│   ├── qwen3tts.py
│   ├── chatterbox.py
│   └── hg-download.py
├── webui.py                   # Gradio Web UI (5 tabs)
├── server.py                  # FastAPI REST API
├── main.py                    # CLI interactive menu
└── CLAUDE.md                  # This file
```

**Note:**
- All models are now consolidated in `models/` (Chatterbox moved from project root)
- Output paths: `output/` (legacy test scripts) vs `outputs/{mode}/` (new scripts)

## Code Conventions

1. **Output directories**:
   - Legacy: `output/` with pattern `{model_name}_{timestamp}.wav`
   - New: `outputs/{mode}/` (CustomVoice/, VoiceDesign/, Clones/)

2. **Voice profiles**: `voices/saved/{id}/audio.wav + metadata.json`

3. **Timestamp format**: `%Y%m%d_%H%M%S`

4. **Sample rate**: 24000 Hz

5. **Emotion tags** (Chatterbox): `[chuckle]`, `[gasp]`, `[sigh]`, `[sniff]`, `[hmm]`

6. **Relative paths** for assets from workspace root

## Dependencies

### Core
- `mlx-audio` - TTS model interface
- `soundfile` - WAV I/O
- `numpy` - Audio array handling
- `huggingface_hub` - Model downloads

### Web UI (Gradio)
- `gradio` - Web UI (webui.py)

### API Server (FastAPI)
- `fastapi` - REST API (server.py)
- `uvicorn` - ASGI server (server.py)
- `librosa` - Audio format conversion (optional, for MP3/M4A support)

### Optional
- `mlx-whisper` - Speech-to-text transcription (for auto-transcribing reference audio)
  - Install: `pip install mlx-whisper`

### Test Scripts
- `argparse` - CLI argument parsing

## Platform Requirements

- **OS**: macOS only (Apple Silicon M1/M2/M3/M4)
- **Environment**: Conda environment `mlx` required

## Git Configuration

A `.gitignore` file is included to exclude:
- **Generated outputs**: `outputs/`, `output/`, `voices/`, `voice_ref/`
- **Models**: `models/` (large files, download separately via `test/hg-download.py`)
- **Python artifacts**: `__pycache__/`, `*.pyc`, `*.egg-info/`
- **Temporary files**: `temp_*/`, `*.tmp`
- **IDE/Editor**: `.vscode/`, `.idea/`, `*.swp`
- **macOS**: `.DS_Store`

## Project Status

### Latest Updates
- **All models consolidated** in `models/` directory
- **Model paths fixed** in all entry points (webui.py, server.py, main.py, test scripts)
- **Chatterbox-Turbo-FP16** moved from project root to `models/`
- **Static web demo** available at `/demo` when running server.py

### Entry Points Status
| File | Status | Model Paths |
|------|--------|-------------|
| `webui.py` | Fixed | `models/Qwen3-TTS-*` |
| `server.py` | Working | `models/Qwen3-TTS-*` |
| `main.py` | Fixed | `models/Qwen3-TTS-*` |
| `test/qwen3tts.py` | Fixed | `models/Qwen3-TTS-*` |
| `test/chatterbox.py` | Fixed | `models/Chatterbox-Turbo-FP16` |
| `test/hg-download.py` | Fixed | Downloads to `models/` |
