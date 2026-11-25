"""Minimal ClearTrack API client. Standard library only (Python 3.8+).

Docs: https://api.cleartrackpromise.in/docs
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.cleartrackpromise.in/v1"


class ClearTrackError(Exception):
    def __init__(self, status, code, message, retry_after=None):
        super().__init__(f"{status} {code}: {message}")
        self.status = status
        self.code = code
        self.message = message
        self.retry_after = retry_after


class ClearTrack:
    def __init__(self, api_key=None, base_url=None, max_retries=2, timeout=30):
        self.api_key = api_key or os.environ.get("CLEARTRACK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Set CLEARTRACK_API_KEY (get a trial key at https://api.cleartrackpromise.in/trial)"
            )
        self.base_url = (base_url or os.environ.get("CLEARTRACK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout

    def track(self, carrier, awb):
        """Normalised tracking for one shipment. carrier: e.g. "indiapost", "bluedart", "delhivery"."""
        q = urllib.parse.quote
        return self._get(f"/track/{q(carrier, safe='')}/{q(awb, safe='')}")

    def usage(self):
        """Plan, period and daily quota for this API key."""
        return self._get("/usage")

    def _get(self, path):
        attempt = 0
        while True:
            req = urllib.request.Request(
                self.base_url + path,
                headers={"X-API-Key": self.api_key, "Accept": "application/json"},
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as res:
                    return json.load(res)
            except urllib.error.HTTPError as e:
                try:
                    err = json.load(e).get("error", {})
                except ValueError:
                    err = {}
                code = err.get("code", "unknown_error")
                retry_after = e.headers.get("Retry-After")
                retry_after = int(retry_after) if retry_after and retry_after.isdigit() else None
                # Retry only the short per-second burst limit. Period / daily quota errors
                # won't clear by waiting a few seconds.
                if e.code == 429 and code == "rate_limit_exceeded" and attempt < self.max_retries:
                    attempt += 1
                    time.sleep(retry_after or 1)
                    continue
                raise ClearTrackError(e.code, code, err.get("message", e.reason), retry_after) from None
