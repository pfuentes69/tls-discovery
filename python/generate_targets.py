#!/usr/bin/env python3

import subprocess
import argparse
import tempfile
import os

def scan_subnet(subnet, ports):
    print(f"[+] Starting scan on subnet {subnet} for ports {ports}")
    ip_port_pairs = set()

    for port in ports:
        print(f"[+] Scanning port {port}...")
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as tmpfile:
            tmp_path = tmpfile.name

        try:
            subprocess.run(
                ['zmap', '-p', str(port), subnet, '-o', tmp_path, f'--blocklist-file=blocklist.conf'],
                check=True
            )

            with open(tmp_path, 'r') as f:
                for line in f:
                    ip = line.strip()
                    ip_port_pairs.add(f"{ip}:{port}")

        finally:
            os.remove(tmp_path)

    return sorted(ip_port_pairs)

def save_target_list(pairs, output_file):
    with open(output_file, 'w') as f:
        for pair in pairs:
            f.write(f"{pair}\n")
    print(f"[+] Saved {len(pairs)} IP:port targets to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate IP:port TLS targets using ZMap")
    parser.add_argument("subnet", help="Target subnet (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", required=True, help="Comma-separated list of ports (e.g., 443,465,993)")
    parser.add_argument("-o", "--output", default="targets.txt", help="Output file for discovered targets")

    args = parser.parse_args()
    ports = [int(p.strip()) for p in args.ports.split(',')]

    targets = scan_subnet(args.subnet, ports)
    save_target_list(targets, args.output)

if __name__ == "__main__":
    main()
