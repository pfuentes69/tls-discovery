#!/bin/bash

# Load config
source ./tls-discovery.conf

# Ensure required values exist
if [ -z "$UUID" ] || [ -z "$UPLOAD_URL" ]; then
  echo "Missing UUID or UPLOAD_URL in tls-discovery.conf"
  exit 1
fi

# Create a sample JSON file named after the UUID
FILENAME="${UUID}.json"
echo "{\"id\": \"$UUID\", \"data\": \"example payload\"}" > "$FILENAME"

echo "[*] Created file: $FILENAME"

# Send via curl
curl -X POST "$UPLOAD_URL-json" \
     -H "Content-Type: application/json" \
     --data-binary "@${FILENAME}"

echo -e "\n[*] Upload complete."
