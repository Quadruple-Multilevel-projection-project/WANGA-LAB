# WANGA TANTA & 231 Extractor v1.0

## What this implementation does
- Enumerates all unordered pairs from the 22-letter Hebrew alphabet: C(22,2)=231.
- Places the 231 catalog entries bijectively in a 21x11 index matrix.
- Computes reproducible visualization coordinates and phase angles.
- Records literal adjacent-letter occurrences in UTF-8 source files with SHA-256 and character offsets.
- Keeps Taamim, Nekudot, Tagin, and Otiot as separate data layers.
- Defaults every gate to ABSTAIN until authoritative semantic evidence and independent approval exist.

## What it deliberately does not claim
- A slot number in the 230-slot index is not an identified crystallographic space group.
- Pseudo-vectors are visualization coordinates, not measured physical vectors.
- A literal pair occurrence does not establish a semantic operator.
- No quantum, subatomic, photonic, or physical processor mapping is inferred.
- This version does not call Gemini or any external model. A future AI-assisted extractor must produce candidate annotations only.

## Run locally
```bash
python scripts/run_extractor.py --input-dir sources --output-dir compiled
python -m pip install -r requirements-extractor.txt
pytest -q tests/test_wanga_extractor.py
```

## Output
- `compiled/wanga_231_gate_catalog.json`
- `compiled/source_observations.json`
- `compiled/run_summary.json`

## Required next inputs for semantic compilation
1. Canonical, licensed source corpus with edition/page metadata.
2. Approved pair ordering and any non-default gate ordering.
3. Authoritative TANTA annotation rules for all four layers.
4. Explicit mapping registry for any proposed 230-group correspondence.
5. Human-approved LOCK authority and auditable approval records.

Until these are supplied, the correct output is ABSTAIN, not fabricated completion.
