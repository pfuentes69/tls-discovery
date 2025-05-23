#!/usr/bin/env python3

import sqlite3

def dump_certificates(db_name="./data/certs.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()

    if not rows:
        print("No certificates found in the database.")
        return

    # Get column names
    col_names = [description[0] for description in cursor.description]

    for row in rows:
        print("=" * 60)
        for col, val in zip(col_names, row):
            print(f"{col}: {val}")
        print("=" * 60 + "\n")

    conn.close()

if __name__ == "__main__":
    dump_certificates()
