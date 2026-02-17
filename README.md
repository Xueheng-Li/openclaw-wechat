# 🤖 OpenClaw 企业微信插件（支持直接加到微信）

> ⭐ 如果觉得有用，请点击右上角的 **Star** 支持一下！

### 🔍 项目概述

**openclaw-wecom** 是一个 [OpenClaw](https://openclaw.ai)（原 ClawdBot/Moltbot）的 <img src="docs/images/wecom-icon.png" width="16" height="16"> **企业微信渠道插件**，让你的 AI 智能体通过企业微信自建应用与用户对话。接入企业微信后，<img src="docs/images/wechat-icon.png" width="16" height="16"> **个人微信用户也可以直接对话**——只需在企业微信管理后台「我的企业 → 微信插件」中扫码关联即可。

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

### 📦 前置要求

- [OpenClaw](https://openclaw.ai) 已安装并正常运行（`openclaw doctor` 通过）
- Node.js 环境（npm 可用）
- 企业微信管理员权限
- 公网可访问的服务器或隧道（用于接收企业微信回调）
- （可选）Python 3 + [FunASR](https://github.com/modelscope/FunASR) + PyTorch + FFmpeg —— 用于本地语音转文字（支持 CUDA / Apple MPS / CPU）

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

#### 第八步：关联个人微信 📱（可选）

如果希望**个人微信**也能直接与 AI 对话，需在企业微信管理后台开启微信插件：

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame)
2. 进入 **我的企业** → **微信插件**
3. 用个人微信扫描页面上的二维码，关联到企业
4. 关联后，个人微信中会出现企业的应用入口，直接发消息即可

<p align="center">
  <img src="docs/images/wecom2wechat.jpg" alt="企业微信管理后台 → 我的企业 → 微信插件" width="600">
  <br>
  <em>在企业微信管理后台「我的企业 → 微信插件」中，用个人微信扫码即可关联</em>
</p>

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
pip install funasr modelscope torch torchaudio torchcodec
```

> 🍎 **Apple Silicon (M1/M2/M3/M4) 支持：** `stt.py` 会自动检测并使用 MPS (Metal Performance Shaders) 加速推理。首次运行时模型会从 ModelScope 自动下载（约 1GB）。
>
> ⚠️ **macOS launchd 部署注意：** 如果 OpenClaw 以 launchd 服务运行，默认 `python3` 可能找不到 ML 依赖。需在 plist 中设置环境变量 `WECOM_STT_PYTHON` 指向正确的 Python 路径（如 conda 环境的 python3）。

**独立使用：**

```bash
python3 stt.py /path/to/audio.wav
```

> 💡 如果企业微信已开启语音识别（Recognition 字段），会优先使用企业微信的结果；仅在无 Recognition 字段时才会调用本地 STT。

> 🤖 **AI Agent 自动部署：** 详细的多环境（CUDA / MPS / CPU）安装部署指南见 [`docs/stt-deploy-guide.md`](docs/stt-deploy-guide.md)，可供 Claude Code 等 AI 编程助手直接参照执行自动化安装。

### 📝 使用

配置完成后，在企业微信或个人微信中找到你的应用，直接发送消息即可：

1. 📱 在企业微信中找到你创建的应用
2. 💬 发送文字、图片、语音、视频、文件消息
3. 🤖 AI 会自动回复

**<img src="docs/images/wechat-icon.png" width="16" height="16"> 个人微信接入：** 在企业微信管理后台「我的企业  → 微信插件」中，用个人微信扫码关联即可。

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
3. 首次运行会从 ModelScope 下载模型（约 1GB），需要网络连接
4. `stt.py` 会自动检测设备：CUDA GPU → Apple MPS → CPU（按优先级依次降级）

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

## 🔗 相关链接

- 🌐 [OpenClaw 官方网站](https://openclaw.ai)
- 📖 [企业微信开发文档](https://developer.work.weixin.qq.com/document/)
- 🔐 [企业微信消息加解密](https://developer.work.weixin.qq.com/document/path/90968)
- 🍴 [上游项目：dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat)
- 🎙️ [FunASR SenseVoice](https://modelscope.cn/models/iic/SenseVoiceSmall)

## 📄 许可证

[MIT License](./LICENSE)

## 🙏 致谢

- 🍴 原始项目：[dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat)，作者 **勾勾的数字生命** ([@dingxiang-me](https://github.com/dingxiang-me))
- 🤖 [OpenClaw](https://openclaw.ai)，由 Peter Steinberger 和 OpenClaw 社区开发
- 🎙️ [FunASR SenseVoice](https://github.com/modelscope/FunASR)，由阿里巴巴达摩院开发

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
