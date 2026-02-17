# 🤖 OpenClaw WeCom Plugin / 企业微信插件

> 🇨🇳 [中文](#-中文文档) | 🇬🇧 [English](#-english-documentation)

---

## 📖 中文文档

### 🔍 项目概述

**openclaw-wecom** 是一个 [OpenClaw](https://openclaw.ai)（原 ClawdBot/Moltbot）的**企业微信渠道插件**，让你的 AI 智能体通过企业微信（WeCom）自建应用与用户对话。接入企业微信后，**个人微信用户也可以直接对话**（通过"我的企业 → 微信插件"扫码关联）。

> 🍴 本项目 fork 自 [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat)（v0.1.0，作者：勾勾的数字生命），并进行了大量功能扩展以兼容新版 OpenClaw。

### ✨ 与上游的主要区别

| 特性 | 上游 (OpenClaw-Wechat v0.1.0) | 本 Fork (v0.3.1) |
|------|------|------|
| 🎯 平台兼容 | ClawdBot | OpenClaw（同时保留 ClawdBot 兼容） |
| 📄 插件描述文件 | `clawdbot.plugin.json` | `openclaw.plugin.json` + `clawdbot.plugin.json` |
| ⚙️ 配置文件 | `~/.clawdbot/clawdbot.json` | `~/.openclaw/openclaw.json` |
| 📨 消息类型 | 文本、图片、语音 | 文本、图片、语音、**视频**、**文件**、**链接** |
| 🎙️ 语音识别 | 仅企业微信自带 | 企业微信自带 + **本地 FunASR SenseVoice STT** |
| 🖥️ Chat UI | 无 | **消息同步到 Transcript + 实时广播** |
| 🌐 代理支持 | 无 | **WECOM_PROXY 环境变量** |
| 📝 消息分段 | 按字符 | **按字节（UTF-8），二分查找分割** |

### 📋 功能特性

#### 🔌 核心功能
- [x] ✅ 支持个人微信对话（通过企业微信桥接）
- [x] ✅ 接收/发送企业微信消息
- [x] ✅ 自动调用 AI 代理处理消息
- [x] ✅ 消息签名验证（SHA1）和 AES-256-CBC 加解密
- [x] ✅ Webhook URL 验证
- [x] ✅ access_token 自动缓存和刷新

#### 🎬 媒体功能
- [x] 🖼️ 图片消息收发 + AI Vision 识别
- [x] 🎙️ 语音消息转文字（企业微信自带 + 本地 FunASR SenseVoice）
- [x] 📹 视频消息接收、下载、发送
- [x] 📎 文件消息接收（支持 .txt/.md/.json/.pdf 等自动读取）
- [x] 🔗 链接分享消息接收

#### 🎨 用户体验
- [x] 📝 命令系统（`/help`、`/status`、`/clear`）
- [x] 🔄 Markdown → 纯文本自动转换（企业微信不支持 Markdown 渲染）
- [x] ✂️ 长消息自动分段（2048 字节限制，按 UTF-8 字节精确分割）
- [x] 🛡️ API 限流保护（3 并发，200ms 间隔）
- [x] ⏳ 处理中提示（"收到您的消息，正在处理中..."）

#### 🚀 高级功能
- [x] 👥 多账户支持（`WECOM_<ACCOUNT>_*` 格式）
- [x] 💬 群聊支持
- [x] 🔒 Token 并发安全（Promise 锁）
- [x] 🖥️ Chat UI 集成（Transcript 写入 + Gateway 实时广播）
- [x] 🌐 HTTP 代理支持（`WECOM_PROXY`）

### 📊 支持的消息类型

| 类型 | 接收 | 发送 | 说明 |
|:----:|:----:|:----:|------|
| 📝 文本 | ✅ | ✅ | 完全支持，超长消息自动按字节分段 |
| 🖼️ 图片 | ✅ | ✅ | 支持 AI Vision 识别，下载后保存到临时文件 |
| 🎙️ 语音 | ✅ | ❌ | 企业微信自带识别 + 本地 FunASR SenseVoice STT（AMR→WAV→文本） |
| 📹 视频 | ✅ | ✅ | 自动下载保存，支持发送视频消息 |
| 📎 文件 | ✅ | ✅ | 自动下载，可读类型自动交给 AI 分析 |
| 🔗 链接 | ✅ | ❌ | 提取标题/描述/URL，可用 WebFetch 获取内容 |

### 📦 前置要求

- [OpenClaw](https://openclaw.ai) 已安装并正常运行（`openclaw doctor` 通过）
- Node.js 环境（npm 可用）
- 企业微信管理员权限
- 公网可访问的服务器或隧道（用于接收企业微信回调）
- （可选）Python 3 + [FunASR](https://github.com/modelscope/FunASR) + FFmpeg —— 用于本地语音转文字

### 🛠️ 安装

#### 方式一：CLI 安装

```bash
openclaw plugin install --path /path/to/openclaw-wecom
```

#### 方式二：手动安装

1. 克隆本仓库：

```bash
git clone https://github.com/xueheng-li/openclaw-wecom.git
cd openclaw-wecom
npm install
```

2. 在 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 中注册插件：

```json
{
  "plugins": {
    "load": {
      "paths": [
        "/path/to/openclaw-wecom"
      ]
    },
    "entries": {
      "clawdbot-wecom": {
        "enabled": true
      }
    }
  }
}
```

> 💡 **注意**：插件 ID 为 `clawdbot-wecom`（保持与上游兼容）。配置中请使用此 ID，而非 `openclaw-wecom`。
> 💡 **Note**: The plugin ID is `clawdbot-wecom` (for backward compatibility with upstream). Use this ID in configuration, not `openclaw-wecom`.

### ⚙️ 配置（详细步骤）

#### 第一步：创建企业微信自建应用 🏢

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame)
2. 进入 **应用管理** → **自建** → **创建应用**
3. 填写应用名称、Logo、可见范围等信息
4. 创建完成后，记录：
   - **AgentId**：应用的 AgentId
   - **Secret**：应用的 Secret

#### 第二步：获取企业信息 🆔

1. 在管理后台首页，点击 **我的企业**
2. 记录 **企业ID (CorpId)**

#### 第三步：配置接收消息 📨

1. 进入你创建的应用 → **接收消息** → **设置API接收**
2. 填写：
   - **URL**：`https://你的域名/wecom/callback`
   - **Token**：自定义一个 Token（随机字符串）
   - **EncodingAESKey**：点击随机生成
3. ⚠️ **先不要保存！** 需要先完成后续步骤启动 OpenClaw 服务

#### 第四步：配置环境变量 🔑

在 `~/.openclaw/openclaw.json` 中添加环境变量：

```json
{
  "env": {
    "vars": {
      "WECOM_CORP_ID": "你的企业ID",
      "WECOM_CORP_SECRET": "你的应用Secret",
      "WECOM_AGENT_ID": "你的应用AgentId",
      "WECOM_CALLBACK_TOKEN": "你设置的Token",
      "WECOM_CALLBACK_AES_KEY": "你生成的EncodingAESKey",
      "WECOM_WEBHOOK_PATH": "/wecom/callback",
      "WECOM_PROXY": ""
    }
  }
}
```

##### 多账户配置

支持配置多个企业微信账户，使用 `WECOM_<ACCOUNT>_*` 格式：

```json
{
  "env": {
    "vars": {
      "WECOM_CORP_ID": "默认账户企业ID",
      "WECOM_CORP_SECRET": "默认账户Secret",
      "WECOM_AGENT_ID": "默认账户AgentId",
      "WECOM_CALLBACK_TOKEN": "默认账户Token",
      "WECOM_CALLBACK_AES_KEY": "默认账户AESKey",

      "WECOM_SALES_CORP_ID": "销售账户企业ID",
      "WECOM_SALES_CORP_SECRET": "销售账户Secret",
      "WECOM_SALES_AGENT_ID": "销售账户AgentId",
      "WECOM_SALES_CALLBACK_TOKEN": "销售账户Token",
      "WECOM_SALES_CALLBACK_AES_KEY": "销售账户AESKey"
    }
  }
}
```

#### 第五步：配置 Gateway 🌐

确保 Gateway 配置允许外部连接：

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan"
  }
}
```

> ⚠️ `bind` 必须为 `"lan"`（而非 `"localhost"`），否则企业微信回调无法到达。

#### 第六步：配置公网访问 🔗

企业微信需要能够访问你的回调 URL。推荐使用 Cloudflare Tunnel：

```bash
# 安装 cloudflared
brew install cloudflared   # macOS
# 或 apt install cloudflared  # Linux

# 创建隧道
cloudflared tunnel create openclaw

# 配置隧道路由
cloudflared tunnel route dns openclaw 你的域名

# 启动隧道（将流量转发到本地 Gateway 端口）
cloudflared tunnel --url http://localhost:18789 run openclaw
```

其他方案：SSH 隧道、Tailscale、Nginx 反向代理 + 端口转发等。

#### 第七步：启动并验证 🚀

1. 重启 OpenClaw Gateway：

```bash
openclaw gateway restart
```

2. 检查插件是否加载：

```bash
openclaw plugin list
```

3. 验证 Webhook 可达：

```bash
curl https://你的域名/wecom/callback
# 应返回 "wecom webhook ok"
```

4. 回到企业微信管理后台，点击**保存**回调配置
5. 如果验证通过，配置完成！🎉

### 🎙️ 本地语音转文字（stt.py）

本 fork 新增了 `stt.py`，使用 [FunASR SenseVoice-Small](https://modelscope.cn/models/iic/SenseVoiceSmall) 模型进行本地语音识别，无需依赖企业微信自带的语音识别功能。

**工作流程：**
1. 收到语音消息 → 下载 AMR 音频文件
2. 使用 FFmpeg 转换为 WAV（16kHz 单声道）
3. 调用 `stt.py` 进行 FunASR SenseVoice 语音识别
4. 将识别结果作为文本消息发送给 AI 代理

**依赖安装：**

```bash
# FFmpeg（音频格式转换）
brew install ffmpeg        # macOS
# 或 apt install ffmpeg    # Linux

# Python 依赖
pip install funasr modelscope
```

**独立使用：**

```bash
python3 stt.py /path/to/audio.wav
```

> 💡 如果企业微信已开启语音识别（Recognition 字段），会优先使用企业微信的结果；仅在无 Recognition 字段时才会调用本地 STT。

### 📝 使用

配置完成后，在企业微信或个人微信中找到你的应用，直接发送消息即可：

1. 📱 在企业微信中找到你创建的应用
2. 💬 发送文字、图片、语音、视频、文件消息
3. 🤖 AI 会自动回复

**个人微信接入：** 在微信中打开 "我的企业" → "微信插件"，用个人微信扫码关联即可。

#### 命令系统

| 命令 | 说明 |
|------|------|
| `/help` | 📋 显示帮助信息 |
| `/status` | 📊 查看系统状态（含账户信息） |
| `/clear` | 🗑️ 清除会话历史，开始新对话 |

### 🔧 环境变量参考

| 变量名 | 必填 | 默认值 | 说明 |
|--------|:----:|--------|------|
| `WECOM_CORP_ID` | ✅ | — | 企业微信企业 ID |
| `WECOM_CORP_SECRET` | ✅ | — | 自建应用的 Secret |
| `WECOM_AGENT_ID` | ✅ | — | 自建应用的 AgentId |
| `WECOM_CALLBACK_TOKEN` | ✅ | — | 回调配置的 Token |
| `WECOM_CALLBACK_AES_KEY` | ✅ | — | 回调配置的 EncodingAESKey（43 字符 Base64） |
| `WECOM_WEBHOOK_PATH` | ❌ | `/wecom/callback` | Webhook 路径 |
| `WECOM_PROXY` | ❌ | — | 出站 WeCom API 的 HTTP 代理地址（如 `http://10.x.x.x:8888`） |

### 🔍 故障排查

#### ❌ 回调验证失败

1. 检查 URL 是否可公网访问：
```bash
curl https://你的域名/wecom/callback
# 应返回 "wecom webhook ok"
```

2. 检查环境变量是否正确配置（Token 和 AESKey 必须与企业微信后台一致）

3. 查看 OpenClaw 日志：
```bash
openclaw logs -f | grep wecom
```

#### ❌ 消息没有回复

1. 检查日志中是否有 `wecom inbound` 记录
2. 确认 AI 模型配置正确（检查 `agents.defaults.model`）
3. 检查是否有错误日志

#### ❌ access_token 获取失败

1. 确认 `WECOM_CORP_ID` 和 `WECOM_CORP_SECRET` 正确
2. 检查应用的可见范围是否包含测试用户
3. 确认服务器能访问 `qyapi.weixin.qq.com`（如有代理需设置 `WECOM_PROXY`）

#### ❌ 语音识别失败

1. 确认已安装 FFmpeg：`ffmpeg -version`
2. 确认已安装 Python 依赖：`python3 -c "from funasr import AutoModel"`
3. 首次运行会从 ModelScope 下载模型，需要网络连接
4. `stt.py` 会自动检测 CUDA GPU，无 GPU 时自动使用 CPU

### 🏗️ 架构

```
┌──────────────┐         ┌──────────────────┐         ┌───────────────┐
│  企业微信     │ ──XML──▶│ OpenClaw Gateway │ ──────▶ │  AI Agent     │
│  / 个人微信   │         │  (port 18789)    │         │  (LLM)        │
│              │ ◀──API──│                  │ ◀────── │               │
└──────────────┘         └──────┬───────────┘         └───────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │ 消息加解密 │ │ STT    │ │ Chat UI  │
              │ AES-256  │ │ FunASR │ │ Broadcast│
              └──────────┘ └────────┘ └──────────┘
```

**消息流程：**

1. 📩 用户在企业微信/个人微信发送消息
2. 🔒 企业微信服务器将加密的 XML 回调发送到你的 Webhook URL
3. 🔓 插件验证签名，解密消息（AES-256-CBC）
4. ⚡ 立即返回 HTTP 200（企业微信要求 5 秒内响应）
5. 🔄 异步处理：根据消息类型分发处理
   - 📝 文本 → 直接交给 AI
   - 🖼️ 图片 → 下载保存 → AI Vision 分析
   - 🎙️ 语音 → 下载 AMR → FFmpeg 转 WAV → FunASR STT → 文本交给 AI
   - 📹 视频/📎 文件 → 下载保存 → 通知 AI
   - 🔗 链接 → 提取元信息 → 交给 AI
6. 🤖 AI 代理生成回复
7. 📤 回复经 Markdown 转换后，自动分段发送回企业微信
8. 🖥️ 同时写入 Transcript + 广播到 Chat UI

### 📁 项目结构

```
openclaw-wecom/
├── index.js                 # 入口文件（重导出）
├── src/
│   └── index.js             # 插件主逻辑（1400+ 行）
├── stt.py                   # 🎙️ 本地语音识别（FunASR SenseVoice）
├── openclaw.plugin.json     # OpenClaw 插件描述文件（新格式）
├── clawdbot.plugin.json     # ClawdBot 插件描述文件（兼容旧版）
├── package.json             # npm 包配置 (v0.3.1)
├── .env.example             # 环境变量示例
├── skills/
│   └── wecom-notify/        # 📨 Claude Code WeCom 通知技能
│       ├── SKILL.md
│       └── scripts/
│           └── send_wecom.py
├── docs/
│   └── channels/
│       └── wecom.md         # 渠道文档
├── CHANGELOG.md             # 版本变更日志
└── LICENSE                  # MIT 许可证
```

### 📨 Claude Code WeCom 通知技能

本仓库还包含一个独立的 **Claude Code 技能**（`wecom-notify`），可以在 Claude Code 中直接发送企业微信消息。这是一个**独立工具**，不依赖 OpenClaw 插件，直接调用企业微信 API。

#### 安装技能

将 `skills/wecom-notify/` 目录复制到 `~/.claude/skills/` 即可：

```bash
cp -r skills/wecom-notify ~/.claude/skills/
```

#### 使用方式

在 Claude Code 中可以直接使用 `/wecom-notify` 命令，或让 AI 自动调用：

```bash
# 发送文本消息
python3 skills/wecom-notify/scripts/send_wecom.py "你好，这是一条测试消息"

# 指定接收人
python3 skills/wecom-notify/scripts/send_wecom.py "消息内容" --to UserName

# 发送图片
python3 skills/wecom-notify/scripts/send_wecom.py --image /path/to/photo.png

# 发送文件
python3 skills/wecom-notify/scripts/send_wecom.py --file /path/to/report.pdf
```

#### 特点

- 🔧 **零依赖**：仅使用 Python 标准库（`urllib.request`、`json`），无需 `pip install`
- 📄 自动从 `~/.openclaw/openclaw.json` 读取 WeCom 配置（复用 OpenClaw 的环境变量）
- 📝 支持文本（2048 字节限制）、图片（jpg/png/gif，≤2MB）、文件（任意格式，≤20MB）
- 🌐 支持 `WECOM_PROXY` 代理

### 📜 版本历史

查看 [CHANGELOG.md](./CHANGELOG.md) 了解完整版本历史。

---

## 🇬🇧 English Documentation

### 🔍 Overview

**openclaw-wecom** is a **WeCom (Enterprise WeChat) channel plugin** for [OpenClaw](https://openclaw.ai) (formerly ClawdBot/Moltbot). It connects your AI agent to WeCom via a self-built application, enabling intelligent conversations. Once connected, **personal WeChat users can also chat** with your AI (via "My Enterprise" > "WeChat Plugin" QR code linking).

> 🍴 This project is forked from [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat) (v0.1.0, by "勾勾的数字生命") and has been significantly extended for compatibility with newer versions of OpenClaw.

### ✨ Key Differences from Upstream

| Feature | Upstream (v0.1.0) | This Fork (v0.3.1) |
|---------|-------------------|---------------------|
| 🎯 Platform | ClawdBot | OpenClaw (with ClawdBot backward compat) |
| 📄 Manifest | `clawdbot.plugin.json` | `openclaw.plugin.json` + `clawdbot.plugin.json` |
| ⚙️ Config | `~/.clawdbot/clawdbot.json` | `~/.openclaw/openclaw.json` |
| 📨 Messages | Text, Image, Voice | Text, Image, Voice, **Video**, **File**, **Link** |
| 🎙️ Voice STT | WeCom built-in only | WeCom built-in + **local FunASR SenseVoice** |
| 🖥️ Chat UI | None | **Transcript sync + real-time broadcast** |
| 🌐 Proxy | None | **WECOM_PROXY env var** |
| ✂️ Splitting | By character | **By UTF-8 byte with binary search** |

### 📊 Supported Message Types

| Type | Receive | Send | Notes |
|:----:|:-------:|:----:|-------|
| 📝 Text | ✅ | ✅ | Full support, auto-segmentation by byte limit |
| 🖼️ Image | ✅ | ✅ | AI Vision recognition, saved to temp files |
| 🎙️ Voice | ✅ | ❌ | WeCom built-in + local FunASR SenseVoice (AMR→WAV→Text) |
| 📹 Video | ✅ | ✅ | Auto-download and save |
| 📎 File | ✅ | ✅ | Auto-download, readable types auto-analyzed by AI |
| 🔗 Link | ✅ | ❌ | Extracts title/description/URL |

### 📦 Prerequisites

- [OpenClaw](https://openclaw.ai) installed and running (`openclaw doctor` passes)
- Node.js environment (npm available)
- WeCom (Enterprise WeChat) admin access
- Public-facing server or tunnel (for receiving WeCom callbacks)
- (Optional) Python 3 + [FunASR](https://github.com/modelscope/FunASR) + FFmpeg -- for local voice-to-text

### 🛠️ Installation

#### Option 1: CLI Install

```bash
openclaw plugin install --path /path/to/openclaw-wecom
```

#### Option 2: Manual Install

```bash
git clone https://github.com/xueheng-li/openclaw-wecom.git
cd openclaw-wecom
npm install
```

Then add to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "load": {
      "paths": ["/path/to/openclaw-wecom"]
    },
    "entries": {
      "clawdbot-wecom": {
        "enabled": true
      }
    }
  }
}
```

### ⚙️ Configuration

#### Step 1: Create a WeCom Self-Built App 🏢

1. Log in to [WeCom Admin Console](https://work.weixin.qq.com/wework_admin/frame)
2. Go to **Application Management** > **Self-Built** > **Create Application**
3. Note the **AgentId** and **Secret**

#### Step 2: Get Enterprise Info 🆔

1. On the admin console homepage, click **My Enterprise**
2. Note the **Corp ID**

#### Step 3: Configure Callback 📨

1. Go to your app > **Receive Messages** > **Set API Receive**
2. Fill in:
   - **URL**: `https://your-domain/wecom/callback`
   - **Token**: A random string
   - **EncodingAESKey**: Click to randomly generate
3. ⚠️ **Do NOT save yet!** Start the OpenClaw service first.

#### Step 4: Set Environment Variables 🔑

In `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "vars": {
      "WECOM_CORP_ID": "your_corp_id",
      "WECOM_CORP_SECRET": "your_app_secret",
      "WECOM_AGENT_ID": "your_agent_id",
      "WECOM_CALLBACK_TOKEN": "your_token",
      "WECOM_CALLBACK_AES_KEY": "your_43_char_aes_key",
      "WECOM_WEBHOOK_PATH": "/wecom/callback",
      "WECOM_PROXY": ""
    }
  }
}
```

#### Step 5: Configure Gateway 🌐

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan"
  }
}
```

> ⚠️ `bind` must be `"lan"` (not `"localhost"`) for WeCom callbacks to reach the gateway.

#### Step 6: Set Up Public Access 🔗

WeCom must be able to reach your callback URL. Recommended: Cloudflare Tunnel.

```bash
brew install cloudflared
cloudflared tunnel create openclaw
cloudflared tunnel route dns openclaw your-domain
cloudflared tunnel --url http://localhost:18789 run openclaw
```

#### Step 7: Start and Verify 🚀

```bash
# Restart gateway
openclaw gateway restart

