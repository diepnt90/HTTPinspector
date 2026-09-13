import base64
import json
import os
import threading
import time
import urllib.request
from mitmproxy import http

ENDPOINT = os.environ.get("INSPECTOR_ENDPOINT", "").rstrip("/")
BODY_LIMIT = int(os.environ.get("BODY_LIMIT", str(256 * 1024)))
POST_TIMEOUT = float(os.environ.get("POST_TIMEOUT", "5"))


def headers_to_dict(headers):
    out = {}
    for key, value in headers.items(multi=True):
        if key in out:
            out[key] = f"{out[key]}\n{value}"
        else:
            out[key] = value
    return out


def encode_body(raw):
    if raw is None:
        return "", "utf8", 0, False
    size = len(raw)
    if size > BODY_LIMIT:
        return "", "utf8", size, True
    if not raw:
        return "", "utf8", 0, False
    try:
        return raw.decode("utf-8"), "utf8", size, False
    except UnicodeDecodeError:
        return base64.b64encode(raw).decode("ascii"), "base64", size, False


def post_event(payload):
    if not ENDPOINT:
        return
    url = ENDPOINT + "/api/inspector/logs"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "HTTPinspector-Pi/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=POST_TIMEOUT) as response:
            response.read(256)
    except Exception as exc:
        print(f"[HTTPinspector] upload failed: {exc}")


def submit(payload):
    threading.Thread(target=post_event, args=(payload,), daemon=True).start()


def build_base(flow: http.HTTPFlow):
    req = flow.request
    body, encoding, body_size, skipped = encode_body(req.raw_content)
    started = getattr(flow, "timestamp_start", None) or time.time()
    return {
        "timestamp": int(started * 1000),
        "method": req.method,
        "scheme": req.scheme,
        "host": req.pretty_host,
        "path": req.path,
        "url": req.pretty_url,
        "request_headers": headers_to_dict(req.headers),
        "request_body": body,
        "request_body_encoding": encoding,
        "request_body_size": body_size,
        "request_body_skipped": skipped,
    }


def response(flow: http.HTTPFlow):
    payload = build_base(flow)
    payload.update(
        {
            "status": flow.response.status_code,
            "response_headers": headers_to_dict(flow.response.headers),
            "duration_ms": round(max(0, (time.time() - (flow.timestamp_start or time.time())) * 1000), 2),
            "error": "",
        }
    )
    submit(payload)


def error(flow: http.HTTPFlow):
    payload = build_base(flow)
    payload.update(
        {
            "status": None,
            "response_headers": {},
            "duration_ms": round(max(0, (time.time() - (flow.timestamp_start or time.time())) * 1000), 2),
            "error": str(flow.error or "Network error"),
        }
    )
    submit(payload)
