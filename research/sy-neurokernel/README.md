# SY-NeuroKernel v0.2

A deterministic, provenance-preserving formal kernel for a 22-address combinatorial relation space.

## Hard invariants

- nodes: 22
- unordered gates: C(22,2) = 231
- directed relations: 22*21 = 462
- full matrix cells: 22*22 = 484

The kernel treats addresses as addresses. Structural tags are discrete metadata; they are not learned embeddings. The formal topology is immutable. The neural layer is optional and may score only relations already present in the formal gate space.

## Layout

```
sy-neurokernel/
  pyproject.toml
  sy_neurokernel/
    __init__.py
    alphabet.py
    gates.py
    graph.py
    neural.py
    engine.py
    provenance.py
  tests/
    test_invariants.py
  sandbox/
    index.html
```

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

The browser sandbox is static and requires no server or external dependency.

## Evidence boundary

The package encodes the formal/combinatorial kernel only. It does not encode historical, mystical, theological, or interpretive conclusions. Any future source-derived object must carry provenance and validation state.

Status: BUILT / TESTED / ARCHITECTURE-FIRST
