#!/bin/sh
set -e

if [ -d /root/.ollama ] && [ -z "$(ls -A /root/.ollama 2>/dev/null)" ] && [ -d /opt/ollama-seed ]; then
  cp -a /opt/ollama-seed/. /root/.ollama/
fi

exec ollama serve

