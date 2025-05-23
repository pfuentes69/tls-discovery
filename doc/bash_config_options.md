In Linux, there are several **standard and maintainable** ways to store configuration parameters (like file paths) for use in Bash scripts. Here are the most common and practical ones:

---

## ✅ 1. **Environment File (`.env` or `.conf`)**

Create a file like `tls-discovery.conf` or `config.conf`:

```bash
# tls-discovery.conf
CERTS_PATH="/opt/myapp/data/certs_dump.json"
TARGETS_FILE="targets.txt"
```

In your script, source the file:

```bash
#!/bin/bash

# Load config
source tls-discovery.conf

echo "Using certs from: $CERTS_PATH"
```

> ✅ Simple, human-readable, supports comments, easy to version-control.

---

## ✅ 2. **Use `/etc/myapp.conf` for Global Config**

For system-wide configuration:

```bash
# /etc/myapp.conf
DATA_DIR="/var/lib/myapp"
LOG_FILE="/var/log/myapp/scan.log"
```

In your script:

```bash
#!/bin/bash

source /etc/myapp.conf
```

> ✅ Good for scripts intended to run as services or system tools.

---

## ✅ 3. **Pass Config via Environment Variables**

From the shell:

```bash
export CERTS_PATH="/some/path"
./run_scan.sh
```

Inside `run_scan.sh`:

```bash
echo "CERTS path is $CERTS_PATH"
```

> ✅ Useful for temporary overrides or in Docker/CI environments.

---

## ✅ 4. **Command-Line Arguments (Optional Override)**

Support defaults in config, but override via CLI:

```bash
source tls-discovery.conf

CERTS_FILE=${1:-$CERTS_PATH}
```

---

## 🛠 Best Practice: Combine

Use a config file with fallback to environment variables and CLI:

```bash
#!/bin/bash
source ./tls-discovery.conf

CERTS_PATH="${CERTS_PATH:-/default/path/to/certs.json}"
```

---

Would you like a template for a real-world config + script setup?
    