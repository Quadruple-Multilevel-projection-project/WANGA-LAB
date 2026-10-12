# Logic Wiki Data Contract

articles.json is the human-edited catalog. readiness_gate.json contains provisional release criteria. agent_registry.json defines bounded research agent roles. The generator writes pages to logic_wiki/generated/.

Each article requires stable id, title, category, kind, status, definition, scope_note, sources and relations. Sources have stable IDs, source type and source status. A general logic reference and a WANGA proposal must never share an epistemic status just because both appear in the same wiki.