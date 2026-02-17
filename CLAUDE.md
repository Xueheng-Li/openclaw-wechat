# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**openclaw-wecom** is a WeCom (Enterprise WeChat) channel plugin for OpenClaw/ClawdBot. It enables AI agents to communicate with users through WeCom's self-built applications, supporting bidirectional messaging with multiple media types.

Forked from [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat) with extensive enhancements.

## Commands

```bash
# Install as OpenClaw plugin
openclaw plugin install --path /path/to/openclaw-wecom
npm install

# Run / restart
openclaw gateway restart

# Verify webhook
curl https://your-domain/wecom/callback

# View logs
openclaw logs -f | grep wecom

# List plugins
openclaw plugin list
```

No test suite, linter, or build step — ES modules run directly.

## Architecture

The plugin is a single-file Node.js ES module (`src/index.js`, ~1400 lines) that:

1. **Registers an HTTP endpoint** (`/wecom/callback`) handling both GET (webhook verification) and POST (message callbacks)
2. **Decrypts inbound messages** using WeCom's AES-256-CBC + SHA-1 signature scheme
3. **Parses XML payloads** into structured messages (text, image, voice, video, file, link)
4. **Routes messages** through OpenClaw's conversation API
5. **Sends responses** back via WeCom's REST API with rate limiting and message segmentation

Entry: `index.js` → re-exports `src/index.js`

### Key Design Patterns

- **Token caching with Promise locking** — prevents concurrent token refresh race conditions (`getWecomAccessToken`)
- **Semaphore-based rate limiting** — max 3 concurrent WeCom API requests, 200ms interval
- **Binary search UTF-8 segmentation** — `splitWecomText()` splits long messages by byte count (2048B limit), not character count
- **Proxy routing** — `wecomFetch()` wraps `fetch()` with optional `undici.ProxyAgent` for isolated networks
- **Multi-account isolation** — per-account token caching via `WECOM_<ACCOUNT>_*` env var prefixes

### Key Constants

```javascript
WECOM_TEXT_BYTE_LIMIT = 2048      // Max bytes per text message
MAX_REQUEST_BODY_SIZE = 1024*1024 // 1MB request body limit
API_RATE_LIMIT = 3                // Max concurrent API requests
API_REQUEST_DELAY_MS = 200        // Delay between requests
```

### Supporting Components

- **`stt.py`** — FunASR SenseVoice-Small voice-to-text (requires Python, FFmpeg)
- **`skills/wecom-notify/`** — Claude Code skill for sending WeCom notifications (stdlib-only Python)
- **`docs/channels/wecom.md`** — Channel documentation

## Configuration

Environment variables in `~/.openclaw/openclaw.json`:
- Required: `WECOM_CORP_ID`, `WECOM_CORP_SECRET`, `WECOM_AGENT_ID`, `WECOM_CALLBACK_TOKEN`, `WECOM_CALLBACK_AES_KEY`
- Optional: `WECOM_WEBHOOK_PATH` (default `/wecom/callback`), `WECOM_PROXY`

Plugin manifest: `openclaw.plugin.json` (plugin ID: `clawdbot-wecom`)

## Development Notes

- **ES Modules** — `"type": "module"` in package.json; use `import`/`export`
- **Dependencies** — only `fast-xml-parser` and `clawdbot` (peer); proxy via built-in `undici`
- **Comments** — bilingual (Chinese + English) throughout
- **Adding message types** — parse in `parseIncomingXml()` → handle in `processInboundMessage()` → create `sendWecom<Type>()` → update README/CHANGELOG
- **Security** — XXE prevention (entity processing disabled), signature verification on all callbacks, 1MB body limit
