"""
YHack War Room — Minimal Flask server for shared brainstorm state.
Deploy to Render as a Web Service.

Routes:
  GET  /           → serves index.html
  GET  /api/brain  → returns brainstorm.json
  POST /api/brain  → writes brainstorm.json
"""

import json
from pathlib import Path
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)
DATA_DIR = Path(__file__).parent
HTML_FILE = DATA_DIR / "index.html"
BRAIN_FILE = DATA_DIR / "brainstorm.json"

# Initialize brainstorm.json if missing
if not BRAIN_FILE.exists():
    BRAIN_FILE.write_text("{}")


@app.route("/")
def index():
    return send_file(HTML_FILE)


@app.route("/playground/<path:filename>")
def playground(filename):
    playground_dir = DATA_DIR / "playground"
    file_path = playground_dir / filename
    if file_path.exists() and file_path.is_relative_to(playground_dir):
        return send_file(file_path)
    return "Not found", 404


@app.route("/api/brain", methods=["GET"])
def get_brain():
    data = json.loads(BRAIN_FILE.read_text())
    return jsonify(data)


@app.route("/api/brain", methods=["POST"])
def set_brain():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400
    BRAIN_FILE.write_text(json.dumps(data, indent=2))
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
