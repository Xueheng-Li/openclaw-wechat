#!/usr/bin/env python3
"""Send text, image, or file messages to WeCom (企业微信) via API.

Usage:
    # Text message
    python3 send_wecom.py "Your message here"
    python3 send_wecom.py "Your message" --to LiXueHeng

    # Image message
    python3 send_wecom.py --image /path/to/photo.png
    python3 send_wecom.py --image /path/to/photo.jpg --to @all

    # File message
    python3 send_wecom.py --file /path/to/document.pdf
    python3 send_wecom.py --file /path/to/report.docx --to LiXueHeng

Reads config from ~/.openclaw/openclaw.json env.vars.
Requires proxy (WECOM_PROXY) for API access.
"""

import json
import mimetypes
import sys
import urllib.request
import uuid
from pathlib import Path


def load_config():
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if not config_path.exists():
        sys.exit("Error: ~/.openclaw/openclaw.json not found")
    data = json.loads(config_path.read_text())
    env = data.get("env", {}).get("vars", {})
    corp_id = env.get("WECOM_CORP_ID")
    corp_secret = env.get("WECOM_CORP_SECRET")
    agent_id = env.get("WECOM_AGENT_ID")
    proxy = env.get("WECOM_PROXY", "")
    if not all([corp_id, corp_secret, agent_id]):
        sys.exit("Error: Missing WECOM_CORP_ID/CORP_SECRET/AGENT_ID in config")
    return corp_id, corp_secret, int(agent_id), proxy


def get_access_token(corp_id, corp_secret, opener):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}"
    resp = opener.open(url, timeout=10)
    data = json.loads(resp.read())
    if data.get("errcode", 0) != 0:
        sys.exit(f"Error getting token: {data}")
    return data["access_token"]


def upload_media(access_token, file_path, media_type, opener):
    """Upload a temporary media file to WeCom and return media_id.

    Args:
        access_token: WeCom API access token
        file_path: Local file path to upload
        media_type: One of 'image', 'voice', 'video', 'file'
        opener: urllib opener with proxy config
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={media_type}"

    file_path = Path(file_path)
    if not file_path.exists():
        sys.exit(f"Error: File not found: {file_path}")

    filename = file_path.name
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    file_data = file_path.read_bytes()

    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    resp = opener.open(req, timeout=30)
    data = json.loads(resp.read())
    if data.get("errcode", 0) != 0:
        sys.exit(f"Error uploading media: {data}")
    return data["media_id"]


def send_text(access_token, agent_id, to_user, text, opener):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": agent_id,
        "text": {"content": text},
        "safe": 0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = opener.open(req, timeout=10)
    data = json.loads(resp.read())
    if data.get("errcode", 0) != 0:
        sys.exit(f"Error sending message: {data}")
    return data


def send_image(access_token, agent_id, to_user, media_id, opener):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "image",
        "agentid": agent_id,
        "image": {"media_id": media_id},
        "safe": 0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = opener.open(req, timeout=10)
    data = json.loads(resp.read())
    if data.get("errcode", 0) != 0:
        sys.exit(f"Error sending image: {data}")
    return data


def send_file(access_token, agent_id, to_user, media_id, opener):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "file",
        "agentid": agent_id,
        "file": {"media_id": media_id},
        "safe": 0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = opener.open(req, timeout=10)
    data = json.loads(resp.read())
    if data.get("errcode", 0) != 0:
        sys.exit(f"Error sending file: {data}")
    return data


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Send WeCom message (text/image/file)")
    parser.add_argument("message", nargs="?", default=None, help="Message text to send")
    parser.add_argument("--to", default="LiXueHeng", help="Recipient UserId (default: LiXueHeng)")
    parser.add_argument("--image", metavar="PATH", help="Send an image file")
    parser.add_argument("--file", metavar="PATH", help="Send a file")
    args = parser.parse_args()

    if not args.message and not args.image and not args.file:
        parser.error("Must provide a message, --image, or --file")

    corp_id, corp_secret, agent_id, proxy = load_config()

    if proxy:
        handler = urllib.request.ProxyHandler({"https": proxy, "http": proxy})
        opener = urllib.request.build_opener(handler)
    else:
        opener = urllib.request.build_opener()

    token = get_access_token(corp_id, corp_secret, opener)

    if args.image:
        media_id = upload_media(token, args.image, "image", opener)
        result = send_image(token, agent_id, args.to, media_id, opener)
        print(json.dumps({"ok": True, "type": "image", "to": args.to, "media_id": media_id, "msgid": result.get("msgid", "")}, ensure_ascii=False))
    elif args.file:
        media_id = upload_media(token, args.file, "file", opener)
        result = send_file(token, agent_id, args.to, media_id, opener)
        print(json.dumps({"ok": True, "type": "file", "to": args.to, "media_id": media_id, "msgid": result.get("msgid", "")}, ensure_ascii=False))
    else:
        result = send_text(token, agent_id, args.to, args.message, opener)
        print(json.dumps({"ok": True, "type": "text", "to": args.to, "msgid": result.get("msgid", "")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
