"""WANGA-X V1: requirement-derived, reversible architecture Blueprint engine."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = Path(__file__).with_name("catalog.json")
VALID_TASK_KINDS = {"logic_model_builder", "document_drift_analysis", "neural_computer_generation", "custom"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_catalog(path: str | Path | None = None) -> dict[str, Any]:
    data = json.loads((Path(path) if path else CATALOG_PATH).read_text(encoding="utf-8"))
    components = data.get("components", [])
    identifiers = [component["id"] for component in components]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Component IDs must be unique.")
    known = set(identifiers)
    for component in components:
        missing = set(component.get("dependencies", [])) - known
        if missing:
            raise ValueError(f"Unknown dependencies for {component['id']}: {sorted(missing)}")
    return data


def detect_provider_state(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Configuration is not the same as endpoint health or verification."""
    values = env if env is not None else os.environ
    llm = bool(values.get("WANGA_MODEL_BASE_URL") and values.get("WANGA_MODEL_NAME"))
    neural = bool(values.get("WANGA_NEURAL_RUNTIME_ADAPTER"))
    return {
        "llm": {"configured": llm, "status": "CONFIGURED_NOT_PROBED" if llm else "UNBOUND",
                "health_probe_status": "NOT_RUN", "base_url_present": bool(values.get("WANGA_MODEL_BASE_URL")),
                "model_name_present": bool(values.get("WANGA_MODEL_NAME"))},
        "neural_runtime": {"configured": neural, "verified": False,
                           "status": "CONFIGURED_NOT_VERIFIED" if neural else "UNAVAILABLE",
                           "adapter_name": values.get("WANGA_NEURAL_RUNTIME_ADAPTER") or None,
                           "health_probe_status": "NOT_RUN"},
    }


def workspace_state(repo_root: str | Path = ROOT) -> dict[str, Any]:
    path = Path(repo_root) / "docs" / "WORK_MEMORY_STATE.json"
    result = {
        "source": None,
        "model_fabric": {"target_slots": 5000, "allocated_slots": 0, "connected_slots": 0,
                         "verified_slots": 0, "status": "FALLBACK_TARGET_ONLY"},
        "perspective_layer": {"target_nodes": 1000, "populated_nodes": 0, "status": "TARGET_ONLY"},
        "reasoning_mode_taxonomy": {"target_modes": 28, "enumerated_modes_loaded": 0,
                                    "status": "TARGET_TAXONOMY_RECORDED_NAMES_NOT_LOADED"},
    }
    if not path.exists():
        return result
    state = json.loads(path.read_text(encoding="utf-8"))
    fabric = state.get("model_fabric", {})
    result["model_fabric"].update({
        "target_slots": fabric.get("target_model_slots", result["model_fabric"]["target_slots"]),
        "allocated_slots": fabric.get("allocated_slots", 0),
        "connected_slots": fabric.get("connected_slots", 0),
        "verified_slots": fabric.get("verified_slots", 0),
        "status": "ARCHITECTURAL_SLOTS_NOT_LIVE_ENDPOINTS",
    })
    perspective = state.get("perspective_layer", {})
    if isinstance(perspective, dict):
        result["perspective_layer"].update({
            "target_nodes": perspective.get("target_nodes", perspective.get("target_count", 1000)),
            "populated_nodes": perspective.get("populated_nodes", perspective.get("verified_nodes", 0)),
            "status": "TARGET_ONLY_UNLESS_POPULATION_EVIDENCED",
        })
    result["source"] = "docs/WORK_MEMORY_STATE.json"
    return result


