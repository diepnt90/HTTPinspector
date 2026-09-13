# HTTPinspector

Raspberry Pi mitmproxy capture agent for the Tool Station **HTTP Inspector** UI.

## What it captures

- Full request headers
- Request body when body size is `<= BODY_LIMIT` (default 256 KiB)
- Full response headers
- Response status and request duration
- **No response body**
- Request bodies larger than the configured limit are skipped

The Pi remains the actual HTTP/HTTPS proxy. Captured records are posted to the AllinOne Cloudflare Worker and shown at `/http-inspector`.

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

Set the deployed Tool Station base URL, for example:

```bash
INSPECTOR_ENDPOINT=https://tools.example.com
BODY_LIMIT=262144
POST_TIMEOUT=5
LISTEN_HOST=0.0.0.0
LISTEN_PORT=8080
```

Then start the service:

```bash
sudo systemctl restart httpinspector
sudo systemctl status httpinspector
```

Live logs:

```bash
journalctl -u httpinspector -f
```

## iPhone proxy setup

Find the Raspberry Pi LAN address:

```bash
hostname -I
```

On iPhone:

1. Settings → Wi-Fi → current network
2. Configure Proxy → Manual
3. Server: Raspberry Pi LAN IP
4. Port: `8080`
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

## Dashboard controls

Open Tool Station → **HTTP Inspector**.

- **Record**: Worker starts storing incoming capture records
- **Pause**: traffic still passes through the Pi, but new records are not stored
- **Erase**: deletes HTTP Inspector records from Cloudflare KV
- Search: searches host, URL, request/response headers, request body and errors
- Filters: HTTP method, response status class and body state

The recording state defaults to paused until Record is enabled in the UI.

## Updating later

```bash
cd HTTPinspector
git pull
sudo systemctl restart httpinspector
```

No reinstall is normally required unless dependencies or the service definition change.
