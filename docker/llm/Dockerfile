FROM ollama/ollama:latest

ARG OLLAMA_MODEL=deepseek-r1:8b

ENV OLLAMA_HOST=0.0.0.0:11434

RUN /bin/sh -c 'set -eu; export OLLAMA_HOST=127.0.0.1:11434; ollama serve >/tmp/ollama.log 2>&1 & pid=$!; i=0; while [ "${i}" -lt 180 ]; do ollama list >/dev/null 2>&1 && break; i=$((i+1)); sleep 1; done; ollama list >/dev/null 2>&1 || (cat /tmp/ollama.log && exit 1); ollama pull "${OLLAMA_MODEL}"; kill "${pid}" 2>/dev/null || true; wait "${pid}" 2>/dev/null || true; mkdir -p /opt/ollama-seed; cp -a /root/.ollama/. /opt/ollama-seed/'

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 11434

ENTRYPOINT ["/entrypoint.sh"]
