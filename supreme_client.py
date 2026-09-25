import os
import json
from urllib import request, error


class PlatformControlClient:
    """Client for the MAIN-BASE-FOUNDATION Supreme admin control API."""

    def __init__(self, api_url=None, token=None):
        self.api_url = (api_url or os.getenv("MAIN_BASE_FOUNDATION_API_URL", "")).rstrip("/")
        self.token = token or os.getenv("SUPREME_CONTROL_TOKEN", "")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, path, method="GET", payload=None):
        if not self.api_url:
            raise RuntimeError("MAIN_BASE_FOUNDATION_API_URL is not configured.")
        if not self.token:
            raise RuntimeError("SUPREME_CONTROL_TOKEN is not configured.")

        url = f"{self.api_url}{path}"
        body = None if payload is None else json.dumps(payload).encode("utf-8")

        req = request.Request(url, data=body, headers=self._headers(), method=method)

        try:
            with request.urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Connection error: {exc.reason}") from exc

    def get_status(self):
        return self._request("/supreme/control/status")

    def send_command(self, command, payload=None):
        return self._request(
            "/supreme/control/command",
            method="POST",
            payload={
                "command": command,
                "payload": payload or {},
                "source": "SUPREME_ADMIN_CLIENT",
            },
        )
