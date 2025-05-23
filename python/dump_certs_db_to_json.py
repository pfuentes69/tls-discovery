#!/usr/bin/env python3

import sqlite3
import json

def dump_certificates_to_json(db_name="./data/certs.db", output_file="./data/certs_dump.json"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()

    if not rows:
        print("No certificates found in the database.")
        return

    # Get column names
    col_names = [description[0] for description in cursor.description]

    # Build list of dicts
    certs = [dict(zip(col_names, row)) for row in rows]

    # Write to JSON file
    with open(output_file, "w") as f:
        json.dump(certs, f, indent=2)

    print(f"[+] Exported {len(certs)} certificates to {output_file}")
    conn.close()

if __name__ == "__main__":
    dump_certificates_to_json()
