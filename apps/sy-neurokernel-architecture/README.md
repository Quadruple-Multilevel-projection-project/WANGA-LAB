# SY-NeuroKernel Structural Boundary UI

Experimental React prototype for the WANGA / SY-NeuroKernel architecture boundary.

## Structural invariants

- 22 address nodes
- C(22,2) = 231 unordered gates
- 22 × 21 = 462 directed relations
- 22 × 22 = 484 matrix cells
- Fixed K22 topology
- Neural processing may transform node states and rank existing relations, but does not create topology

## Runtime

The prototype is intentionally deployable as a single static HTML file. React, Tailwind and lucide-react are loaded from CDNs so the page can run without a local npm build.

This is an experimental representation surface, not evidence that the underlying architectural claims have been empirically validated.
