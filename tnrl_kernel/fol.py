from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from .ir import Proposition, TruthStatus

@dataclass
class FOLStore:
    facts: Dict[str, Proposition]

    def __init__(self):
        self.facts = {}

    def assert_fact(self, fact: Proposition) -> None:
        fact.validate()
        key = self._key(fact)
        existing = self.facts.get(key)
        if existing and existing.status != fact.status:
            self.facts[key] = Proposition(fact.predicate, fact.arguments, TruthStatus.CONTRADICTED, existing.provenance + fact.provenance)
        else:
            self.facts[key] = fact

    def entails(self, fact: Proposition) -> bool:
        existing = self.facts.get(self._key(fact))
        return existing is not None and existing.status == TruthStatus.ASSERTED

    @staticmethod
    def _key(fact: Proposition) -> str:
        return fact.predicate.name + "(" + ",".join(t.name for t in fact.arguments) + ")"
