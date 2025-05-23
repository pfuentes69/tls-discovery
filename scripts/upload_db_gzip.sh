#!/bin/bash

# Load config
source ./tls-discovery.conf

# Ensure required values exist
if [ -z "$UUID" ] || [ -z "$UPLOAD_URL" ] || [ -z "$DUMP_FILE" ]; then
  echo "Missing UUID or UPLOAD_URL or DUMP_FILE in tls-discovery.conf"
  exit 1
fi

if [ ! -f "$DUMP_FILE" ]; then
  echo "Input file '$DUMP_FILE' not found!"
  exit 1
fi

# Output file name based on UUID
FILENAME="/tmp/${UUID}.json.gz"

# Compress the file
gzip -c "$DUMP_FILE" > "$FILENAME"
echo "[*] Compressed '$DUMP_FILE' to '$FILENAME'"

# Send the compressed file via curl as multipart/form-data
curl -X POST "$UPLOAD_URL" \
     -F "file=@${FILENAME}"

echo -e "\n[*] Upload complete."
