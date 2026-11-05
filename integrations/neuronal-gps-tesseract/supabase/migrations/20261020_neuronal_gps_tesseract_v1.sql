-- Supabase migration proposal: external tesseract + 1,028-agent registry
-- Status: SPECIFIED_NOT_DEPLOYED. Coordinates and weights are intentionally unresolved.
-- Apply only after the Supabase project is restored and this migration is reviewed.

create extension if not exists pgcrypto;

create table if not exists public.logic_nodes (
  node_id text primary key,
  node_kind text not null check (node_kind in ('OMEGA_CENTER','MASTER_PLUGIN','QUADRANT_MANAGER','TESSERACT_VERTEX')),
  display_name text not null,
  status text not null default 'SPECIFIED_NOT_DEPLOYED',
  source_ref text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.master_plugin_instances (
  instance_id text primary key,
  ordinal integer not null unique check (ordinal between 1 and 1028),
  center_node_id text not null references public.logic_nodes(node_id),
  quadrant_id text check (quadrant_id in ('Q1_NORTH','Q2_EAST','Q3_SOUTH','Q4_WEST')),
  root_id text,
  config_id text,
  deployment_status text not null default 'SPECIFIED_NOT_DEPLOYED',
  capability_manifest jsonb not null default '{}'::jsonb,
  source_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.agent_positions_latest (
  instance_id text primary key references public.master_plugin_instances(instance_id) on delete cascade,
  coordinate_source text,
  coordinate_frame text,
  observed_at timestamptz,
  right_ascension_deg double precision,
  declination_deg double precision,
  distance_value double precision,
  distance_unit text,
  symbolic_x double precision,
  symbolic_y double precision,
  symbolic_z double precision,
  tesseract_vertex_id text,
  position_status text not null default 'UNRESOLVED',
  evidence_ref text,
  updated_at timestamptz not null default now(),
  check (right_ascension_deg is null or (right_ascension_deg >= 0 and right_ascension_deg < 360)),
  check (declination_deg is null or (declination_deg >= -90 and declination_deg <= 90))
);

create table if not exists public.logic_edges (
  edge_id uuid primary key default gen_random_uuid(),
  source_node_id text not null references public.logic_nodes(node_id) on delete cascade,
  target_node_id text not null references public.logic_nodes(node_id) on delete cascade,
  edge_type text not null,
  status text not null default 'SPECIFIED_NOT_DEPLOYED',
  source_ref text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(source_node_id, target_node_id, edge_type),
  check (source_node_id <> target_node_id)
);

create table if not exists public.logic_weight_slots (
  weight_slot_id text primary key,
  target_id text not null,
  weight_value double precision,
  weight_status text not null default 'UNRESOLVED',
  derivation_ref text,
  evidence_ref text,
  updated_at timestamptz not null default now(),
  check (
    (weight_status = 'UNRESOLVED' and weight_value is null)
    or
    (weight_status in ('DERIVED','MEASURED','REVIEWED') and weight_value is not null
      and derivation_ref is not null and evidence_ref is not null)
  )
);

create table if not exists public.agent_position_samples (
  sample_id bigint generated always as identity primary key,
  instance_id text not null references public.master_plugin_instances(instance_id) on delete cascade,
  observed_at timestamptz not null,
  coordinate_source text not null,
  coordinate_frame text not null,
  right_ascension_deg double precision,
  declination_deg double precision,
  distance_value double precision,
  distance_unit text,
  evidence_ref text,
  payload jsonb not null default '{}'::jsonb,
  check (right_ascension_deg is null or (right_ascension_deg >= 0 and right_ascension_deg < 360)),
  check (declination_deg is null or (declination_deg >= -90 and declination_deg <= 90))
);

create index if not exists idx_position_samples_instance_time
  on public.agent_position_samples(instance_id, observed_at desc);
create index if not exists idx_logic_edges_target on public.logic_edges(target_node_id);
create index if not exists idx_plugin_instances_quadrant on public.master_plugin_instances(quadrant_id);

alter table public.logic_nodes enable row level security;
alter table public.master_plugin_instances enable row level security;
alter table public.agent_positions_latest enable row level security;
alter table public.logic_edges enable row level security;
alter table public.logic_weight_slots enable row level security;
alter table public.agent_position_samples enable row level security;

-- No anon/authenticated policies are created. Access must be added deliberately
-- after the intended auth/tenant model is approved. Never expose service_role keys.

insert into public.logic_nodes (node_id, node_kind, display_name, status, metadata)
values ('OMEGA_CENTER', 'OMEGA_CENTER', 'Central Ω Orchestrator', 'SPECIFIED_NOT_DEPLOYED',
        '{"purpose":"single logical routing center","coordinates_status":"UNRESOLVED"}'::jsonb)
on conflict (node_id) do nothing;

insert into public.logic_nodes (node_id, node_kind, display_name, status, metadata)
values
  ('TESSERACT_V00','TESSERACT_VERTEX','Tesseract vertex 0000','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0000"}'::jsonb),
  ('TESSERACT_V01','TESSERACT_VERTEX','Tesseract vertex 0001','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0001"}'::jsonb),
  ('TESSERACT_V02','TESSERACT_VERTEX','Tesseract vertex 0010','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0010"}'::jsonb),
  ('TESSERACT_V03','TESSERACT_VERTEX','Tesseract vertex 0011','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0011"}'::jsonb),
  ('TESSERACT_V04','TESSERACT_VERTEX','Tesseract vertex 0100','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0100"}'::jsonb),
  ('TESSERACT_V05','TESSERACT_VERTEX','Tesseract vertex 0101','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0101"}'::jsonb),
  ('TESSERACT_V06','TESSERACT_VERTEX','Tesseract vertex 0110','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0110"}'::jsonb),
  ('TESSERACT_V07','TESSERACT_VERTEX','Tesseract vertex 0111','SPECIFIED_NOT_DEPLOYED','{"bit_address":"0111"}'::jsonb),
  ('TESSERACT_V08','TESSERACT_VERTEX','Tesseract vertex 1000','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1000"}'::jsonb),
  ('TESSERACT_V09','TESSERACT_VERTEX','Tesseract vertex 1001','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1001"}'::jsonb),
  ('TESSERACT_V10','TESSERACT_VERTEX','Tesseract vertex 1010','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1010"}'::jsonb),
  ('TESSERACT_V11','TESSERACT_VERTEX','Tesseract vertex 1011','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1011"}'::jsonb),
  ('TESSERACT_V12','TESSERACT_VERTEX','Tesseract vertex 1100','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1100"}'::jsonb),
  ('TESSERACT_V13','TESSERACT_VERTEX','Tesseract vertex 1101','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1101"}'::jsonb),
  ('TESSERACT_V14','TESSERACT_VERTEX','Tesseract vertex 1110','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1110"}'::jsonb),
  ('TESSERACT_V15','TESSERACT_VERTEX','Tesseract vertex 1111','SPECIFIED_NOT_DEPLOYED','{"bit_address":"1111"}'::jsonb)
on conflict (node_id) do nothing;

insert into public.master_plugin_instances (instance_id, ordinal, center_node_id, quadrant_id, root_id, config_id)
select
  'MASTER-PLUGIN-' || lpad(n::text, 4, '0'),
  n,
  'OMEGA_CENTER',
  case when n <= 257 then 'Q1_NORTH'
       when n <= 514 then 'Q2_EAST'
       when n <= 771 then 'Q3_SOUTH'
       else 'Q4_WEST' end,
  null,
  null
from generate_series(1, 1028) as n
on conflict (instance_id) do nothing;

insert into public.agent_positions_latest (instance_id, position_status)
select instance_id, 'UNRESOLVED'
from public.master_plugin_instances
on conflict (instance_id) do nothing;

insert into public.logic_edges (source_node_id, target_node_id, edge_type, status, metadata)
select instance_id, 'OMEGA_CENTER', 'ROUTES_TO_CENTER', 'SPECIFIED_NOT_DEPLOYED',
       '{"claim_status":"planned topology; not a live connection"}'::jsonb
from public.master_plugin_instances
on conflict (source_node_id, target_node_id, edge_type) do nothing;

insert into public.logic_edges (source_node_id, target_node_id, edge_type, status, metadata)
select 'OMEGA_CENTER', 'TESSERACT_V' || lpad(n::text, 2, '0'), 'TESSERACT_VERTEX_LINK',
       'SPECIFIED_NOT_DEPLOYED', '{"topology":"4D hypercube vertex; no physical entanglement implied"}'::jsonb
from generate_series(0, 15) as n
on conflict (source_node_id, target_node_id, edge_type) do nothing;

-- The 32 actual tesseract edges: connect vertex addresses that differ in exactly one bit.
insert into public.logic_edges (source_node_id, target_node_id, edge_type, status, metadata)
select
  'TESSERACT_V' || lpad(a::text, 2, '0'),
  'TESSERACT_V' || lpad(b::text, 2, '0'),
  'TESSERACT_HYPERCUBE_EDGE',
  'SPECIFIED_NOT_DEPLOYED',
  '{"topology":"4D hypercube edge; symbolic graph only"}'::jsonb
from generate_series(0, 15) as a
cross join generate_series(0, 15) as b
where a < b
  and ((a # b) & ((a # b) - 1)) = 0
on conflict (source_node_id, target_node_id, edge_type) do nothing;

-- Deliberately no weights, astronomy positions, or root/config assignments are fabricated.
-- Expected seed counts: 1 center + 16 tesseract vertices; 1,028 plugin instances;
-- 1,028 center-routing edges + 16 center-to-vertex links + 32 tesseract edges.
