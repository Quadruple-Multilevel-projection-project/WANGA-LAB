import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from logic_trader import LogicTrader, RiskPolicy  # noqa: E402


class LogicTraderTests(unittest.TestCase):
    def test_invalid_prices_are_rejected(self):
        trader = LogicTrader()
        for price in (0, -1, float("nan"), float("inf")):
            with self.subTest(price=price), self.assertRaises(ValueError):
                trader.step(price)

    def test_warmup_does_not_trade(self):
        trader = LogicTrader()
        for price in (100, 101, 102, 103):
            result = trader.step(price)
            self.assertEqual(result.action, "HOLD")
        self.assertEqual(trader.units, 0)

    def test_position_cap_is_enforced(self):
        policy = RiskPolicy(fast_window=2, slow_window=3, min_trend_spread=0.01,
                            max_single_tick_move=0.5)
        trader = LogicTrader(initial_cash=1000, policy=policy)
        result = None
        for price in (10, 10, 10, 11):
            result = trader.step(price)
        self.assertEqual(result.action, "PAPER_BUY")
        self.assertLessEqual(trader.units * 11, 1000 * policy.max_position_fraction + 1e-8)
        self.assertGreaterEqual(trader.cash, 0)

    def test_abrupt_price_move_halts_trader(self):
        policy = RiskPolicy(max_single_tick_move=0.05)
        trader = LogicTrader(policy=policy)
        trader.step(100)
        result = trader.step(94)
        self.assertEqual(result.action, "HALT")
        self.assertTrue(trader.halted)
        self.assertEqual(trader.step(95).action, "HALT")

    def test_invalid_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            RiskPolicy(fast_window=5, slow_window=3)
        with self.assertRaises(ValueError):
            RiskPolicy(max_position_fraction=1.1)

    def test_demo_is_deterministic(self):
        first = [(x.action, x.price, x.equity, x.units) for x in LogicTraderTests._demo()]
        second = [(x.action, x.price, x.equity, x.units) for x in LogicTraderTests._demo()]
        self.assertEqual(first, second)

    @staticmethod
    def _demo():
        from logic_trader import run_demo
        return run_demo()


if __name__ == "__main__":
    unittest.main()
