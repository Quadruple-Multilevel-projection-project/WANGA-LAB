# First-Order Logic — Part 3

## Transformations, Contradiction, and Dependencies

Part 3 models what happens when propositions are transformed, compared, or placed in a dependency graph.

```text
proposition
   ↓
transformation
   ↓
comparison
   ├── consistency
   └── contradiction
          ↓
dependency graph
          ↓
downstream conclusion
```

### Modules

`transformations` — logical transformations with explicit provenance.

`contradiction` — contradiction records, competing propositions, and resolution status.

`sentence-registry` — canonical registry connecting formal propositions to their source records.

A contradiction is recorded before any resolution is asserted. Resolution requires an explicit evidentiary basis.
