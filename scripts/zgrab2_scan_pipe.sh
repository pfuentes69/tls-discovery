#!/bin/bash

# Load config
source ./tls-discovery.conf

# Ensure required values exist
if [ -z "$INPUT_FILE" ] || [ -z "$FIFO_PIPE" ] || [ -z "$OUT_DIR" ]; then
  echo "Missing INPUT_FILE or FIFO_PIPE or OUT_DIR in tls-discovery.conf"
  exit 1
fi

mkdir -p "$OUT_DIR"
rm -f "$FIFO_PIPE"
mkfifo "$FIFO_PIPE"

# Start the zgrab2 docker container with input from FIFO
docker run --rm -i ghcr.io/zmap/zgrab2 tls --port 443 < "$FIFO_PIPE" > "$OUT_DIR/raw_output.json" &
ZGRAB_PID=$!

# Feed the IPs into the FIFO
while IFS=: read -r ip port; do
  echo "[*] Queuing scan for $ip:$port..."

  # sanitize filename
  safe_ip=$(echo "$ip" | tr '.:' '__')
  outfile="$OUT_DIR/results_${safe_ip}_${port}.json"

  # echo target into FIFO
  echo "$ip"

  # Extract result for the current IP from raw output
  # This assumes one JSON object per line in raw_output.json
  tail -f "$OUT_DIR/raw_output.json" | \
    grep -m 1 "\"ip\": \"$ip\"" > "$outfile" &
done < "$INPUT_FILE"

# Wait for the docker process to finish (if necessary)
wait "$ZGRAB_PID"
rm -f "$FIFO_PIPE"
