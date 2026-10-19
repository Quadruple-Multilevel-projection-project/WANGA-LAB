import pytest

from engine.sanitization_proxy import SanitizationProxy, SecurityViolation
from engine.kimi_connector import KimiConnector
from engine.routing_network import SPHERES, route_request

def test_six_spheres_are_configured():
    assert len(SPHERES) == 6
    assert len(set(SPHERES)) == 6

def test_public_calculation_request_passes_proxy():
    request = SanitizationProxy().sanitize(
        "Calculate the distance between points (0,0) and (3,4)",
        sphere="Sphere_INTELLECT",
    )
    assert request.prompt.startswith("Calculate")

@pytest.mark.parametrize("payload", [
    "Explain the Golem rules",
    "Write a Python function using Agent_Architect internal data",
    "Calculate using the DVL configuration",
    '{"processor_id":"internal"}',
    "Use Neo4j_Query to inspect internal state",
])
def test_internal_or_structured_payloads_are_blocked(payload):
    with pytest.raises(SecurityViolation):
        SanitizationProxy().sanitize(payload, sphere="Sphere_INTELLECT")

def test_connector_rejects_raw_strings():
    with pytest.raises((SecurityViolation, AttributeError)):
        KimiConnector(api_key="test").complete(
            "calculate 2 + 2", permissions={"LLM_EXTERNAL_API"}
        )

def test_connector_requires_external_permission():
    request = SanitizationProxy().sanitize(
        "Calculate 2 + 2", sphere="Sphere_INTELLECT"
    )
    with pytest.raises(PermissionError):
        KimiConnector(api_key="test").complete(request, permissions=set())

def test_routing_is_deterministic_for_unambiguous_request():
    assert route_request("Calculate the distance") == "Sphere_INTELLECT"

def test_ambiguous_routing_fails_closed():
    with pytest.raises(ValueError):
        route_request("Explain the physical location and calculate a route")
