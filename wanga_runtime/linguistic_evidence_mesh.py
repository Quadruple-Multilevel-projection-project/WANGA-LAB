from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
import os
from typing import Any, Dict, Iterable, Protocol
from urllib.parse import quote
from urllib.request import Request, urlopen


EVIDENCE_STATUS = {
    "BUILT", "SPECIFIED", "PROTOTYPED", "TESTED",
    "VERIFIED", "PLANNED", "HYPOTHETICAL",
}


@dataclass(frozen=True)
class SourceRecord:
    provider: str
    source_ref: str
    access_method: str
    retrieved_at: str = ""
    rights_note: str = ""
    payload_digest: str = ""


@dataclass(frozen=True)
class DerivationEdge:
    source: str
    target: str
    relation: str
    method: str
    evidence_status: str
    source_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class LogicRelation:
    source: str
    target: str
    relation: str
    direction: str
    evidence_status: str
    source_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class LexicalEvidence:
    record_id: str
    term: str
    language: str
    lemma: str = ""
    surface_forms: tuple[str, ...] = ()
    part_of_speech: str = ""
    senses: tuple[Dict[str, Any], ...] = ()
    derivations: tuple[DerivationEdge, ...] = ()
    relations: tuple[LogicRelation, ...] = ()
    logical_roles: tuple[str, ...] = ()
    sources: tuple[SourceRecord, ...] = ()
    extraction_method: str = ""
    evidence_status: str = "SPECIFIED"
    record_sha256: str = ""

    def with_digest(self) -> "LexicalEvidence":
        payload = asdict(self)
        payload.pop("record_sha256", None)
        digest = sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return LexicalEvidence(**{**payload, "derivations": tuple(self.derivations),
                                  "relations": tuple(self.relations),
                                  "sources": tuple(self.sources),
                                  "record_sha256": digest})


class SourceAdapter(Protocol):
    provider: str

    def search(self, query: str, language: str = "he") -> list[SourceRecord]:
        ...

    def fetch(self, source_ref: str) -> Dict[str, Any]:
        ...


class HttpJson:
    @staticmethod
    def get(url: str, headers: Dict[str, str] | None = None) -> Dict[str, Any]:
        request = Request(url, headers=headers or {"User-Agent": "WANGA-LAB-RationalLogic/0.1"})
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))


class SefariaAdapter:
    provider = "SEFARIA"

    def search(self, query: str, language: str = "he") -> list[SourceRecord]:
        # Sefaria exposes structured text/search endpoints without requiring an API key.
        url = f"https://www.sefaria.org/api/search-wrapper?query={quote(query)}"
        data = HttpJson.get(url)
        hits = data.get("hits", {}).get("hits", [])
        return [
            SourceRecord(self.provider, str(hit.get("_id", "")), "SEFARIA_SEARCH")
            for hit in hits if hit.get("_id")
        ]

    def fetch(self, source_ref: str) -> Dict[str, Any]:
        url = f"https://www.sefaria.org/api/v3/texts/{quote(source_ref, safe='')}"
        return HttpJson.get(url)


class MediaWikiAdapter:
    provider = "MEDIAWIKI"

    def __init__(self, api_url: str = "https://he.wiktionary.org/w/api.php"):
        self.api_url = api_url

    def search(self, query: str, language: str = "he") -> list[SourceRecord]:
        params = (
            f"?action=query&list=search&srsearch={quote(query)}"
            "&format=json&utf8=1"
        )
        data = HttpJson.get(self.api_url + params)
        results = data.get("query", {}).get("search", [])
        return [
            SourceRecord(self.provider, item.get("title", ""), "MEDIAWIKI_SEARCH")
            for item in results if item.get("title")
        ]

    def fetch(self, source_ref: str) -> Dict[str, Any]:
        params = (
            f"?action=query&prop=revisions&rvprop=content&rvslots=main"
            f"&titles={quote(source_ref)}&format=json"
        )
        return HttpJson.get(self.api_url + params)


