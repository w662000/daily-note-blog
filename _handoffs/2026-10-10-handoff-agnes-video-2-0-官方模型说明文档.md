---
layout: default
title: 交接文档 · Agnes Video 2.0 官方模型说明文档
date: 2026-10-13 23:30:00 +0800
---

# Agnes Video 2.0 官方模型说明文档

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\creative\agnes-video-generator\SKILL.md

---
name: agnes-video-generator
description: "Agnes Video 2.0 完全免费的AI视频生成模型 - 无需订阅、无需高端GPU、无使用限制，支持多场景视频生成、AI旁白、自动字幕"
version: 1.0.0
author: [lcy362, Bruce Yang]
license: MIT
platforms: [macos, linux, windows]
compatibility: "需要Python 3.10+和ffmpeg（Docker和npm版本自动包含ffmpeg）"
prerequisites:
  commands: ["python3"]
  env_vars: ["AGNES_API_KEY"]
setup:
  help: "克隆项目后运行 ./start.sh 自动部署，或使用 Docker/npm 一键部署。需要免费的 Agnes AI API 密钥。"
metadata:
  hermes:
    tags:
      - agnes-video
      - video-generation
      - ai-video
      - text-to-video
      - image-to-video
      - multi-scene
      - ai-narration
      - auto-subtitles
      - digital-anchor
      - free-ai
      - creative
      - multimedia
    related_skills: [comfyui, manim-video]
    category: creative
---

# Agnes Video 2.0 官方模型说明文档

## 模型概述

Agnes Video 2.0 是由 Agnes AI 开发的完全免费的AI视频生成模型，无需订阅、无需高端GPU、无使用限制。用户只需输入文本想法即可自动生成多场景AI视频，包含旁白和字幕。

## 核心能力

### 🎬 多种创作模式

| 模式 | 描述 | 适用场景 |
|------|-------------|----------|
| **Simple Video** | 单提示词→单个AI视频。完全控制所有参数（生成模式、时长、分辨率、种子、负面提示）。支持图片转视频和关键帧模式。 | 快速单片段AI视频 |
| **Creative Video** | 完整AI流程：想法→故事→脚本→角色参考→多场景视频→旁白→字幕→最终输出。10步流程，完全自动化。 | 故事创作、创意视频 |
| **Manuscript Video** | 粘贴长篇文章或脚本→按阅读时长自动分段→每段AI视频→统一TTS旁白+字幕叠加→最终输出。5步流程。 | 说明视频、课程内容、Vlog |
| **Digital Anchor** | AI生成的数字主播（或上传自定义图片）→动态主播片段→TTS旁白→字幕定位→循环拼接。可选参考图片保持外观一致性。 | 虚拟主播、产品展示、新闻播报 |

### 🆓 完全免费的AI模型链

所有核心AI能力都**完全免费**—无试用期、无水印、无令牌限制：

| 能力 | 模型 | 费用 |
|-----------|-------|------|
| 文本/脚本生成 | `agnes-2.0-flash` | 免费 |
| 图像生成 | `agnes-image-2.1-flash` | 免费 |
| 视频生成 | `agnes-video-v2.0` | 免费 |
| 文本转语音旁白 | Edge TTS (微软) | 免费，无需额外API密钥 |

所有AI API调用共享全局令牌桶速率限制器（16请求/分钟），具有自动重试和指数退避以确保稳定运行。

### 🎙️ AI旁白与智能字幕

Creative Video 和 Manuscript Video 支持：

- **免费TTS旁白**：基于微软Edge TTS，提供4种中文语音角色（温柔女声、沉稳男声、活泼女声、年轻男声），语速可调（-30%至+30%）
- **词级精细字幕**：从TTS词级时间戳生成的SRT字幕，每2-3秒一条，精确音视频同步
- **多行自动换行**：长字幕文本智能拆分为两行，优先在标点符号处断行，防止屏幕溢出
- **完全可配置字幕样式**：字体、颜色、大小、位置（顶部/底部）、描边、半透明背景
- **音视频同步策略**：所有视频片段先拼接，然后整体叠加音频和字幕，避免分段叠加的累积误差。TTS输出自动放大2.5倍以补偿Edge TTS的低默认音量

### 🎨 灵活的创意控制