# Check plugin loaded
openclaw plugin list

# Verify webhook is reachable
curl https://your-domain/wecom/callback
# Should return "wecom webhook ok"
```

Then go back to the WeCom admin console and **save** the callback configuration.

### 🎙️ Local Voice-to-Text (stt.py)

This fork includes `stt.py` which uses [FunASR SenseVoice-Small](https://modelscope.cn/models/iic/SenseVoiceSmall) for local speech recognition, independent of WeCom's built-in voice recognition.

**Pipeline:** Voice AMR → FFmpeg → WAV (16kHz mono) → FunASR SenseVoice → Text

**Setup:**

```bash
# FFmpeg
brew install ffmpeg        # macOS
# or apt install ffmpeg    # Linux

# Python dependencies
pip install funasr modelscope
```

**Standalone usage:**

```bash
python3 stt.py /path/to/audio.wav
```

> 💡 If WeCom provides a Recognition field (built-in STT), that is used first. Local STT is only invoked as a fallback.

### 🔧 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|:--------:|---------|-------------|
| `WECOM_CORP_ID` | ✅ | — | WeCom Enterprise Corp ID |
| `WECOM_CORP_SECRET` | ✅ | — | Self-built app Secret |
| `WECOM_AGENT_ID` | ✅ | — | Self-built app Agent ID |
| `WECOM_CALLBACK_TOKEN` | ✅ | — | Callback verification Token |
| `WECOM_CALLBACK_AES_KEY` | ✅ | — | Callback AES encryption key (43-char Base64) |
| `WECOM_WEBHOOK_PATH` | ❌ | `/wecom/callback` | Webhook path |
| `WECOM_PROXY` | ❌ | — | HTTP proxy for outbound WeCom API calls (e.g. `http://10.x.x.x:8888`) |

