import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "SUPREME-ADMIN")
PORT = int(os.getenv("PORT", "10000"))
SUPREME_API_URL = os.getenv("SUPREME_API_URL", "http://localhost:10000")
SUPREME_API_KEY = os.getenv("SUPREME_API_KEY", "")
SUPREME_ID = os.getenv("SUPREME_ID", "SUP-9C4M-7X2K-6P8R")
OWNER_PERSON_ID = os.getenv("OWNER_PERSON_ID", "PRS-7K4M-2Q8N-6T1X")

# CORS support
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def call_supreme(endpoint):
    headers = {
        "Authorization": f"Bearer {SUPREME_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{SUPREME_API_URL.rstrip('/')}{endpoint}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        return response.status_code, response.json()
    except Exception as exc:
        return 500, {"error": str(exc)}

@app.get("/")
def root():
    return jsonify({
        "service": APP_NAME,
        "status": "running",
        "supreme_id": SUPREME_ID,
        "owner_person_id": OWNER_PERSON_ID,
        "version": "1.0.0"
    }), 200

@app.get("/health")
def health():
    return jsonify({
        "service": APP_NAME,
        "status": "healthy",
        "supreme_id": SUPREME_ID,
        "owner_person_id": OWNER_PERSON_ID
    }), 200

@app.get("/supreme/bridge/status")
def bridge_status():
    status_code, payload = call_supreme("/supreme/status")
    if status_code != 200:
        return jsonify({
            "service": APP_NAME,
            "status": "bridge_error",
            "supreme_id": SUPREME_ID,
            "owner_person_id": OWNER_PERSON_ID,
            "upstream": payload
        }), status_code

    return jsonify({
        "service": APP_NAME,
        "status": "healthy",
        "supreme_id": SUPREME_ID,
        "owner_person_id": OWNER_PERSON_ID,
        "upstream": payload
    }), 200

@app.get("/supreme/bridge/profile")
def bridge_profile():
    status_code, payload = call_supreme("/supreme/profile")
    if status_code != 200:
        return jsonify({
            "service": APP_NAME,
            "status": "bridge_error",
            "upstream": payload
        }), status_code

    return jsonify({
        "service": APP_NAME,
        "status": "healthy",
        "supreme_id": SUPREME_ID,
        "owner_person_id": OWNER_PERSON_ID,
        "profile": payload
    }), 200

@app.get("/supreme/bridge/search")
def bridge_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "Missing q parameter"}), 400

    status_code, payload = call_supreme(f"/supreme/search?q={q}")
    if status_code != 200:
        return jsonify({
            "service": APP_NAME,
            "status": "bridge_error",
            "upstream": payload
        }), status_code

    return jsonify({
        "service": APP_NAME,
        "status": "healthy",
        "supreme_id": SUPREME_ID,
        "owner_person_id": OWNER_PERSON_ID,
        "results": payload
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Server error",
        "message": "Internal server error"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