- **自定义参考图片**：上传角色或场景参考图片以保持跨场景视觉一致性
- **自定义结束帧**：为每个场景指定结束帧图像以实现精确的视觉过渡控制
- **图片到图片结束帧**：从参考图片通过img2img自动生成场景结束帧
- **三种视频链接模式**：`keyframes`（首尾帧插值，推荐）/ `ti2vid`（场景间过渡帧）/ `none`（独立场景）
- **多种分辨率**：竖屏9:16（768×1152）、横屏16:9（1152×768）、正方形1:1（1024×1024）
- **灵活的时长**：自定义场景时长
- **智能稿件分割**：按句号/问号/感叹号分割，贪婪地合并为5-12秒片段（基于阅读速度~4字符/秒），保留长句子，自动向前合并短句子

### 🔧 生产级可靠性

- **检查点恢复**：中断后自动从最后一个检查点恢复；每步后状态持久化，无重复API调用
- **任务管理**：从Web UI创建、查看、恢复和停止任务
- **实时进度**：WebSocket推送每步生成进度（步骤名称、状态、百分比、当前/总数）
- **内置CJK字体**：项目自带中文字体，字幕渲染无乱码

## 模型技术特点

### 视频生成能力
- **最大视频长度**：每片段20秒，场景数量无限制
- **多场景管道**：内置（创意/稿件），无需手动编辑
- **AI旁白（TTS）**：免费，内置
- **自动字幕**：词级SRT
- **数字主播**：内置
- **分辨率选项**：9:16 / 16:9 / 1:1
- **图片转视频**：支持
- **关键帧动画**：支持
- **本地GPU需求**：无（云API）
- **水印**：无水印
- **使用限制**：无限制（16请求/分钟速率限制）

### 与商业AI视频工具对比

| 功能 | Agnes Video Generator | Runway Gen-3 | Pika 2.0 | OpenAI Sora | Kling 1.6 |
|------|:---:|:---:|:---:|:---:|:---:|
| **价格** | 免费 | $15-95/月 | $10-95/月 | $20+/月（有限） | 免费配额，然后按秒付费 |
| **开源** | ✅ 是（MIT） | ❌ 否 | ❌ 否 | ❌ 否 | ❌ 否 |
| **自托管** | ✅ 是 | ❌ 否 | ❌ 否 | ❌ 否 | ❌ 否 |
| **最大视频长度** | 每片段20秒，无场景限制 | 每片段10秒 | 每片段10秒 | 每片段20秒 | 每片段10秒 |
| **多场景管道** | ✅ 内置（创意/稿件） | ❌ 手动编辑 | ❌ 手动编辑 | ❌ 手动编辑 | ❌ 手动编辑 |
| **AI旁白（TTS）** | ✅ 免费，内置 | ❌ 第三方 | ❌ 第三方 | ❌ 不可用 | ❌ 不可用 |
| **自动字幕** | ✅ 词级SRT | ❌ 不可用 | ❌ 不可用 | ❌ 不可用 | ❌ 不可用 |
| **数字主播** | ✅ 内置 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 |
| **分辨率选项** | 9:16 / 16:9 / 1:1 | 多种 | 多种 | 多种 | 多种 |
| **图片转视频** | ✅ 是 | ✅ 是 | ✅ 是 | ✅ 图片输入 | ✅ 是 |
| **关键帧动画** | ✅ 是 | ✅ 是 | ✅ 是 | ❌ 不可用 | ❌ 不可用 |
| **本地GPU需求** | ❌ 无（云API） | ❌ 无（云） | ❌ 无（云） | ❌ 无（云） | ❌ 无（云） |
| **水印** | 无水印 | 内置水印 | 内置水印 | C2PA元数据 | 内置水印 |
| **使用限制** | 无限制（16请求/分钟） | 按计算计费 | 按生成计费 | 按生成计费 | 按生成计费 |

## 部署方式

### 1. 手动部署
```bash
git clone https://github.com/lcy362/agnes-video-generator.git
cd agnes-video-generator
./start.sh
```

### 2. Docker部署（无需Python/FFmpeg）
```bash
docker run -d -p 8765:8765 \
  -e AGNES_API_KEY=<your-key> \
  -v ~/agnes-data/working:/app/.working_dir \
  -v ~/agnes-data/config:/app/.agnes_config \
  ghcr.io/lcy362/free-short-video:latest
```

