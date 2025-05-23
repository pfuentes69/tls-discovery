#!/usr/bin/env python3

import sqlite3
import json
import os

def dump_new_certificates(
    db_name="./data/certs.db",
    output_file="./data/certs_diff.json",
    snapshot_file="./data/last_fingerprints.json"
):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Load previous fingerprints
    if os.path.exists(snapshot_file):
        with open(snapshot_file, "r") as f:
            known_fingerprints = set(json.load(f))
    else:
        known_fingerprints = set()

    # Fetch all certs from DB
    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()

    if not rows:
        print("No certificates found in the database.")
        return

    # Get column names
    col_names = [desc[0] for desc in cursor.description]

    new_certs = []
    new_fingerprints = set()

    for row in rows:
        cert = dict(zip(col_names, row))
        fingerprint = cert.get("fingerprint_sha256")
        if fingerprint and fingerprint not in known_fingerprints:
            new_certs.append(cert)
            new_fingerprints.add(fingerprint)

    if not new_certs:
        print("No new certificates found.")
        return

    # Export new certs
    with open(output_file, "w") as f:
        json.dump(new_certs, f, indent=2)

    print(f"[+] Exported {len(new_certs)} new certificates to {output_file}")

    # Update snapshot
    all_fingerprints = list(known_fingerprints.union(new_fingerprints))
    with open(snapshot_file, "w") as f:
        json.dump(all_fingerprints, f, indent=2)

    conn.close()

if __name__ == "__main__":
    dump_new_certificates()
