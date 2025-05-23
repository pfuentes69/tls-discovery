## 🚀 How to Use It

### 1. Install ZMap

```bash
sudo apt install zmap  # Debian/Ubuntu
brew install zmap      # macOS
```

### 2. Run the Script to build the list of targets

```bash
chmod +x generate_targets.py
sudo ./generate_targets.py 192.168.2.0/24 -p 443,465,993 -o targets.txt
```

### 3. Output

* A `targets.txt` file with one IP per line, only for hosts with at least one specified port open.

---

## 4. Feed to ZGrab

```bash
./zgrab2_scan.sh
```

### 5. Process the output

```bash
chmod +x extract_certs_json.py
sudo ./extract_certs_json.py
```

