# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**openclaw-wechat** is a WeCom (Enterprise WeChat) channel plugin for OpenClaw/ClawdBot. It enables AI agents to communicate with users through WeCom's self-built applications, supporting bidirectional messaging with multiple media types.

Forked from [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat) with extensive enhancements.

## Commands

```bash
# Install as OpenClaw plugin
openclaw plugin install --path /path/to/openclaw-wechat
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

Plugin manifest: `openclaw.plugin.json` (plugin ID: `wecom`)

## Development Notes

- **ES Modules** — `"type": "module"` in package.json; use `import`/`export`
- **Dependencies** — only `fast-xml-parser` and `clawdbot` (peer); proxy via built-in `undici`
- **Comments** — bilingual (Chinese + English) throughout
- **Adding message types** — parse in `parseIncomingXml()` → handle in `processInboundMessage()` → create `sendWecom<Type>()` → update README/CHANGELOG
- **Security** — XXE prevention (entity processing disabled), signature verification on all callbacks, 1MB body limit

## Lessons Learned (Production Issues & Fixes)

### Voice STT (stt.py)
- `stt.py` uses FunASR SenseVoice-Small which lives in a conda environment (e.g. `sci`), not the system Python
- Set `WECOM_STT_PYTHON` env var in `openclaw.json → env.vars` to point to the correct Python binary (e.g. `/path/to/anaconda3/envs/sci/bin/python3`)
- The code reads `process.env.WECOM_STT_PYTHON || "python3"` — if unset, it falls back to system python which won't have funasr

### Outbound Media (sendMedia / deliverReply)
- **OpenClaw requires both `sendText` AND `sendMedia`** in the outbound object — if either is missing, `createPluginHandler()` returns null → "Outbound not configured"
- `sendMedia` must handle all file types, not just images — use `resolveWecomMediaType()` to detect type from file extension (image/video/file)
- `fetchMediaFromUrl` must support local file paths (`/` and `~` prefixes) in addition to HTTP URLs — use `readFile` for local, `fetch` for remote
- `deliverReply` should also use `resolveWecomMediaType()` instead of checking `mediaType === "image"`

### OpenClaw Media Security Model
- OpenClaw's core enforces `mediaLocalRoots` — only files within allowed directories can be sent: `tmpdir`, `~/.openclaw/media`, `~/.openclaw/agents`, `~/.openclaw/workspace`, `~/.openclaw/sandboxes`
- Files outside these roots are silently blocked by `assertLocalMediaAllowed()` — the plugin's sendMedia never gets called
- **Workaround**: copy files to `~/.openclaw/workspace/` before sending, then clean up after

### Flat Channel Config (no `accounts` field)
- When config uses flat structure (`channels.wecom.corpId` directly, no `accounts` sub-object), `listAccountIds` must return `["default"]` if `corpId` exists
- `resolveAccount` must fall back to top-level wecom config when `accounts[id]` is undefined

### Cron / Scheduled Messages
- Best pattern: isolated session + `agentTurn` + `delivery.mode: "none"` + agent calls `message` tool itself
- Main session `systemEvent` can timeout when session is busy
- Cron jobs auto-disable after 3 consecutive errors
