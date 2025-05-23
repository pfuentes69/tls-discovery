#!/usr/bin/env python3

import json
import glob
import os
import base64
import sqlite3
from textwrap import wrap

def der_to_pem(der_b64: str) -> str:
    lines = wrap(der_b64, 64)
    return "-----BEGIN CERTIFICATE-----\n" + "\n".join(lines) + "\n-----END CERTIFICATE-----\n"

def init_db(db_name="certs.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            certificate_pem TEXT,
            fingerprint_sha256 TEXT UNIQUE,
            IssuerName TEXT,
            CommonName TEXT,
            Domain TEXT,
            SubjectDN TEXT,
            IssuanceDate TEXT,
            ExpirationDate TEXT,
            SerialNumber TEXT,
            SslType TEXT
        )
    ''')
    conn.commit()
    return conn

def insert_certificate(conn, cert):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO certificates (
                ip, certificate_pem, fingerprint_sha256,
                IssuerName, CommonName, Domain, SubjectDN, IssuanceDate, ExpirationDate, SerialNumber, 
                SslType
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cert["ip"],
            cert["certificate_pem"],
            cert["fingerprint_sha256"],
            cert["IssuerName"],
            cert["CommonName"],
            cert["CommonName"],
            cert["SubjectDN"],
            cert["IssuanceDate"],
            cert["ExpirationDate"],
            cert["SerialNumber"],
            cert["SslType"]
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Duplicate entry by fingerprint_sha256

def extract_certificates_to_db(path="./data", db_name="./data/certs.db"):
    result_files = glob.glob(os.path.join(path, "results_*.json"))
    if not result_files:
        print("[-] No results_*.json files found.")
        return

    conn = init_db(db_name)

    for file_path in result_files:
        print(f"[+] Processing {file_path}")
        with open(file_path, "r") as f:
            for line in f:
                try:
                    result = json.loads(line)
                    cert = result.get("data", {}).get("tls", {}).get("result", {}) \
                                 .get("handshake_log", {}).get("server_certificates", {}) \
                                 .get("certificate", {})
                    parsed = cert.get("parsed", {})
                    cert_raw_b64 = cert.get("raw")
                    if cert_raw_b64 and parsed.get("fingerprint_sha256"):
                        cert_pem = der_to_pem(cert_raw_b64)

                        serial_decimal = parsed.get("serial_number", "")
                        serial_hex = hex(int(serial_decimal))[2:]
                        if len(serial_hex) % 2 != 0:
                            serial_hex = '0' + serial_hex

                        cert_record = {
                            "ip": result.get("ip", "unknown"),
                            "certificate_pem": cert_pem,
                            "fingerprint_sha256": parsed.get("fingerprint_sha256", ""),
                            "IssuerName": parsed.get("issuer_dn", ""),
                            "CommonName": parsed.get("subject", "").get("common_name", "")[0],
                            "SubjectDN": parsed.get("subject_dn", ""),
                            "IssuanceDate": parsed.get("validity", {}).get("start", ""),
                            "ExpirationDate": parsed.get("validity", {}).get("end", ""),
                            "SerialNumber": serial_hex,
                            "SslType": parsed.get("validation_level", "")
                        }
                        insert_certificate(conn, cert_record)
                except Exception as e:
                    print(f"[-] Error: {e}")
    conn.close()

if __name__ == "__main__":
    extract_certificates_to_db()