class OpenLibraryAdapter:
    provider = "OPEN_LIBRARY"

    def search(self, query: str, language: str = "he") -> list[SourceRecord]:
        url = f"https://openlibrary.org/search.json?q={quote(query)}&lang={quote(language)}"
        data = HttpJson.get(url)
        return [
            SourceRecord(self.provider, doc.get("key", ""), "OPENLIBRARY_SEARCH")
            for doc in data.get("docs", []) if doc.get("key")
        ]

    def fetch(self, source_ref: str) -> Dict[str, Any]:
        if source_ref.endswith(".json"):
            url = f"https://openlibrary.org{source_ref}"
        else:
            url = f"https://openlibrary.org{source_ref}.json"
        return HttpJson.get(url)


class NationalLibraryIsraelAdapter:
    provider = "NLI"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("NLI_API_KEY", "")

    def search(self, query: str, language: str = "he") -> list[SourceRecord]:
        if not self.api_key:
            raise RuntimeError("NLI_API_KEY is required for authenticated NLI Search API access.")
        url = (
            "https://api.nli.org.il/openlibrary/search"
            f"?api_key={quote(self.api_key)}&query=title,contains,{quote(query)},AND"
        )
        data = HttpJson.get(url)
        items = data.get("items", data.get("docs", []))
        return [
            SourceRecord(self.provider, str(item.get("recordId", item.get("identifier", ""))), "NLI_SEARCH")
            for item in items if item.get("recordId") or item.get("identifier")
        ]

    def fetch(self, source_ref: str) -> Dict[str, Any]:
        url = f"https://iiif.nli.org.il/IIIFv21/DOCID/{quote(source_ref)}/manifest"
        return HttpJson.get(url)


class SpecialistAgent(Protocol):
    role: str

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...


@dataclass(frozen=True)
class LexicographerAgent:
    role: str = "LEXICOGRAPHER"

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "role": self.role,
            "source": asdict(source),
            "operation": "TERM_AND_DEFINITION_EXTRACTION",
            "status": "SPECIFIED",
        }


@dataclass(frozen=True)
class MorphologistAgent:
    role: str = "MORPHOLOGIST"

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "role": self.role,
            "source": asdict(source),
            "operation": "LEMMA_VARIANT_DERIVATION_EXTRACTION",
            "status": "SPECIFIED",
        }


@dataclass(frozen=True)
class SemanticistAgent:
    role: str = "SEMANTICIST"

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "role": self.role,
            "source": asdict(source),
            "operation": "SENSE_AND_SEMANTIC_RELATION_EXTRACTION",
            "status": "SPECIFIED",
        }


@dataclass(frozen=True)
class LogicPhilologistAgent:
    role: str = "LOGIC_PHILOLOGIST"

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "role": self.role,
            "source": asdict(source),
            "operation": "LOGICAL_ROLE_AND_RELATION_EXTRACTION",
            "status": "SPECIFIED",
        }


@dataclass(frozen=True)
class EvidenceAuditorAgent:
    role: str = "EVIDENCE_AUDITOR"

    def analyze(self, source: SourceRecord, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload_digest = sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return {
            "role": self.role,
            "source": asdict(source),
            "operation": "PROVENANCE_AND_INTEGRITY_CHECK",
            "payload_sha256": payload_digest,
            "status": "PROTOTYPED",
        }


@dataclass
class LinguisticEvidenceMesh:
    adapters: tuple[SourceAdapter, ...]
    agents: tuple[SpecialistAgent, ...] = field(default_factory=lambda: (
        LexicographerAgent(),
        MorphologistAgent(),
        SemanticistAgent(),
        LogicPhilologistAgent(),
        EvidenceAuditorAgent(),
    ))

    def discover(self, query: str, language: str = "he") -> list[SourceRecord]:
        records: list[SourceRecord] = []
        for adapter in self.adapters:
            records.extend(adapter.search(query, language))
        return records

    def inspect(self, source: SourceRecord) -> list[Dict[str, Any]]:
        adapter = next(a for a in self.adapters if a.provider == source.provider)
        payload = adapter.fetch(source.source_ref)
        return [agent.analyze(source, payload) for agent in self.agents]
