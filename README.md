# Certificate Scan Pipeline

## Prerequisites

- Ubuntu-based system
- Root access (for zmap)
- Internet (for Docker + pulling zgrab2)

## Setup

```bash
git clone https://yourrepo/tls-discovery.git
cd tls-discovery
chmod +x setup.sh
./setup.sh
```

## Run the Pipeline

```bash
cd scripts
sudo ./run_cert_scan_pipeline.sh 10.247.0.0/16 -p 443,465,993
```

## Output

- Intermediate results: results_*.json
- Final DB: certs.db
- Final JSON: certs_dump.json