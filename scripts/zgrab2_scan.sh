#!/bin/bash

# Load config
source ./tls-discovery.conf

# Ensure required values exist
if [ -z "$INPUT_FILE" ]; then
  echo "Missing INPUT_FILE in tls-discovery.conf"
  exit 1
fi

while IFS=: read -r ip port; do
  echo "[*] Scanning $ip on port $port..."

  # Sanitize IP for filename (e.g., replace dots and colons)
  safe_ip=$(echo "$ip" | tr '.:' '__')
  outfile="./data/results_${safe_ip}_${port}.json"

  echo "$ip" | docker run --rm -i ghcr.io/zmap/zgrab2 tls --port $port > "$outfile"
done < "$INPUT_FILE"
