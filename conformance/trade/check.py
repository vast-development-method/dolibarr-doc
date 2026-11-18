"""Reconcile the trade chapter's ten checkpoints using exact decimal arithmetic."""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


EXAMPLE = Path(__file__).resolve().parents[2] / "examples/trade/trade-cycle--warehouse.valid.json"


def main():
    balances = dict(units=0, receivable=Decimal(0), payable=Decimal(0), bankChange=Decimal(0))
    events = json.loads(EXAMPLE.read_text())["events"]
    for step, event in enumerate(events, 1):
        operation = event["operation"]
        if operation == "receive":
            balances["units"] += event["quantity"]
        elif operation == "ship":
            balances["units"] -= event["quantity"]
        elif operation in {"supplier-invoice", "customer-invoice"}:
            net = Decimal(event["netUnitPrice"]) * event["quantity"]
            tax = (net * event["taxPercent"] / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            account = "payable" if operation == "supplier-invoice" else "receivable"
            balances[account] += net + tax
        elif operation in {"pay", "collect"}:
            amount = Decimal(event["amount"])
            account = "payable" if operation == "pay" else "receivable"
            balances[account] -= amount
            balances["bankChange"] += -amount if operation == "pay" else amount
        elif operation not in {"customer-order", "supplier-order"}:
            raise ValueError(f"Unknown operation {operation}")

        expected = {k: Decimal(v) for k, v in event["expect"].items()}
        if balances != expected:
            raise SystemExit(f"Step {step}, {operation}: computed {balances}, expected {expected}")
    print(f"Reconciled all {len(events)} trade-cycle checkpoints.")


if __name__ == "__main__":
    main()
