from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))
from logic_trader import run_demo  # noqa: E402


if __name__ == "__main__":
    print("LOGIC TRADER — PAPER-ONLY SYNTHETIC DEMO")
    print("No exchange connection, wallet access, or real orders are possible in this prototype.\n")
    for index, decision in enumerate(run_demo(), start=1):
        print(
            f"{index:02d} price={decision.price:8.2f} action={decision.action:16} "
            f"equity={decision.equity:9.2f} units={decision.units:.6f} reason={decision.reason}"
        )
