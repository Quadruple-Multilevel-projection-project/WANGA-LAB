"""Deterministic paper-trading prototype. No exchange/network/account integration."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import fmean
from typing import Literal

Action = Literal["HOLD", "PAPER_BUY", "PAPER_SELL", "PAPER_RISK_EXIT", "HALT"]


@dataclass(frozen=True)
class RiskPolicy:
    fast_window: int = 3
    slow_window: int = 5
    min_trend_spread: float = 0.002
    max_position_fraction: float = 0.10
    max_drawdown_fraction: float = 0.02
    max_single_tick_move: float = 0.08
    fee_rate: float = 0.001

    def __post_init__(self) -> None:
        if self.fast_window < 1 or self.slow_window <= self.fast_window:
            raise ValueError("slow_window must be greater than fast_window >= 1")
        for name in (
            "min_trend_spread", "max_position_fraction", "max_drawdown_fraction",
            "max_single_tick_move", "fee_rate",
        ):
            value = getattr(self, name)
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.max_position_fraction > 1:
            raise ValueError("max_position_fraction cannot exceed 1")
        if self.max_drawdown_fraction >= 1:
            raise ValueError("max_drawdown_fraction must be below 1")
        if self.max_single_tick_move >= 1:
            raise ValueError("max_single_tick_move must be below 1")
        if self.fee_rate >= 1:
            raise ValueError("fee_rate must be below 1")


@dataclass(frozen=True)
class Decision:
    action: Action
    price: float
    reason: str
    equity: float
    cash: float
    units: float
    fast_average: float | None
    slow_average: float | None
    lifecycle_state: str = "PROTOTYPED"
    execution_mode: str = "PAPER_ONLY"


class LogicTrader:
    """Rule-based research fixture; all fills are simulated locally in memory."""

    def __init__(self, initial_cash: float = 10_000.0, policy: RiskPolicy | None = None):
        if not isfinite(initial_cash) or initial_cash <= 0:
            raise ValueError("initial_cash must be finite and greater than zero")
        self.policy = policy or RiskPolicy()
        self.initial_cash = float(initial_cash)
        self.cash = float(initial_cash)
        self.units = 0.0
        self.prices: list[float] = []
        self.halted = False
        self.halt_reason: str | None = None
        self.realized_pnl = 0.0
        self.cost_basis = 0.0

    def equity(self, price: float) -> float:
        return self.cash + self.units * price

    def _decision(self, action: Action, price: float, reason: str,
                  fast: float | None = None, slow: float | None = None) -> Decision:
        return Decision(action, price, reason, self.equity(price), self.cash, self.units, fast, slow)

    def _close_position(self, price: float) -> float:
        if self.units <= 0:
            return 0.0
        gross = self.units * price
        fee = gross * self.policy.fee_rate
        proceeds = gross - fee
        self.cash += proceeds
        self.realized_pnl += proceeds - self.cost_basis
        self.cost_basis = 0.0
        self.units = 0.0
        return proceeds

    def step(self, price: float) -> Decision:
        if not isfinite(price) or price <= 0:
            raise ValueError("price must be finite and greater than zero")
        price = float(price)
        if self.halted:
            return self._decision("HALT", price, self.halt_reason or "Trading halted by risk gate")

        previous = self.prices[-1] if self.prices else None
        self.prices.append(price)

        if previous is not None:
            one_tick_move = abs(price / previous - 1.0)
            if one_tick_move >= self.policy.max_single_tick_move:
                self.halted = True
                self.halt_reason = f"Escape guard: single-tick move {one_tick_move:.2%} breached limit"
                return self._decision("HALT", price, self.halt_reason)

        equity = self.equity(price)
        drawdown = (self.initial_cash - equity) / self.initial_cash
        if drawdown >= self.policy.max_drawdown_fraction:
            self._close_position(price)
            self.halted = True
            self.halt_reason = f"Risk gate: drawdown {drawdown:.2%} reached limit"
            return self._decision("PAPER_RISK_EXIT", price, self.halt_reason)

        if len(self.prices) < self.policy.slow_window:
            return self._decision("HOLD", price, "Warm-up: insufficient price history")

        fast = fmean(self.prices[-self.policy.fast_window:])
        slow = fmean(self.prices[-self.policy.slow_window:])
        spread = (fast - slow) / slow

        if self.units == 0 and spread >= self.policy.min_trend_spread:
            equity = self.equity(price)
            budget = min(self.cash, equity * self.policy.max_position_fraction)
            # Fee is reserved before sizing; no borrowing or leverage is possible.
            purchasable = budget / (price * (1 + self.policy.fee_rate))
            if purchasable <= 0:
                return self._decision("HOLD", price, "Risk gate: no budget available", fast, slow)
            cost = purchasable * price
            fee = cost * self.policy.fee_rate
            self.cash -= cost + fee
            self.units += purchasable
            self.cost_basis += cost + fee
            return self._decision("PAPER_BUY", price, "Predictive-role trend rule passed risk gate", fast, slow)

        if self.units > 0 and spread < 0:
            self._close_position(price)
            return self._decision("PAPER_SELL", price, "Trend reversal; simulated position closed", fast, slow)

        return self._decision("HOLD", price, "No eligible rule signal", fast, slow)


def run_demo() -> list[Decision]:
    """Run a reproducible example using synthetic—not live—prices."""
    trader = LogicTrader()
    synthetic_prices = [100.0, 100.5, 101.0, 102.0, 103.0, 104.0, 103.5, 102.0, 101.0]
    return [trader.step(price) for price in synthetic_prices]
