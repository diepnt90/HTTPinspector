FROM python:3.12-slim

RUN pip install --no-cache-dir mitmproxy

WORKDIR /app
COPY inspector.py /app/inspector.py

ENV INSPECTOR_ENDPOINT=https://daulac.nomzom.lol \
    BODY_LIMIT=262144 \
    POST_TIMEOUT=5 \
    LISTEN_HOST=0.0.0.0 \
    LISTEN_PORT=8445

EXPOSE 8445

CMD ["sh","-c","mitmdump --listen-host ${LISTEN_HOST} --listen-port ${LISTEN_PORT} --set block_global=false -s /app/inspector.py"]
