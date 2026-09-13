# HTTPinspector

Raspberry Pi mitmproxy capture agent for the Tool Station **HTTP Inspector** UI.

## What it captures

- Full request headers
- Request body when body size is `<= BODY_LIMIT` (default 256 KiB)
- Full response headers
- Response status and request duration
- **No response body**
- Request bodies larger than the configured limit are skipped

The Raspberry Pi is the actual HTTP/HTTPS proxy. Capture events are forwarded to the AllinOne Cloudflare Worker and broadcast to open HTTP Inspector pages in realtime. Inspector traffic is **not stored in Cloudflare KV**. If no dashboard is open, events are simply discarded by the realtime relay.

## First install on Raspberry Pi

```bash
git clone https://github.com/diepnt90/HTTPinspector.git
cd HTTPinspector
bash install.sh
```

Edit the generated configuration:

```bash
nano config.env
```

Set the deployed Tool Station base URL:

```bash
INSPECTOR_ENDPOINT=https://your-allinone-domain.example
BODY_LIMIT=262144
POST_TIMEOUT=5
LISTEN_HOST=0.0.0.0
LISTEN_PORT=8445
```

Then start the service:

```bash
sudo systemctl restart httpinspector
sudo systemctl status httpinspector
```

Live service logs:

```bash
journalctl -u httpinspector -f
```

## iPhone proxy setup

The proxy listens on TCP port `8445`.

If the iPhone is on the same LAN, use the Raspberry Pi LAN IP. If your router forwards TCP `8445` to the Pi and your network supports the route you want to use, you can use your DDNS hostname such as:

```text
daulac.duckdns.org
```

On iPhone:

1. Settings → Wi-Fi → current network
2. Configure Proxy → Manual
3. Server: Raspberry Pi LAN IP or `daulac.duckdns.org`
4. Port: `8445`
5. Authentication: Off

With the proxy enabled, open on the iPhone:

```text
http://mitm.it
```

Install the mitmproxy iOS certificate, then enable full trust under:

```text
Settings → General → About → Certificate Trust Settings
```

Apps using certificate pinning may reject interception even after the mitmproxy CA is trusted.

## Realtime dashboard

Open Tool Station → **HTTP Inspector**.

- **Record**: start adding incoming live events to this browser tab
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
