# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**openclaw-wechat** is a WeCom (Enterprise WeChat) channel plugin for OpenClaw/ClawdBot. It enables AI agents to communicate with users through WeCom's self-built applications, supporting bidirectional messaging with multiple media types.

Forked from [dingxiang-me/OpenClaw-Wechat](https://github.com/dingxiang-me/OpenClaw-Wechat) with extensive enhancements.

## Commands

```bash
# Install as OpenClaw plugin (note: "plugins" plural, not "plugin")
npm install
openclaw plugins install --link /path/to/openclaw-wechat  # --link for local dev (symlink)
openclaw plugins install /path/to/openclaw-wechat          # without --link copies to ~/.openclaw/extensions/

# Run / restart
openclaw gateway restart
# or via launchctl on macOS:
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# Verify webhook
curl https://your-domain/wecom/callback  # expect "wecom webhook ok"

# View logs
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep wecom

# List plugins
openclaw plugins list
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

Channel config in `~/.openclaw/openclaw.json` under `channels.wecom`:
- Required: `corpId`, `corpSecret`, `agentId`, `callbackToken`, `callbackAesKey`
- Optional: `webhookPath` (default `/wecom/callback`), `dmPolicy`, `allowFrom`

Environment variables (in `openclaw.json` under `env.vars` AND in the LaunchAgent plist):
- `WECOM_PROXY` — outbound proxy for WeCom API (e.g. `http://10.147.17.105:8888` for IP whitelist compliance)
- `WECOM_STT_PYTHON` — path to Python binary with FunASR installed (for voice STT)
- `PYTORCH_ENABLE_MPS_FALLBACK` — set to `1` for Apple Silicon MPS fallback

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

### WeCom IP Whitelist is Per-App
- `errcode:60020` ("not allow to access from your ip") means the proxy/server IP is not whitelisted for **this specific agent app**
- Each self-built application (agentId) has its own "企业可信IP" list — whitelisting an IP for agent 1000002 does NOT apply to agent 1000003
- When creating a new WeCom app, always add the proxy IP to that app's trusted IP list separately

### Callback URL Verification ("回调地址不通过")
- WeCom Admin's "随机获取" (random generate) creates NEW token/AES key each time you click it
- You must copy the credentials AFTER generating and BEFORE clicking save
- If credentials in `openclaw.json` don't match what WeCom expects, verification returns 401 (signature mismatch) and WeCom shows "回调地址不通过"
- Verify config is loaded: `curl https://your-domain/wecom/callback` should return "wecom webhook ok" (not "not configured")
- After updating credentials in `openclaw.json`, restart the gateway — the config change requires a full restart

### macOS LaunchAgent Env Vars
- `WECOM_PROXY`, `WECOM_STT_PYTHON`, `PYTORCH_ENABLE_MPS_FALLBACK` must be in the LaunchAgent plist (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`)
- `openclaw gateway install` / updates regenerate the plist and **wipe** manually added env vars
- Use PlistBuddy to re-add after any reinstall, or set up a WatchPaths auto-patcher

### Cron / Scheduled Messages
- Best pattern: isolated session + `agentTurn` + `delivery.mode: "none"` + agent calls `message` tool itself
- Main session `systemEvent` can timeout when session is busy
- Cron jobs auto-disable after 3 consecutive errors
