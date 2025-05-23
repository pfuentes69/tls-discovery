import json
import glob
import os
import base64
from textwrap import wrap

def der_to_pem(der_b64: str) -> str:
    # Convert base64 DER to PEM-formatted certificate
    lines = wrap(der_b64, 64)
    return "-----BEGIN CERTIFICATE-----\n" + "\n".join(lines) + "\n-----END CERTIFICATE-----\n"

def extract_certificates_from_results(path="."):
    result_files = glob.glob(os.path.join(path, "results_*.json"))

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

                        ip = result.get("ip", "unknown")
                        port = result.get("data", {}).get("tls", {}).get("port", "443")
                        safe_ip = ip.replace(":", "_")
                        filename = f"{safe_ip}_{port}.crt.pem"

                        with open(filename, "w") as out:
                            out.write(cert_pem)
                        print(f"    -> Wrote {filename}")
                except Exception as e:
                    print(f"    [!] Error processing {file_path}: {e}")

if __name__ == "__main__":
    extract_certificates_from_results()
