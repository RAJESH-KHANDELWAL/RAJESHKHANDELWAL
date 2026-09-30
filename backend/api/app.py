from __future__ import annotations

from urllib.parse import quote

import requests

from flask import (
    Flask,
    jsonify,
    request,
    Response,
)


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# SUPREME CENTRAL API
# ============================================================

SUPREME_API_URL = (
    "https://supremesetuhub-3v4e.onrender.com"
)


# ============================================================
# SUPREME CENTRAL FRONTEND
# ============================================================
# No HTML/CSS duplication.
#
# The frontend is served from:
#
# SUPREMESETUHUB
#     ↓
# frontend/supreme/index.html
#
# RAJESHKHANDELWAL receives it live.
# ============================================================

SUPREME_FRONTEND_URL = (
    SUPREME_API_URL
    + "/api/v1/frontend/supreme"
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
# Live frontend comes directly from SUPREMESETUHUB.
# No local index.html is used.
# ============================================================

@app.get("/")
def root():

    try:

        response = requests.get(
            SUPREME_FRONTEND_URL,
            timeout=20,
        )

        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get(
                "Content-Type",
                "text/html; charset=utf-8",
            ),
        )

    except requests.RequestException as exc:

        return jsonify({
            "error": "SUPREME frontend unavailable",
            "message": str(exc),
            "supreme_frontend": (
                SUPREME_FRONTEND_URL
            ),
        }), 502


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return jsonify({

        "service": "RAJESHKHANDELWAL",

        "status": "healthy",

        "frontend_source": (
            SUPREME_FRONTEND_URL
        ),

        "architecture": (
            "SUPREME CENTRAL FRONTEND"
        ),

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
            timeout=15,
        )

        try:

            payload = response.json()

        except ValueError:

            payload = {
                "error": (
                    "SUPREME returned "
                    "a non-JSON response"
                ),
                "status_code": (
                    response.status_code
                ),
                "text": response.text[:1000],
            }

        return (
            response.status_code,
            payload,
        )

    except requests.RequestException as exc:

        return (
            500,
            {
                "error": str(exc),
                "upstream": SUPREME_API_URL,
            },
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

        "upstream": payload,

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

        "profile": payload,

    }), status_code


# ============================================================
# SUPREME SEARCH
# ============================================================

@app.get("/supreme/bridge/search")
def bridge_search():

    query = request.args.get(
        "q",
        "",
    ).strip()

    if not query:

        return jsonify({
            "error": "Missing q parameter",
        }), 400

    encoded_query = quote(
        query,
        safe="",
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

        "results": payload,

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
            "does not exist"
        ),

    }), 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def server_error(error):

    return jsonify({

        "error": "Server error",

        "message": (
            "Internal server error"
        ),

    }), 500


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":

    import os

    port = int(
        os.getenv(
            "PORT",
            "10000",
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )
