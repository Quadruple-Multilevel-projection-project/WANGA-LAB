# Neuronal GPS + External Tesseract Registry

**Status: SPECIFIED_NOT_DEPLOYED.** This folder records the intended schema and connection contract. It does not prove a live Supabase connection or deployment.

## Target

- 1,028 uniquely identified master-plugin instances.
- One separate routing center: `OMEGA_CENTER`.
- A mathematical 4D tesseract shell with 16 vertices and 32 edges.
- Supabase Postgres as the operational registry; GitHub as versioned source of truth for schema/configuration.
- Astronomy coordinates, symbolic coordinates, source mappings, and logic weights remain explicitly unresolved until supported by sources.

## Files

- `supabase/migrations/20261020_neuronal_gps_tesseract_v1.sql` — proposed schema and deterministic seed for 1,028 instance slots, one center, and 16 tesseract vertices.
- `config/neuronal_gps_tesseract_v1.json` — machine-readable deployment and unresolved-state contract.

## Important distinctions

1. The 1,028 rows are registry slots, not 1,028 installed/running plugins.
2. The central node is separate from the 1,028 instances.
3. A tesseract is a 4D hypercube: 16 vertices and 32 edges. The 1,028 agents are attached to the central routing graph; they are not 1,028 tesseract vertices.
4. Astronomical positions require a real catalog/ephemeris, coordinate frame, epoch and verified mapping from an instance to a celestial object. None is fabricated here.
5. At a 10 ms cadence, 1,028 instances produce 102,800 position samples/second. Before enabling history writes, define ingestion capacity, batching, partitioning, retention and backpressure.
6. Weights remain `UNRESOLVED`; no numeric weights are seeded.
7. RLS is enabled and no public/anonymous policies are created by default. Add authenticated access only after the ownership and authorization model is approved.

## Apply sequence

1. Restore/activate the Supabase project and inspect cost/status.
2. Review the migration and apply it to the intended project.
3. Verify row counts, foreign keys, RLS, and indexes.
4. Configure GitHub Actions or the official Supabase GitHub integration using least-privilege secrets in the platform settings. Never commit service-role keys.
5. Verify a round-trip write/read and CI migration check.
6. Run a three-instance routing test before attempting scale-out.
7. Add astronomy data only after the coordinate source and identity semantics are explicitly chosen.
