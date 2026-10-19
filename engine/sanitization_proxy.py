"""Strict outbound boundary for external-model requests.

This is an application-layer guard, not a physical air gap. Deploy the connector
in a separate process/container with network egress limited to the provider.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Final

SECURITY_VIOLATION = "SECURITY_VIOLATION"
_INTERNAL_MARKERS: Final[tuple[str, ...]] = (
    "golem", "f1-f7", "dvl", "agent_architect", "data_triangulator",
    "kimi_calc_01", "neo4j_query", "python_exec", "llm_external_api",
    "weight_slot", "processor_id", "internal agent", "internal network",
    "sanitization_proxy", "plugin_registry", "126d", "126-dimensional",
)
_PUBLIC_TASK_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?is)^write a python function that [\w\s,().:'-]{5,500}$"),
    re.compile(r"(?is)^calculate [\w\s,().:+*/=-]{3,300}$"),
    re.compile(r"(?is)^explain [\w\s,().:'-]{5,500}$"),
)

class SecurityViolation(ValueError):
    """Raised when a request cannot be proven safe for external disclosure."""

@dataclass(frozen=True, slots=True)
class SanitizedRequest:
    prompt: str
    sphere: str
    _seal: object

class SanitizationProxy:
    """Fail-closed proxy: accepts only a narrow, public-task language."""

    _seal = object()

    def sanitize(self, raw_request: str, *, sphere: str) -> SanitizedRequest:
        if not isinstance(raw_request, str) or not raw_request.strip():
            raise SecurityViolation(f"{SECURITY_VIOLATION}: empty or invalid request")
        if sphere not in {
            "Sphere_PHYSICAL", "Sphere_PLACE", "Sphere_THOUGHT",
            "Sphere_ADVICE", "Sphere_WILL", "Sphere_INTELLECT",
        }:
            raise SecurityViolation(f"{SECURITY_VIOLATION}: unknown sphere")
        text = " ".join(raw_request.split())
        lowered = text.casefold()
        if any(marker in lowered for marker in _INTERNAL_MARKERS):
            raise SecurityViolation(f"{SECURITY_VIOLATION}: internal marker detected")
        if any(ch in text for ch in ("{", "}", "<", ">", "\\", "`")):
            raise SecurityViolation(f"{SECURITY_VIOLATION}: structured or code payload denied")
        if not any(pattern.fullmatch(text) for pattern in _PUBLIC_TASK_PATTERNS):
            raise SecurityViolation(f"{SECURITY_VIOLATION}: request is not in public-task allowlist")
        return SanitizedRequest(prompt=text, sphere=sphere, _seal=self._seal)

def is_proxy_issued(request: object) -> bool:
    return isinstance(request, SanitizedRequest) and request._seal is SanitizationProxy._seal
