import subprocess
import os
import json
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

SCRIPT_PATH = os.path.abspath("./scripts/run_cert_scan_pipeline.sh")
CERTS_JSON_PATH = "./data/certs_dump.json"
UPLOAD_DIR = './uploads'
MAX_CONTENT_LENGTH = 5000 # In KB

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH * 1024

@app.route('/api/upload-json', methods=['POST'])
def upload_file_json():
    if not request.is_json:
        return jsonify({"error": "Expected JSON payload"}), 400

    try:
        data = request.get_json()

        # Validate required field
        uuid = data.get("id")
        if not uuid:
            return jsonify({"error": "Missing 'id' field in JSON"}), 400

        filename = f"{uuid}.json"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Save the JSON content
        with open(filepath, 'w') as f:
            import json
            json.dump(data, f, indent=2)

        return jsonify({"status": "success", "file_saved": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if file part is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = uploaded_file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    uploaded_file.save(filepath)

    return jsonify({"status": "success", "file_saved": filename}), 200


@app.route("/api/certs", methods=["GET"])
def get_certs():
    if not os.path.exists(CERTS_JSON_PATH):
        abort(404, description="certs_dump.json not found")

    try:
        with open(CERTS_JSON_PATH, "r") as f:
            certs_data = json.load(f)
        return jsonify(certs_data)
    except Exception as e:
        abort(500, description=f"Failed to read certs_dump.json: {str(e)}")


@app.route("/api/run-scan", methods=["POST"])
def run_scan():
    data = request.get_json()

    if not data or "subnet" not in data or "ports" not in data:
        return jsonify({"error": "Missing required fields: 'subnet' and 'ports'"}), 400

    subnet = data["subnet"]
    ports = data["ports"]
    output = data.get("output", "targets.txt")

    # Basic validation
    if not isinstance(subnet, str) or not isinstance(ports, str):
        return jsonify({"error": "Invalid input format. 'subnet' and 'ports' must be strings."}), 400

    try:
        result = subprocess.run(
            ["bash", SCRIPT_PATH, subnet, "-p", ports, "-o", output],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({
            "status": "success",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stdout,
            "error": e.stderr
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
