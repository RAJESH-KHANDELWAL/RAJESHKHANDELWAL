from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# ============================================================
# FRONTEND
# ============================================================

FRONTEND_DIR = (
    Path(__file__).resolve().parents[2] / "frontend"
)


# ============================================================
# CORS
# ============================================================

@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Origin",
        "*"
    )

    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type,Authorization"
    )

    response.headers.add(
        "Access-Control-Allow-Methods",
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
        "message": "The requested endpoint does not exist"
    }), 404


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return jsonify({
        "service": "RAJESHKHANDELWAL",
        "status": "healthy"
    }), 200


# ============================================================
# SUPREME BRIDGE
# ============================================================

SUPREME_API_URL = (
    "https://supremesetuhub-3v4e.onrender.com"
)


def call_supreme(endpoint):

    import requests

    url = (
        SUPREME_API_URL.rstrip("/")
        + endpoint
    )

    try:

        response = requests.get(
            url,
            timeout=15
        )

        return (
            response.status_code,
            response.json()
        )

    except Exception as exc:

        return (
            500,
            {
                "error": str(exc)
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

    status_code, payload = call_supreme(
        "/supreme/search?q="
        + query
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
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Not found",
        "message": (
            "The requested endpoint "
            "does not exist"
        )
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Server error",
        "message": "Internal server error"
    }), 500


# ============================================================
# RUN
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