### 3. npm一键部署
```bash
npx free-short-video
# 或安装全局
npm install -g free-short-video
free-short-video  # 简写：fsv
```

## API密钥获取

1. 访问 [Agnes AI平台](https://platform.agnes-ai.com)
2. 注册并获取免费API密钥（格式为 `sk-` 开头）
3. 在Web UI中配置或通过环境变量设置：
```bash
export AGNES_API_KEY="your-api-key"
```

**重要**：API使用Form表单数据，不是JSON格式！使用 `-F` 参数而非 `-d` 参数。

## API调用方式

**重要**：API使用Form表单数据，不是JSON格式！

```bash
# Simple Video - 正确调用方式
curl -X POST http://localhost:8765/api/tasks/simple \
  -F "prompt=修仙小说中的主角韩立施展剑阵..." \
  -F "mode=t2v" \
  -F "duration=15" \
  -F "video_width=1152" \
  -F "video_height=768"

# Creative Video
curl -X POST http://localhost:8765/api/tasks/creative \
  -F "idea=太空探险故事" \
  -F "scene_count=3" \
  -F "duration=10"

# 配置API Key
curl -X POST http://localhost:8765/api/config \
  -F "api_key=sk-xxxxxxxx"
```

## 使用流程

1. **配置API密钥**：在页面顶部输入并保存Agnes AI API密钥（`sk-` 开头格式）
2. **选择视频模式**：选择Simple/Creative/Manuscript/Anchor模式
3. **输入创作内容**：
   - Simple Video：输入提示词
   - Creative Video：描述视频想法
   - Manuscript Video：粘贴文章或脚本
   - Digital Anchor：输入主播台词
4. **点击"开始生成"**：进度面板显示每步实时生成状态
5. **检查点恢复**：如服务器中断，重启后可在"任务列表"中点击"Resume"继续

## 输出目录结构

所有AI视频任务产物存储在 `.working_dir/{timestamp}_{task_id}/` 下：

```
.working_dir/{timestamp}_{task_id}/
├── task_state.json              # 任务状态（检查点恢复需要）
├── final_video.mp4              # 最终视频（含旁白+字幕）
├── story.txt                    # AI生成的故事（创意模式）
├── script.json                  # 场景脚本（JSON格式）
├── narration.mp3                # 合并的TTS旁白音频
├── narration.srt                # 合并的字幕文件
├── scene_0/
│   ├── video.mp4                # 场景0 AI视频
│   ├── end_frame.png            # 场景0结束帧
│   └── task.json                # 视频生成任务ID
├── scene_1/
│   └── ...
└── scene_2/
    └── ...
```

## 实际应用示例

### 创意视频实例
**场景**：制作一个太空探险故事视频

**输入**：
```
想法：太空探险故事
要求：3个场景，每个场景5秒，科幻风格，有角色和飞船
```

**生成过程**：
1. AI分析并生成故事脚本
2. 生成角色参考图片
3. 为每个场景生成视频片段
4. 生成TTS旁白（可选择中文语音）
5. 生成自动字幕
6. 拼接所有片段并添加音轨

**输出**：一个完整的15秒太空探险视频，包含故事情节、角色对话、场景转换、AI旁白和字幕

### 稿件视频实例
**场景**：将一篇AI文章转换为视频

**输入**：
```
稿件文本：
"人工智能正在改变我们的世界。从智能手机到自动驾驶汽车，AI技术无处不在。未来，AI将帮助医生诊断疾病，帮助科学家发现新药物，帮助教师个性化教育。"
```

**生成过程**：
1. 系统按阅读时长自动分割文本为3个片段
2. 为每个片段生成相应的视频内容
3. 生成统一的TTS旁白
4. 生成同步的字幕
5. 拼接所有片段

**输出**：一个15秒的教育视频，展示AI在不同领域的应用

### 数字主播实例
**场景**：制作产品介绍视频

**输入**：
```
主播台词："大家好！今天为大家介绍我们的新产品——智能手表。它具有健康监测、运动追踪、智能提醒等功能，是您生活的完美伴侣。"
```

**输出**：一个数字主播视频，主播形象生动，表情自然，同步显示字幕，可循环播放

## 注意事项

1. **模型局限性**：生成的帧有时不稳定，复杂动作偶尔变形
2. **完全免费**：无使用限制，迭代快速
3. **硬件要求**：普通笔记本电脑即可运行，无需高端GPU
4. **网络依赖**：所有AI计算在云端运行
5. **语言支持**：界面支持13种语言，中文语音支持4种角色

## 优势总结

- **零成本**：完全免费，无订阅费
- **易用性**：一键部署，普通电脑即可运行
- **功能丰富**：多种创作模式，AI旁白，自动字幕
- **开源**：MIT许可证，可自托管
- **多场景**：内置多场景视频生成管道
- **无水印**：生成视频无水印
- **无限制**：无使用次数限制

## 🔧 故障排除

### API端点问题（重要）

Agnes Video Generator有两个不同的API端点：
- **Chat/Image API**: `https://api.agnes-ai.cn/v1`（与国内站一致）
- **Video API**: 使用相同的base URL

**注意**：项目默认配置使用 `apihub.agnes-ai.cn`，但实际API端点是 `api.agnes-ai.cn`（无hub）。如遇到404错误，需要修改代码：

```bash
# 修改 core/config.py 第482-484行
AGNES_DOMAIN_MAP = {
    "com": "https://api.agnes-ai.com",   # 原为 apihub.agnes-ai.com
    "cn": "https://api.agnes-ai.cn",     # 原为 apihub.agnes-ai.cn
}
```

### HTTP 401 无效令牌
- 检查API Key是否为`sk-`开头
- 确认Key未过期或被撤销
- 访问 https://platform.agnes-ai.com 重新获取

### HTTP 404 Not Found
- 可能是API端点配置错误（见上方）
- 可能是视频生成权限未开通
- 检查API Key是否有视频生成权限

### HTTP 422 参数错误
- 使用 `-F` 参数（Form表单）而非 `-d`（JSON）
- 检查必填字段是否完整

### HTTP 429 速率限制
- 默认16请求/分钟
- 系统会自动重试和退避

### ModuleNotFoundError
- 运行 `pip install -r requirements.txt`
- 确保使用正确的Python环境

### ffmpeg not found
- Windows: `choco install ffmpeg` 或 `scoop install ffmpeg`
- macOS: `brew install ffmpeg`
- Docker/npm版本自动包含ffmpeg，无需单独安装

## 📚 相关资源

- **GitHub仓库**：https://github.com/lcy362/agnes-video-generator
- **在线Demo**：https://video.lichuanyang.top
- **API文档**：项目根目录 docs/ 文件夹
- **故障排查**：详见 `references/troubleshooting.md`（API Key无效、422参数错误、依赖缺失等常见问题）
- **API端点配置**：详见 `references/api-endpoint-configuration.md`（解决404错误）
- **会话记录**：详见 `references/session-2026-08-04.md`（2026-08-04调试记录，API端点配置问题）

## 📝 支持的引用文件

- `references/api-endpoint-configuration.md` - API端点配置问题解决方案（重要）
- `references/session-2026-08-04.md` - 2026-08-04会话调试记录
- `references/prompt-templates.md` - Prompt模板示例

## ⚠️ API 端点配置（重要）

**正确的国内站端点**：`https://api.agnes-ai.cn/v1`

**错误的端点**（会返回404）：`https://apihub.agnes-ai.cn/v1`

配置方法：
```bash
curl -X POST http://localhost:8765/api/config/domain -F "domain=cn"
```

**调试记录**：详见 `references/session-2026-08-04.md`（API端点配置问题排查）

## 快速开始命令

```bash
# 克隆项目
git clone https://github.com/lcy362/agnes-video-generator.git
cd agnes-video-generator

# 一键启动
./start.sh

# 或使用Docker
docker run -d -p 8765:8765 \
  -e AGNES_API_KEY=your-api-key \
  -v ~/agnes-data/working:/app/.working_dir \
  -v ~/agnes-data/config:/app/.agnes_config \
  ghcr.io/lcy362/free-short-video:latest

# 或使用npm
npx free-short-video
```

启动后访问 http://localhost:8765 开始创作你的第一个AI视频！
