---
layout: default
title: 技术点 · Voice Mode
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Voice Mode

> 来源：261010_Voice Mode_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- The `~/.hermes/` directory and default `config.yaml` are created automatically the first time you run `hermes`. You only need to create `~/.hermes/.env` manually for API keys.
- A paid [Nous Portal](./tool-gateway.md) subscription supplies the LLM (step 2) **and** OpenAI TTS via the Tool Gateway — no separate OpenAI key needed. On a fresh install, `hermes setup --portal` wires both up at once.
- ```
# CLI voice mode (microphone + audio playback)
cd ~/.hermes/hermes-agent && uv pip install -e ".[voice]"

# Discord + Telegram messaging (includes discord.py[voice] for VC support)
cd ~/.hermes/hermes-agent && uv pip install -e ".[messaging]"

# Premium TTS (ElevenLabs)
cd ~/.hermes/hermes-agent && uv pip install -e ".[tts-premium]"

# Local TTS (NeuTTS, optional)
python -m pip install -U neutts[all]

# Everything at once
cd ~/.hermes/hermes-agent && uv pip install -e ".[all]"
```
- ```
# macOS
brew install portaudio ffmpeg opus
brew install espeak-ng   # for NeuTTS

# Ubuntu/Debian
sudo apt install portaudio19-dev ffmpeg libopus0
sudo apt install espeak-ng   # for NeuTTS
```
- ```
# Speech-to-Text — local provider needs NO key at all
# pip install faster-whisper          # Free, runs locally, recommended
GROQ_API_KEY=your-key                 # Groq Whisper — fast, free tier (cloud)
VOICE_TOOLS_OPENAI_KEY=your-key       # OpenAI Whisper — paid (cloud)

# Text-to-Speech (optional — Edge TTS and NeuTTS work without any key)
ELEVENLABS_API_KEY=***           # ElevenLabs — premium quality
# VOICE_TOOLS_OPENAI_KEY above also enables OpenAI TTS
```
- If `faster-whisper` is installed, voice mode works with **zero API keys** for STT. The model (~150 MB for `base`) downloads automatically on first use.
- ```
HF_ENDPOINT=https://your-hugging-face-mirror.example
HF_HUB_DISABLE_XET=1
```
- ```
hermes                # Start the interactive CLI
```
- ```
/voice          Toggle voice mode on/off
/voice on       Enable voice mode
/voice off      Disable voice mode
/voice tts      Toggle TTS output
/voice status   Show current state
```
- 8. Recording **automatically restarts** — speak again without pressing any key
- The record key is configurable via `voice.record_key` in `~/.hermes/config.yaml` (default: `ctrl+b`).
- 3. Plays audio per sentence in real-time — providers with a chunked PCM API (ElevenLabs, OpenAI) stream raw audio for the lowest time-to-first-word; every other provider (including the default Edge) synthesizes and plays each sentence as it completes

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