def normalize_requirement(requirement: Mapping[str, Any], catalog: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(requirement, Mapping):
        raise ValueError("Requirement must be a JSON object.")
    goal = requirement.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("Requirement needs a non-empty goal.")
    task_kind = str(requirement.get("task_kind", "custom"))
    if task_kind not in VALID_TASK_KINDS:
        raise ValueError(f"Unknown task_kind {task_kind!r}; supported: {sorted(VALID_TASK_KINDS)}")
    profile = catalog["task_profiles"].get(task_kind, catalog["task_profiles"]["custom"])
    explicit = requirement.get("required_capabilities", [])
    optional = requirement.get("optional_capabilities", [])
    if not isinstance(explicit, list) or any(not isinstance(item, str) for item in explicit):
        raise ValueError("required_capabilities must be a list of strings.")
    if not isinstance(optional, list) or any(not isinstance(item, str) for item in optional):
        raise ValueError("optional_capabilities must be a list of strings.")
    inputs = requirement.get("input_types", ["structured_requirements"])
    outputs = requirement.get("output_types", ["blueprint", "verification_report"])
    if not isinstance(inputs, list) or not all(isinstance(item, str) for item in inputs):
        raise ValueError("input_types must be a list of strings.")
    if not isinstance(outputs, list) or not all(isinstance(item, str) for item in outputs):
        raise ValueError("output_types must be a list of strings.")
    constraints = requirement.get("constraints", {})
    resources = requirement.get("resource_limits", {})
    if not isinstance(constraints, dict) or not isinstance(resources, dict):
        raise ValueError("constraints and resource_limits must be objects.")
    known = set(catalog.get("computation_definitions", {}))
    for component in catalog["components"]:
        known.update(component.get("provides", []))
    unknown = sorted(set(explicit + optional) - known)
    if unknown:
        raise ValueError(f"Unknown capabilities; use catalog-defined names only: {unknown}")

    profile_required = set(profile.get("required_capabilities", []))
    required = profile_required | set(explicit) | set(catalog["mandatory_capabilities"])
    optional_set = set(profile.get("optional_capabilities", [])) | set(optional)
    if "natural_language" in inputs:
        required.add("natural_language_requirement_interpretation")
        optional_set.discard("natural_language_requirement_interpretation")
    if constraints.get("require_neural_runtime") is True:
        required.add("neural_runtime_materialization")
        optional_set.discard("neural_runtime_materialization")
    if constraints.get("require_source_provenance", True):
        required.add("source_provenance")
    if constraints.get("require_verification", True):
        required.add("goal_verification")
    if constraints.get("require_reversible_builds", True):
        required.add("reversible_builds")

    computations = []
    for index, capability in enumerate(sorted(required), 1):
        computations.append({
            "id": f"NC-{index:03d}",
            "capability": capability,
            "operation": catalog["computation_definitions"].get(capability, f"Provide declared capability: {capability}."),
            "derived_from": "TASK_PROFILE_OR_EXPLICIT_REQUIREMENT" if capability in profile_required | set(explicit) else "WANGA_X_INTEGRITY_CONSTRAINT",
        })
    rid = str(requirement.get("requirement_id") or "REQ-" + stable_hash({
        "goal": goal.strip(), "task_kind": task_kind, "required_capabilities": sorted(required)
    })[:12].upper())
    return {
        "requirement_id": rid, "goal": goal.strip(), "task_kind": task_kind,
        "input_types": sorted(set(inputs)), "output_types": sorted(set(outputs)),
        "required_capabilities": sorted(required), "optional_capabilities": sorted(optional_set),
        "required_neural_computation": computations,
        "constraints": {
            "require_source_provenance": constraints.get("require_source_provenance", True),
            "require_verification": constraints.get("require_verification", True),
            "require_reversible_builds": constraints.get("require_reversible_builds", True),
            "no_automatic_publication": constraints.get("no_automatic_publication", True),
            "require_neural_runtime": constraints.get("require_neural_runtime", False),
            "max_components": int(resources.get("max_components", 20)),
        },
        "resource_limits": dict(resources),
        "source_status": "USER_REQUIREMENT_STRUCTURED_NOT_SEMANTICALLY_VERIFIED",
    }


def _component_available(component: Mapping[str, Any], providers: Mapping[str, Any]) -> bool:
    state = component.get("availability", "BUILT")
    if state == "BUILT":
        return True
    if state == "REQUIRES_CONFIGURED_LLM":
        return bool(providers.get("llm", {}).get("configured"))
    if state == "REQUIRES_VERIFIED_NEURAL_BACKEND":
        return bool(providers.get("neural_runtime", {}).get("verified"))
    return state in {
        "BUILT_REGISTRY_LIVE_ENDPOINTS_UNVERIFIED",
        "BLUEPRINT_ONLY_NO_TRAINING_BACKEND",
        "BUILT_ROUTING_CONTRACT_PERSPECTIVE_NODES_UNPOPULATED",
    }


def _dependency_closure(
    selected_ids: set[str], components: Mapping[str, Mapping[str, Any]], providers: Mapping[str, Any]
) -> tuple[set[str], list[str]]:
    resolved: set[str] = set()
    blocked: set[str] = set()
    visiting: set[str] = set()

    def add(component_id: str) -> bool:
        if component_id in resolved:
            return True
        if component_id in visiting:
            blocked.add(component_id + ":DEPENDENCY_CYCLE")
            return False
        component = components.get(component_id)
        if component is None:
            blocked.add(component_id + ":UNKNOWN_COMPONENT")
            return False
        if not _component_available(component, providers):
            blocked.add(component_id + ":UNAVAILABLE:" + str(component.get("availability")))
            return False
        visiting.add(component_id)
        dependencies_ok = all(add(dependency) for dependency in component.get("dependencies", []))
        visiting.discard(component_id)
        if not dependencies_ok:
            blocked.add(component_id + ":DEPENDENCY_UNRESOLVED")
            return False
        resolved.add(component_id)
        return True

    for component_id in sorted(selected_ids):
        add(component_id)
    return resolved, sorted(blocked)


def _topological_order(selected: set[str], components: Mapping[str, Mapping[str, Any]]) -> list[str]:
    pending = set(selected)
    ordered: list[str] = []
    while pending:
        ready = sorted(
            component_id for component_id in pending
            if (set(components[component_id].get("dependencies", [])) & selected) <= set(ordered)
        )
        if not ready:
            raise ValueError(f"Architecture dependency cycle or missing dependency: {sorted(pending)}")
        ordered.extend(ready)
        pending.difference_update(ready)
    return ordered


def _candidate_for_strategy(
    requirement: Mapping[str, Any], catalog: Mapping[str, Any], providers: Mapping[str, Any], strategy: str
) -> dict[str, Any]:
    all_components = {component["id"]: component for component in catalog["components"]}
    available = [component for component in catalog["components"] if _component_available(component, providers)]
    providers_by_capability: dict[str, list[dict[str, Any]]] = {}
    for component in available:
        for capability in component.get("provides", []):
            providers_by_capability.setdefault(capability, []).append(component)
    selected = {
        "requirement_normalizer", "rational_logic", "provenance_ledger",
        "source_registry", "verification_gate", "reversible_state_manager", "blueprint_materializer",
    }
    rationale: dict[str, str] = {}
    for capability in requirement["required_capabilities"]:
        candidates = list(providers_by_capability.get(capability, []))
        if not candidates:
            rationale[capability] = "NO_ELIGIBLE_COMPONENT_FOR_REQUIRED_CAPABILITY"
            continue
        if strategy == "AUDIT_FIRST":
            candidates.sort(key=lambda item: (-item.get("audit_score", 0), item.get("cost", 100), item["id"]))
        elif strategy == "EXTENSIBILITY_FIRST":
            candidates.sort(key=lambda item: (-item.get("extensibility_score", 0), item.get("cost", 100), item["id"]))
        else:
            candidates.sort(key=lambda item: (item.get("cost", 100), -item.get("audit_score", 0), item["id"]))
        selected.add(candidates[0]["id"])
        rationale[capability] = f"SELECTED:{candidates[0]['id']}:{strategy}"
    closure, blocked = _dependency_closure(selected, all_components, providers)
    covered = sorted({
        capability for component_id in closure for capability in all_components[component_id].get("provides", [])
    } & set(requirement["required_capabilities"]))
    missing = sorted(set(requirement["required_capabilities"]) - set(covered))
    comp_cost = sum(all_components[component_id].get("cost", 1) for component_id in closure)
    audit_score = sum(all_components[component_id].get("audit_score", 0) for component_id in closure)
    extension_score = sum(all_components[component_id].get("extensibility_score", 0) for component_id in closure)
    external_count = sum(
        1 for component_id in closure
        if str(all_components[component_id].get("availability", "")).startswith("REQUIRES_")
    )
    bonus = audit_score * 0.9 if strategy == "AUDIT_FIRST" else extension_score * 0.9 if strategy == "EXTENSIBILITY_FIRST" else 0
    score = len(covered) * 100 - len(missing) * 80 - comp_cost * 2 - external_count * 8 + bonus
    order = _topological_order(closure, all_components)
    return {
        "strategy": strategy, "selected_component_ids": order, "coverage": covered,
        "missing_capabilities": missing, "blocked_dependencies": blocked, "rationale": rationale,
        "component_cost_score": comp_cost, "audit_score": audit_score,
        "extensibility_score": extension_score, "candidate_score": round(score, 3),
    }


def _make_frame(frame_id: str, stage: str, state: Any, parent_hash: str | None, event_type: str = "STATE") -> dict[str, Any]:
    frame = {"frame_id": frame_id, "stage": stage, "event_type": event_type,
             "parent_frame_hash": parent_hash, "state": state}
    frame["frame_hash"] = stable_hash(frame)
    return frame


def build_blueprint(
    raw_requirement: Mapping[str, Any], *, repo_root: str | Path = ROOT,
    catalog: Mapping[str, Any] | None = None, provider_state: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    providers = provider_state or detect_provider_state()
    normalized = normalize_requirement(raw_requirement, catalog)
    component_map = {item["id"]: item for item in catalog["components"]}
    candidates = [
        _candidate_for_strategy(normalized, catalog, providers, strategy)
        for strategy in ("MINIMAL_COST", "AUDIT_FIRST", "EXTENSIBILITY_FIRST")
    ]
    winner = sorted(candidates, key=lambda item: (-item["candidate_score"], item["component_cost_score"], item["strategy"]))[0]
    selected = winner["selected_component_ids"]
    selected_set = set(selected)
    covered = sorted({
        capability for component_id in selected
        for capability in component_map[component_id].get("provides", [])
    } & set(normalized["required_capabilities"]))
    missing = sorted(set(normalized["required_capabilities"]) - set(covered))

    unbound = []
    for component in catalog["components"]:
        if component["id"] in selected_set or _component_available(component, providers):
            continue
        required_match = sorted(set(component.get("provides", [])) & set(missing))
        if required_match:
            unbound.append({
                "component_id": component["id"], "status": "PLANNED_UNBOUND",
                "provides": component.get("provides", []),
                "required_capabilities": required_match,
                "availability": component.get("availability"),
            })

    optional_unbound = []
    for capability in normalized["optional_capabilities"]:
        if capability in covered:
            continue
        candidates_for_cap = [item for item in catalog["components"] if capability in item.get("provides", [])]
        if candidates_for_cap and not any(_component_available(item, providers) for item in candidates_for_cap):
            optional_unbound.append(capability)

    selected_components = []
    for position, component_id in enumerate(selected, 1):
        component = component_map[component_id]
        selected_components.append({
            "position": position, "component_id": component_id, "name": component["name"],
            "provides": component.get("provides", []), "dependencies": component.get("dependencies", []),
            "availability": component.get("availability"),
            "execution_state": "REGISTRY_OR_CODE_AVAILABLE_NOT_AUTOMATICALLY_VERIFIED",
            "source_path": f"wanga_x_v1/catalog.json#{component_id}",
        })
    edges = [
        {"from": dependency, "to": component_id, "relation": "REQUIRES"}
        for component_id in selected for dependency in component_map[component_id].get("dependencies", [])
        if dependency in selected_set
    ]
    target_state = workspace_state(repo_root)
    core = {
        "blueprint_version": "wanga-x/1.0",
        "requirement_id": normalized["requirement_id"], "goal": normalized["goal"], "task_kind": normalized["task_kind"],
        "input_types": normalized["input_types"], "output_types": normalized["output_types"],
        "required_capabilities": normalized["required_capabilities"], "optional_capabilities": normalized["optional_capabilities"],
        "required_neural_computation": normalized["required_neural_computation"],
        "selected_architecture_strategy": winner["strategy"], "selected_components": selected_components,
        "component_order": selected, "dependency_edges": edges, "missing_capabilities": missing,
        "planned_unbound_components": unbound, "optional_unbound_capabilities": optional_unbound,
        "candidate_architectures": candidates, "provider_state": providers,
        "target_architecture_inventory": target_state,
        "materialization_contract": {
            "artifact_generated": True, "actual_neural_weights_generated": False,
            "live_model_endpoint_created": False, "execution_authority": "NOT_GRANTED",
            "publication_authority": "NOT_GRANTED",
        },
        "constraints": normalized["constraints"],
    }
    blueprint = dict(core)
    blueprint["blueprint_hash_sha256"] = stable_hash(core)

    frames = []
    parent = None
    stages = [
        ("F0", "REQUIREMENT_CAPTURED", {"requirement": dict(raw_requirement)}),
        ("F1", "REQUIREMENT_NORMALIZED", {"normalized_requirement": normalized}),
        ("F2", "REQUIRED_COMPUTATION_DERIVED", {"required_neural_computation": normalized["required_neural_computation"]}),
        ("F3", "ARCHITECTURE_CANDIDATES_RANKED", {"candidate_architectures": candidates, "selected_strategy": winner["strategy"]}),
        ("F4", "BLUEPRINT_GENERATED", {"blueprint_hash_sha256": blueprint["blueprint_hash_sha256"],
                                         "component_order": selected, "missing_capabilities": missing}),
    ]
    for frame_id, stage, state in stages:
        frame = _make_frame(frame_id, stage, state, parent)
        frames.append(frame)
        parent = frame["frame_hash"]

    verification = verify_blueprint(blueprint, catalog)
    frames.append(_make_frame("F5", "BLUEPRINT_STRUCTURALLY_VERIFIED", verification, parent))
    if verification["status"] != "PASS":
        build_status = "BLUEPRINT_CONTRACT_FAILURE_REVIEW"
    elif missing:
        build_status = "BLUEPRINT_INCOMPLETE_REQUIRED_CAPABILITY_BLOCKED"
    else:
        build_status = "BLUEPRINT_READY_FOR_REVIEW"
    return {
        "system": "WANGA-X Requirement-Driven Blueprint Engine V1",
        "build_status": build_status, "requirement": normalized,
        "required_neural_computation": normalized["required_neural_computation"],
        "blueprint": blueprint, "verification": verification, "construction_frames": frames,
        "reversibility": {
            "supported_operations": ["PAUSE", "SNAPSHOT", "INSPECT", "ROLLBACK", "EDIT_REQUIREMENT", "REBUILD", "VERIFY", "COMMIT"],
            "current_operation": "BLUEPRINT_BUILD",
            "history_policy": "APPEND_ONLY; rollback appends a new branch frame and does not rewrite prior frames",
        },
        "status_limits": [
            "The engine generates and verifies a Blueprint artifact, not trained neural weights.",
            "Connected/verified model counts are read from repository state; target slots are not live endpoints.",
            "A configured model endpoint is not considered healthy or verified until a separate probe succeeds.",
            "A requirement-derived computation is an engineering proposal until acceptance tests establish adequate coverage.",
        ],
    }


def verify_blueprint(blueprint: Mapping[str, Any], catalog: Mapping[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    component_map = {component["id"]: component for component in catalog["components"]}
    selected_records = blueprint.get("selected_components", [])
    ids = [record.get("component_id") for record in selected_records]
    selected = set(ids)
    errors = []
    blockers = []
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_COMPONENT_ID")
    for component_id in ids:
        component = component_map.get(component_id)
        if component is None:
            errors.append("UNKNOWN_COMPONENT:" + str(component_id))
            continue
        for dependency in component.get("dependencies", []):
            if dependency not in selected:
                errors.append(f"MISSING_DEPENDENCY:{component_id}:{dependency}")
    provided = {cap for component_id in selected if component_id in component_map for cap in component_map[component_id].get("provides", [])}
    blockers.extend("REQUIRED_CAPABILITY_NOT_COVERED:" + cap for cap in sorted(set(blueprint.get("required_capabilities", [])) - provided))
    if not blueprint.get("blueprint_hash_sha256"):
        errors.append("MISSING_BLUEPRINT_HASH")
    if not blueprint.get("requirement_id"):
        errors.append("MISSING_REQUIREMENT_ID")
    contract = blueprint.get("materialization_contract", {})
    if contract.get("actual_neural_weights_generated") is True:
        errors.append("UNSUPPORTED_CLAIM_NEURAL_WEIGHTS_GENERATED")
    if contract.get("live_model_endpoint_created") is True:
        errors.append("UNSUPPORTED_CLAIM_LIVE_ENDPOINT_CREATED")
    return {
        "status": "PASS" if not errors else "FAIL",
        "checks": {
            "component_ids_unique": "DUPLICATE_COMPONENT_ID" not in errors,
            "dependencies_closed": not any(error.startswith("MISSING_DEPENDENCY:") for error in errors),
            "required_capabilities_covered": not any(item.startswith("REQUIRED_CAPABILITY_NOT_COVERED:") for item in blockers),
            "blueprint_hash_present": "MISSING_BLUEPRINT_HASH" not in errors,
            "requirement_id_present": "MISSING_REQUIREMENT_ID" not in errors,
            "no_false_neural_materialization_claim": "UNSUPPORTED_CLAIM_NEURAL_WEIGHTS_GENERATED" not in errors,
            "no_false_live_endpoint_claim": "UNSUPPORTED_CLAIM_LIVE_ENDPOINT_CREATED" not in errors,
        },
        "errors": sorted(set(errors)), "blockers": blockers,
        "verification_scope": "STRUCTURAL_BLUEPRINT_CONTRACT_ONLY_NOT_EMPIRICAL_MODEL_QUALITY",
    }


def append_rollback_frame(run: Mapping[str, Any], target_frame_id: str, change_note: str) -> dict[str, Any]:
    frames = list(run.get("construction_frames", []))
    target = next((frame for frame in frames if frame.get("frame_id") == target_frame_id), None)
    if target is None:
        raise ValueError(f"Unknown frame ID {target_frame_id!r}")
    parent_hash = frames[-1]["frame_hash"] if frames else None
    state = {
        "rollback_target_frame_id": target_frame_id, "rollback_target_hash": target["frame_hash"],
        "change_note": change_note, "restored_state_reference": target["state"],
    }
    new_id = f"FR{len(frames):02d}"
    rollback = _make_frame(new_id, "ROLLBACK_BRANCH_CREATED", state, parent_hash, event_type="ROLLBACK_AND_BRANCH")
    updated = dict(run)
    updated["construction_frames"] = frames + [rollback]
    updated["reversibility"] = dict(run.get("reversibility", {}))
    updated["reversibility"].update({
        "current_operation": "ROLLBACK_BRANCH_CREATED",
        "rollback_parent_frame_id": target_frame_id,
        "rollback_frame_id": new_id,
    })
    return updated


def write_artifact(result: Mapping[str, Any], out_path: str | Path) -> None:
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
