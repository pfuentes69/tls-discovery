#!/usr/bin/env python3

import json
import glob
import os
import base64
from datetime import datetime, timezone
from textwrap import wrap

def der_to_pem(der_b64: str) -> str:
    lines = wrap(der_b64, 64)
    return "-----BEGIN CERTIFICATE-----\n" + "\n".join(lines) + "\n-----END CERTIFICATE-----\n"

def extract_certificates_to_json(output_file="", path="."):
    result_files = glob.glob(os.path.join(path, "results_*.json"))
    all_certs = []

    if not result_files:
        print("[-] No results_*.json files found.")
        return

    for file_path in result_files:
        print(f"[+] Processing {file_path}")
        with open(file_path, "r") as f:
            for line in f:
                try:
                    result = json.loads(line)
                    cert_data = result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {})
                    cert_raw_b64 = cert_data.get("raw")
                    if cert_raw_b64:
                        cert_pem = der_to_pem(cert_raw_b64)
                        entry = {
                            "ip": result.get("ip", "unknown"),
#                            "port": result.get("data", {}).get("tls", {}).get("port", 443),
                            "certificate_pem": cert_pem,
                            "serial_number": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("serial_number", {}),
                            "fingerprint_sha256": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("fingerprint_sha256", {}),
                            "issuer_dn": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("issuer_dn", {}),
                            "subject_dn": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("subject_dn", {}),
                            "validity": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("validity", {}),
                            "validation_level": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("certificate", {}).get("parsed", {}).get("validation_level", {}),
                            "validation": result.get("data", {}).get("tls", {}).get("result", {}) \
                                     .get("handshake_log", {}).get("server_certificates", {}) \
                                     .get("validation", {})
                        }
                        all_certs.append(entry)
                except Exception as e:
                    print(f"    [!] Error processing line in {file_path}: {e}")

    # Write to single JSON file
    if output_file == "":
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        output_file = f"scan-{timestamp}.json"
    with open(output_file, "w") as out:
        json.dump(all_certs, out, indent=2)
    print(f"[+] Written all certificates to {output_file}")

if __name__ == "__main__":
    extract_certificates_to_json()
