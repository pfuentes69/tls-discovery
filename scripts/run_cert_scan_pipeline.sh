#!/bin/bash

set -e  # Exit on error
set -o pipefail

# ======== Usage Check ========
usage() {
  echo "Usage: sudo $0 SUBNET -p PORTS [-o OUTPUT]"
  echo "Example: sudo $0 10.247.0.0/16 -p 443,465,993 -o targets.txt"
  exit 1
}

# ======== Parse Arguments ========
if [[ "$EUID" -ne 0 ]]; then
  echo "[-] This script must be run as root."
  exit 1
fi

if [[ $# -lt 3 ]]; then
  usage
fi

SUBNET=""
PORTS=""
OUTPUT="./data/targets.txt"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--ports)
      PORTS="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT="$2"
      shift 2
      ;;
    -*)
      echo "Unknown option: $1"
      usage
      ;;
    *)
      if [[ -z "$SUBNET" ]]; then
        SUBNET="$1"
        shift
      else
        echo "Unknown positional argument: $1"
        usage
      fi
      ;;
  esac
done

if [[ -z "$SUBNET" || -z "$PORTS" ]]; then
  echo "[-] Missing required arguments: subnet or ports"
  usage
fi

# ======== Step 1: Generate Targets ========
echo "[*] Step 1: Generating targets..."
if ! python3 ./python/generate_targets.py "$SUBNET" -p "$PORTS" -o "$OUTPUT"; then
  echo "[-] Failed to generate targets."
  exit 1
fi
echo "[+] Targets generated successfully into $OUTPUT"

# ======== Cleanup: Remove Previous Results ========
echo "[*] Cleaning up old result files..."
rm -f ./data/results_*.json
echo "[+] Old result files deleted."

# ======== Step 2: Run Zgrab2 Scan ========
echo "[*] Step 2: Running Zgrab2 scan..."
if [[ ! -f "$OUTPUT" ]]; then
  echo "[-] Target file '$OUTPUT' not found!"
  exit 1
fi

if ! ./scripts/zgrab2_scan.sh; then
  echo "[-] Zgrab2 scan failed."
  exit 1
fi
echo "[+] Zgrab2 scan completed."

# ======== Step 3: Extract Certificates to DB ========
echo "[*] Step 3: Extracting certificates into SQLite DB..."
if ! python3 ./python/extract_certs_db.py; then
  echo "[-] Failed to extract certs into DB."
  exit 1
fi
echo "[+] Certificates extracted to certs.db"

# ======== Step 4: Dump Certificates from DB to JSON ========
echo "[*] Step 4: Dumping certificates to certs_dump.json..."
if ! python3 ./python/dump_certs_db_to_json.py; then
  echo "[-] Failed to dump certs to JSON."
  exit 1
fi
echo "[+] Dump complete: certs_dump.json"

# ======== Step 5: Upload DB to server ========
# echo "[*] Step 5: Upload DB to server..."
# if ! ./scripts/upload_db_gzip.sh; then
#   echo "[-] DB upload failed."
#   exit 1
# fi
# echo "[+] DB upload completed."

echo "[✅] Full scan pipeline completed successfully."