### 🔍 Troubleshooting

#### Callback Verification Failed
1. Check if the URL is publicly accessible: `curl https://your-domain/wecom/callback`
2. Ensure Token and AESKey match the WeCom admin console
3. Check logs: `openclaw logs -f | grep wecom`

#### No Reply to Messages
1. Look for `wecom inbound` in logs
2. Verify AI model configuration (`agents.defaults.model`)
3. Check for error logs

#### access_token Fetch Failed
1. Verify `WECOM_CORP_ID` and `WECOM_CORP_SECRET`
2. Ensure the app's visibility scope includes the test user
3. Confirm the server can reach `qyapi.weixin.qq.com` (set `WECOM_PROXY` if behind a firewall)

#### Voice Recognition Failed
1. Verify FFmpeg is installed: `ffmpeg -version`
2. Verify Python deps: `python3 -c "from funasr import AutoModel"`
3. First run downloads the model from ModelScope (requires internet)
4. `stt.py` auto-detects CUDA GPU; falls back to CPU automatically

### 🏗️ Architecture

```
┌──────────────┐         ┌──────────────────┐         ┌───────────────┐
│  WeCom /     │ ──XML──▶│ OpenClaw Gateway │ ──────▶ │  AI Agent     │
│  Personal WX │         │  (port 18789)    │         │  (LLM)        │
│              │ ◀──API──│                  │ ◀────── │               │
└──────────────┘         └──────┬───────────┘         └───────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │ Crypto   │ │ STT    │ │ Chat UI  │
              │ AES-256  │ │ FunASR │ │ Broadcast│
              └──────────┘ └────────┘ └──────────┘
```

