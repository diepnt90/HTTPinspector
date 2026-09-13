# HTTPinspector

mitmproxy capture agent for the Tool Station **HTTP Inspector** UI.

## What it captures

- Full request headers
- Request body when body size is `<= BODY_LIMIT` (default 256 KiB)
- Full response headers
- Response status and request duration
- **No response body**
- Request bodies larger than the configured limit are skipped

Capture events are forwarded to the AllinOne Cloudflare Worker and broadcast to open HTTP Inspector pages in realtime. Inspector traffic is **not stored in Cloudflare KV**. If no dashboard is open, events are discarded by the realtime relay.

HTTP Inspector UI:

```text
https://daulac.nomzom.lol/http-inspector/
```

## First install

```bash
git clone https://github.com/diepnt90/HTTPinspector.git
cd HTTPinspector
bash install.sh
```

The installer creates `config.env`, installs mitmproxy, enables the `httpinspector` systemd service, and starts it automatically.

Default configuration:

```bash
INSPECTOR_ENDPOINT=https://daulac.nomzom.lol
BODY_LIMIT=262144
POST_TIMEOUT=5
LISTEN_HOST=0.0.0.0
LISTEN_PORT=8445
```

Check status:

```bash
sudo systemctl status httpinspector
```

Live service logs:

```bash
journalctl -u httpinspector -f
```

## Proxy client example

The proxy listens on TCP port `8445`.

For a client on the same LAN, use the machine's LAN IP and port `8445`. If TCP `8445` is forwarded to the machine through a router, a configured hostname can also be used.

For HTTPS inspection, the client must trust the mitmproxy CA. Open:

```text
http://mitm.it
```

and install the certificate appropriate for the client platform. Applications using certificate pinning may reject interception even after the mitmproxy CA is trusted.

## Realtime dashboard

Open:

```text
https://daulac.nomzom.lol/http-inspector/
```

- **Record**: start adding incoming live events to the current browser tab
- **Pause**: keep the live connection open but stop adding events to the list
- **Erase**: clear the current browser session immediately
- Search: searches host, URL, request/response headers, request body and errors
- Filters: HTTP method, response status class and body state

The dashboard keeps up to 2,000 captured requests in browser memory for the current page session. Reloading or closing the page clears them. No HTTP Inspector request history is written to KV.

## Updating later

```bash
cd HTTPinspector
git pull
sudo systemctl restart httpinspector
```

No reinstall is normally required unless dependencies or the systemd service definition change.
