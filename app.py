import os

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "SUPREME-ADMIN",
    })


@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()

    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    return jsonify({
        "text": "AI generation is delegated to the MAIN-BASE-FOUNDATION platform.",
        "prompt": prompt,
        "status": "delegated",
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
