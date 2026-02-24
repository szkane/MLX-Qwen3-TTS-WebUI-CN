# MLX Audio TTS

基于 Apple MLX 框架的多模态文本转语音（TTS）合成工作区。支持自定义语音、语音设计、语音克隆和**多人对话**四种模式。

Forked from [Blizaine qwen3-tts-apple-silicon](https://github.com/Blizaine/qwen3-tts-apple-silicon/tree/main)

## 平台要求

- **操作系统**: macOS only (Apple Silicon M1/M2/M3/M4)
- **环境**: Conda 环境 `mlx`

## 快速开始

```bash
# 创建 conda 环境（如果不存在）
conda create -n mlx python=3.11  # 仅在环境不存在时执行
conda activate mlx

# 安装依赖
pip install -U mlx-audio soundfile numpy argparse gradio fastapi uvicorn

# 下载模型（一次性操作）
python test/hg-download.py

# 方式 1: FastAPI 服务 - REST API + Web Demo (推荐)
python server.py
# 访问：http://localhost:7860/demo

# 方式 2: Gradio Web UI - 5 标签页界面
python webui.py --port 7860

# 方式 3: CLI 交互式命令行
python main.py
```

## 三种工作模式

| 模式             | 功能                  | 入口                                          |
| ---------------- | --------------------- | --------------------------------------------- |
| **Custom Voice** | 预设说话人 + 情感控制 | `CustomVoice` 标签页 / `/api/v1/custom-voice` |
| **Voice Design** | 自然语言描述生成语音  | `VoiceDesign` 标签页 / `/api/v1/voice-design` |
| **Voice Clone**  | 从参考音频克隆语音    | `VoiceClone` 标签页 / `/api/v1/base/clone`    |

---

## ✨ 多人对话模式（Multi-Person Conversation）

**创建多人对话，一键生成多角色音频！**

在 Web Demo 的 "Multi-Person Conversation" 标签页中，您可以：

### 核心特性

1. **多说话者支持**
   - 支持 2-5 个说话者
   - 每个说话者独立配置声音和文本
   - 批量生成，自动拼接音频

2. **灵活的声音来源**
   - **Voice Design**：用自然语言描述声音特征（如 "A warm, friendly female voice"）
   - **Saved Voices**：从语音克隆中保存的声音库中选择

3. **直观的可视化界面**
   - 彩色说话者卡片，一目了然
   - 时间线显示各说话者片段
   - 点击跳转到指定说话者
   - 实时高亮当前播放的说话者

4. **多语言支持**
   - 支持中文、英语、日语、韩语等多种语言
   - 每个说话者可独立设置语言
   - 界面支持中英文切换

### 使用示例

```json
POST /api/v1/conversation/generate
{
  "speakers": [
    {
      "voice_source": "voice_design",
      "text": "你好！欢迎参加我们的节目。",
      "instruct": "一个温暖友好的男声",
      "language": "Chinese"
    },
    {
      "voice_source": "saved_voice",
      "text": "谢谢邀请！很高兴来到这里。",
      "prompt_id": "abc123-def456",
      "language": "Chinese"
    }
  ],
  "speed": 1.0,
  "response_format": "base64"
}
```

### API 端点

```
POST /api/v1/conversation/generate    # 生成多人对话
```

## 模型列表

| 模型                                     | 用途                          | 关键方法                                                   |
| ---------------------------------------- | ----------------------------- | ---------------------------------------------------------- |
| **Chatterbox-Turbo-FP16**                | 富有表现力的讲故事 + 语音克隆 | `generate(text, ref_audio)`                                |
| **Qwen3-TTS-12Hz-1.7B-Base-bf16**        | 生产级 TTS，预设语音          | `generate(text, voice, language)`                          |
| **Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16** | 情感控制语音合成              | `generate_custom_voice(text, speaker, language, instruct)` |
| **Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16** | 从描述生成自定义语音          | `generate_voice_design(text, language, instruct)`          |

### 模型变体

| 变体            | 大小   | 内存占用       | 质量 |
| --------------- | ------ | -------------- | ---- |
| **Pro (1.7B)**  | ~5-6GB | 最佳质量，较慢 |
| **Lite (0.6B)** | ~2-3GB | 更快，良好质量 |

### 支持的说话人

| 语言     | 说话人                                      |
| -------- | ------------------------------------------- |
| **英语** | Ryan, Aiden, Ethan, Chelsie, Serena, Vivian |
| **中文** | Vivian, Serena, Uncle_Fu, Dylan, Eric       |
| **日语** | Ono_Anna                                    |
| **韩语** | Sohee                                       |

## 目录结构

```
mlx_test/
├── models/                    # 模型存储目录
│   ├── Chatterbox-Turbo-FP16/
│   ├── Qwen3-TTS-12Hz-1.7B-Base-bf16/
│   ├── Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16/
│   └── Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16/
├── outputs/                   # 输出文件目录
│   ├── CustomVoice/
│   ├── VoiceDesign/
│   └── Clones/
├── voices/                    # 保存的语音配置
│   └── saved/
├── voice_ref/                 # 参考音频文件 (WAV/M4A)
├── static/                    # Web Demo 静态文件
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── test/                      # 测试脚本
│   ├── qwen3tts.py
│   ├── chatterbox.py
│   └── hg-download.py
├── webui.py                   # Gradio Web UI
├── server.py                  # FastAPI REST API
├── main.py                    # CLI 交互式菜单
└── README.md                  # 项目说明
```

## API 端点

### 自定义语音

```
POST /api/v1/custom-voice/generate    # 生成语音（说话人 + 情感）
GET  /api/v1/speakers                 # 获取可用说话人列表
GET  /api/v1/languages                # 获取可用语言列表
```

### 语音设计

```
POST /api/v1/voice-design/generate    # 从描述生成语音
```

### 语音克隆

```
POST /api/v1/base/clone               # 从参考音频克隆语音
POST /api/v1/base/clone/stream        # 流式输出克隆语音
```

### 语音提示

```
POST /api/v1/base/create-prompt       # 创建语音提示
POST /api/v1/base/generate-with-prompt # 使用已有提示生成
GET  /api/v1/prompts/{id}             # 获取提示
DELETE /api/v1/prompts/{id}           # 删除提示
```

### 工具端点

```
POST /api/v1/base/transcribe          # 语音转文字
GET  /api/v1/health                   # 健康检查
GET  /api/v1/health/models            # 检查已加载模型
GET  /demo                            # Web Demo 页面
GET  /                                # 重定向到 /demo
```

## 依赖安装

### 核心依赖

```bash
pip install mlx-audio soundfile numpy huggingface_hub
```

### Web UI (Gradio)

```bash
pip install gradio
```

### API 服务 (FastAPI)

```bash
pip install fastapi uvicorn librosa
```

### 可选依赖

```bash
# 语音转文字转录
pip install mlx-whisper
```

## 使用示例

### CLI 测试脚本

```bash
# 预设语音（Aiden）
python test/qwen3tts.py -m base

# 语音克隆（使用参考音频）
python test/qwen3tts.py -m clone

# 自定义说话人 + 情感指令
python test/qwen3tts.py -m custom

# 从文本描述设计语音
python test/qwen3tts.py -m design

# 带情感标签的故事讲述
python test/chatterbox.py
```

### 情感标签（Chatterbox）

在文本中使用情感标签：

- `[chuckle]` - 轻笑
- `[gasp]` - 倒吸一口气
- `[sigh]` - 叹息
- `[sniff]` - 抽鼻子
- `[hmm]` - 沉吟

## 输出约定

- **输出目录**: `outputs/{mode}/`（CustomVoice/, VoiceDesign/, Clones/）
- **语音配置**: `voices/saved/{id}/audio.wav + metadata.json`
- **时间戳格式**: `%Y%m%d_%H%M%S`
- **采样率**: 24000 Hz

## 注意事项

- 所有模型存储在 `models/` 目录
- 模型文件较大，请确保有足够磁盘空间
- 首次运行需要下载模型（使用 `test/hg-download.py`）
- 输出音频保存在 `outputs/` 目录

## 许可证

本项目仅供学习和研究使用。
