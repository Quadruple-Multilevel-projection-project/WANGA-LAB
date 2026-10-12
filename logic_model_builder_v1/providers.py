"""Proposal providers for the logic-native model builder.

The structured provider is an offline baseline. The optional LLM provider proposes
LNL code and never bypasses the parser/critic.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Mapping, Protocol


class ProposalProvider(Protocol):
    name: str

    def propose(self, specification: Mapping[str, Any], critique: list[dict[str, Any]], attempt: int) -> str:
        ...


class StructuredSpecProvider:
    """Deterministically turn a structured model specification into LNL."""
    name = "structured-spec-baseline"

    def propose(self, specification: Mapping[str, Any], critique: list[dict[str, Any]], attempt: int) -> str:
        lines = [
            f"model {specification.get('model_name', 'wanga_model')} "
            f"version={specification.get('version', '0.1')}"
        ]
        if specification.get("description"):
            lines[0] += " description=" + json.dumps(str(specification["description"]), ensure_ascii=False)

        for source in specification.get("sources", []):
            opts = [
                "uri=" + json.dumps(str(source["uri"]), ensure_ascii=False),
                "status=" + str(source.get("status", "UNREVIEWED")).upper(),
            ]
            for key in ("version", "location", "note"):
                if source.get(key):
                    opts.append(key + "=" + json.dumps(str(source[key]), ensure_ascii=False))
            lines.append(f"source {source['id']} " + " ".join(opts))

        for fact in specification.get("facts", []):
            refs = ",".join(fact.get("evidence_refs", []))
            lines.append(
                f"fact {fact['id']} {fact['atom']} "
                f"status={str(fact.get('epistemic_status', 'UNKNOWN')).upper()} evidence={refs}"
            )

        for rule in specification.get("rules", []):
            opts = []
            if rule.get("source_ids"):
                opts.append("source=" + ",".join(rule["source_ids"]))
            if rule.get("assumption", False):
                opts.append("assumption=true")
            header = f"rule {rule['id']}"
            if opts:
                header += " " + " ".join(opts)
            lines.append(header + ":")
            lhs = " AND ".join(str(atom) for atom in rule["antecedents"])
            lines.append(f"  {lhs} => {rule['consequent']}")

        for goal in specification.get("goals", []):
            lines.append("goal " + str(goal))
        constraints = specification.get("constraints", [
            "require_evidence",
            "no_unbound_rule_vars",
            "no_automatic_verified_status",
            "require_rule_sources_or_explicit_assumption",
        ])
        for constraint in constraints:
            lines.append("constraint " + str(constraint))
        return "\n".join(lines) + "\n"


class OpenAICompatibleProvider:
    """Optional LLM adapter; calls a model only when explicitly selected.

    Required: WANGA_MODEL_BASE_URL (e.g. http://localhost:11434/v1),
    WANGA_MODEL_NAME. WANGA_MODEL_API_KEY is optional for local endpoints.
    """
    name = "openai-compatible-llm"

    def __init__(self, base_url: str | None = None, model: str | None = None,
                 api_key: str | None = None, timeout: int = 45):
        self.base_url = (base_url or os.environ.get("WANGA_MODEL_BASE_URL", "")).rstrip("/")
        self.model = model or os.environ.get("WANGA_MODEL_NAME", "")
        self.api_key = api_key or os.environ.get("WANGA_MODEL_API_KEY", "")
        self.timeout = timeout
        if not self.base_url or not self.model:
            raise ValueError("Configure WANGA_MODEL_BASE_URL and WANGA_MODEL_NAME before selecting --provider llm.")

    def propose(self, specification: Mapping[str, Any], critique: list[dict[str, Any]], attempt: int) -> str:
        prompt = {
            "task": "Return only one WANGA Logic-Native Language (LNL/0.1) program. Do not return markdown or explanations.",
            "specification": specification,
            "critique_from_previous_attempt": critique,
            "attempt": attempt,
            "required_constraints": [
                "require_evidence", "no_unbound_rule_vars",
                "no_automatic_verified_status", "require_rule_sources_or_explicit_assumption"
            ],
            "rules": [
                "Do not invent source URIs or evidence content.",
                "Never label a raw fact VERIFIED.",
                "Mark unsourced modeling rules with assumption=true.",
                "Do not assign semantic meaning to a letter gate without explicit source-backed input.",
                "All rule variables in conclusions must occur in antecedents."
            ],
            "grammar_example": (
                'model site_change version=0.1\n'
                'source E1 uri="fixture://request" status=TEST_FIXTURE\n'
                'fact C1 request.action(typo_fix) status=TEST_FIXTURE evidence=E1\n'
                'rule R1 assumption=true:\n'
                '  request.action($action) => action.candidate($action)\n'
                'goal action.candidate(typo_fix)\n'
                'constraint require_evidence\n'
                'constraint no_unbound_rule_vars\n'
                'constraint no_automatic_verified_status\n'
                'constraint require_rule_sources_or_explicit_assumption'
            ),
        }
        payload = json.dumps({
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "Propose a candidate formal logic model; an external deterministic compiler and critic will reject invalid output."},
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
        }).encode("utf-8")
        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                **({"Authorization": "Bearer " + self.api_key} if self.api_key else {}),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise RuntimeError(f"Configured model endpoint returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"Cannot reach configured model endpoint: {exc}") from exc
        try:
            text = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Response must include choices[0].message.content") from exc
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Model returned empty LNL output")
        text = text.strip()
        if text.startswith("~~~") or text.startswith("```"):
            parts = text.split("\n", 1)
            if len(parts) == 2:
                text = parts[1]
            if text.endswith("```") or text.endswith("~~~"):
                text = text[:-3].strip()
        return text
