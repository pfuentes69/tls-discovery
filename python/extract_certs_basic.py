import json

with open("results.json", "r") as f:
    for line in f:
        result = json.loads(line)
        cert = result.get("data", {}).get("tls", {}).get("result", {}) \
                    .get("handshake_log", {}).get("server_certificates", {}) \
                    .get("certificate", "")
        if cert:
            ip = result.get("ip")
            with open(f"{ip}.crt.pem", "w") as out:
                out.write(cert)