**Message Flow:**

1. 📩 User sends a message in WeCom / personal WeChat
2. 🔒 WeCom servers send an encrypted XML callback to your webhook URL
3. 🔓 Plugin verifies the signature and decrypts the message (AES-256-CBC)
4. ⚡ Immediately returns HTTP 200 (WeCom requires a response within 5 seconds)
5. 🔄 Async processing based on message type (text/image/voice/video/file/link)
6. 🤖 AI agent generates a reply
7. 📤 Reply is converted from Markdown to plain text, auto-segmented, and sent back
8. 🖥️ Simultaneously written to Transcript and broadcast to Chat UI

### 📁 Project Structure

```
openclaw-wecom/
├── index.js                 # Entry point (re-export)
├── src/
│   └── index.js             # Plugin main logic (1400+ lines)
├── stt.py                   # 🎙️ Local voice recognition (FunASR SenseVoice)
├── openclaw.plugin.json     # OpenClaw plugin manifest (new format)
├── clawdbot.plugin.json     # ClawdBot plugin manifest (legacy compat)
├── package.json             # npm package config (v0.3.1)
├── .env.example             # Environment variable template
├── skills/
│   └── wecom-notify/        # 📨 Claude Code WeCom notification skill
│       ├── SKILL.md
│       └── scripts/
│           └── send_wecom.py
├── docs/
│   └── channels/
│       └── wecom.md         # Channel documentation
├── CHANGELOG.md             # Version changelog
└── LICENSE                  # MIT License
```

