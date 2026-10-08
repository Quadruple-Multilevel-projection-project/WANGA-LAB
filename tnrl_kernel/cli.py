import json
from .architect import Architect, ArchitectureSpec

spec=ArchitectureSpec(
    name="TNRL-Kernel",
    version="0.1.0",
    layers=("source", "ontology", "talmudic_operators", "ir", "fol", "runtime"),
    operators=("kushya","terutz","reaya","dehiya","stira","havdalah","mekor","mahloket","hachraa"),
    kernel_contract={"higher_rational_logic": "external", "neural_bridge": "adapter"},
)
print(json.dumps(Architect().compile(spec), ensure_ascii=False, indent=2))
