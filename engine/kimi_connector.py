"""Moonshot/Kimi adapter. It accepts only a proxy-issued SanitizedRequest."""
from __future__ import annotations
import os
from .sanitization_proxy import SanitizedRequest, is_proxy_issued, SecurityViolation, SECURITY_VIOLATION

BASE_URL = "https://api.moonshot.ai/v1"
MODEL = "kimi-k3"

class KimiConnector:
    def __init__(self, *, api_key: str | None = None, client=None):
        self._api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        self._client = client

    def complete(self, request: SanitizedRequest, *, permissions: set[str]) -> str:
        if "LLM_EXTERNAL_API" not in permissions:
            raise PermissionError("LLM_EXTERNAL_API permission required")
        if not is_proxy_issued(request):
            raise SecurityViolation(f"{SECURITY_VIOLATION}: connector requires proxy-issued request")
        if self._client is None:
            if not self._api_key:
                raise RuntimeError("MOONSHOT_API_KEY is not configured")
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise RuntimeError("Install the openai package to use the Moonshot-compatible API") from exc
            self._client = OpenAI(api_key=self._api_key, base_url=BASE_URL)
        response = self._client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": request.prompt}],
        )
        return response.choices[0].message.content or ""