### 📨 Claude Code WeCom Notification Skill

This repo also includes a standalone **Claude Code skill** (`wecom-notify`) for sending WeCom messages directly from Claude Code. It is an **independent tool** that calls the WeCom API directly — no OpenClaw plugin required.

#### Installing the Skill

Copy the `skills/wecom-notify/` directory to `~/.claude/skills/`:

```bash
cp -r skills/wecom-notify ~/.claude/skills/
```

#### Usage

Use the `/wecom-notify` command in Claude Code, or let the AI invoke it automatically:

```bash
# Send a text message
python3 skills/wecom-notify/scripts/send_wecom.py "Hello, this is a test message"

# Specify recipient
python3 skills/wecom-notify/scripts/send_wecom.py "Message content" --to UserName

# Send an image
python3 skills/wecom-notify/scripts/send_wecom.py --image /path/to/photo.png

# Send a file
python3 skills/wecom-notify/scripts/send_wecom.py --file /path/to/report.pdf
```

#### Features

- 🔧 **Zero dependencies**: Uses only Python stdlib (`urllib.request`, `json`) — no `pip install` needed
- 📄 Reads WeCom config automatically from `~/.openclaw/openclaw.json` (reuses OpenClaw env vars)
- 📝 Supports text (2048-byte limit), images (jpg/png/gif, ≤2MB), and files (any format, ≤20MB)
- 🌐 Supports `WECOM_PROXY` for proxy routing

### 📜 Version History

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.

---

## 🔗 相关链接 / Related Links

- 🌐 [OpenClaw Official Site](https://openclaw.ai)
- 📖 [企业微信开发文档 / WeCom Developer Docs](https://developer.work.weixin.qq.com/document/)
- 🔐 [企业微信消息加解密 / WeCom Message Encryption](https://developer.work.weixin.qq.com/document/path/90968)
- 🍴 [Upstream: dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat)
- 🎙️ [FunASR SenseVoice](https://modelscope.cn/models/iic/SenseVoiceSmall)

## 📄 许可证 / License

[MIT License](./LICENSE)

## 🙏 致谢 / Acknowledgments

- 🍴 原始项目 / Original project: [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat) by **勾勾的数字生命** ([@dingxiang-me](https://github.com/dingxiang-me))
- 🤖 [OpenClaw](https://openclaw.ai) by Peter Steinberger and the OpenClaw community
- 🎙️ [FunASR SenseVoice](https://github.com/modelscope/FunASR) by Alibaba DAMO Academy

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！ / Issues and Pull Requests are welcome!
