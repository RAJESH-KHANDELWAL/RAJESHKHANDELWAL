from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

import requests

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
)


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# FRONTEND
# ============================================================
# Actual RAJESHKHANDELWAL Home Page:
#
# frontend/
# └── supreme/
#     └── index.html
#
# All frontend assets such as CSS, JS, images, etc.
# should also be available inside frontend/supreme/
# ============================================================

FRONTEND_DIR = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "supreme"
)


# ============================================================
# SUPREME CENTRAL API
# ============================================================

SUPREME_API_URL = (
    "https://supremesetuhub-3v4e.onrender.com"
)


# ============================================================
# CORS
# ============================================================

@app.after_request
def after_request(response):

    response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type,Authorization"
    )

    response.headers["Access-Control-Allow-Methods"] = (
        "GET,PUT,POST,DELETE,OPTIONS"
    )

    return response


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def root():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# FRONTEND STATIC FILES
# ============================================================
# Examples:
#
# /style.css
# /script.js
# /images/logo.png
#
# These files are served from:
#
# frontend/supreme/
# ============================================================

@app.get("/<path:filename>")
def frontend_files(filename):

    requested_file = FRONTEND_DIR / filename

    if requested_file.is_file():

        return send_from_directory(
            FRONTEND_DIR,
            filename
        )

    return jsonify({
        "error": "Not found",
        "message": (
            "The requested endpoint "
            "or frontend file does not exist"
        )
    }), 404


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return jsonify({
        "service": "RAJESHKHANDELWAL",
        "status": "healthy",
        "frontend": "frontend/supreme/index.html",
        "supreme_api": SUPREME_API_URL
    }), 200


# ============================================================
# SUPREME BRIDGE
# ============================================================

def call_supreme(endpoint: str):

    url = (
        SUPREME_API_URL.rstrip("/")
        + endpoint
    )

    try:

        response = requests.get(
            url,
            timeout=15
        )

        try:
            payload = response.json()

        except ValueError:

            payload = {
                "error": (
                    "SUPREME returned "
                    "a non-JSON response"
                ),
                "status_code": response.status_code,
                "text": response.text[:1000]
            }

        return (
            response.status_code,
            payload
        )

    except requests.RequestException as exc:

        return (
            500,
            {
                "error": str(exc),
                "upstream": SUPREME_API_URL
            }
        )


# ============================================================
# SUPREME STATUS
# ============================================================

@app.get("/supreme/bridge/status")
def bridge_status():

    status_code, payload = call_supreme(
        "/supreme/status"
    )

    return jsonify({
        "service": "RAJESHKHANDELWAL",
        "status": (
            "healthy"
            if status_code == 200
            else "bridge_error"
        ),
        "upstream": payload
    }), status_code


# ============================================================
# SUPREME PROFILE
# ============================================================

@app.get("/supreme/bridge/profile")
def bridge_profile():

    status_code, payload = call_supreme(
        "/supreme/profile"
    )

    return jsonify({
        "service": "RAJESHKHANDELWAL",
        "status": (
            "healthy"
            if status_code == 200
            else "bridge_error"
        ),
        "profile": payload
    }), status_code


# ============================================================
# SUPREME SEARCH
# ============================================================

@app.get("/supreme/bridge/search")
def bridge_search():

    query = request.args.get(
        "q",
        ""
    ).strip()

    if not query:

        return jsonify({
            "error": "Missing q parameter"
        }), 400

    encoded_query = quote(
        query,
        safe=""
    )

    status_code, payload = call_supreme(
        "/supreme/search?q="
        + encoded_query
    )

    return jsonify({
        "service": "RAJESHKHANDELWAL",
        "status": (
            "healthy"
            if status_code == 200
            else "bridge_error"
        ),
        "results": payload
    }), status_code


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Not found",
        "message": (
            "The requested endpoint "
            "or resource does not exist"
        )
    }), 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Server error",
        "message": "Internal server error"
    }), 500


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":

    import os

    port = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
