"""Run portable examples of the Dolibarr 24.0.3 sales decision rules."""

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import sys


def allocation(data):
    """Check the optional ceiling for a positive, order-backed goods allocation."""
    reserved = sum(
        Decimal(row["qty"]) for row in data["allocations"]
        if row["orderLine"] == data["orderLine"]
        and row["shipmentStatus"] >= 0
        and row["rowId"] != data.get("editingRow")
    )
    remaining = Decimal(data["orderedQty"]) - reserved
    return {
        "remainingBeforeRequest": str(remaining),
        "permittedByCeiling": not data["ceilingEnabled"] or Decimal(data["requestedQty"]) <= remaining,
    }


def completion(data):
    """Evaluate the two independent order-close paths after a shipment event."""
    by_line = defaultdict(Decimal)
    by_product = defaultdict(Decimal)
    expected_products = defaultdict(Decimal)
    for row in data["shipments"]:
        qty = Decimal(row["qty"])
        if row["status"] >= 2:
            by_line[row["orderLine"]] += qty
        if row["status"] > 0:
            by_product[row["product"]] += qty

    line_match = True
    for line in data["orderLines"]:
        qty = Decimal(line["qty"])
        if line["type"] == "goods" or data["stockSupportsServices"]:
            if by_line[line["id"]] != qty:
                line_match = False
        if line["type"] == "goods" or (data["stockSupportsServices"] and line["type"] != "title"):
            expected_products[line["product"]] += qty

    product_match = all(
        product in by_product and by_product[product] == qty
        for product, qty in expected_products.items()
    )
    return {
        "coreRequestsClosure": data["event"] == "close" and line_match,
        "workflowRequestsClosure": data["event"] in data["workflowEvents"] and product_match,
    }


def rounded_net(value, places):
    quantum = Decimal(1).scaleb(-places)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def cumulative_billing(data):
    """Compare one order with all its linked invoices on invoice validation."""
    if not data["enabled"] or data["sourceOrderCount"] != 1 or not data["linkedInvoices"]:
        return False
    total = Decimal(0)
    for invoice in data["linkedInvoices"]:
        if invoice["id"] != data["validatingInvoice"] and invoice["state"] not in ("validated", "closed"):
            return False
        total += Decimal(invoice["net"])
    return rounded_net(total, data["totalPrecision"]) == rounded_net(
        Decimal(data["orderNet"]), data["totalPrecision"]
    )


def direct_billing(data):
    """Test the amount gate for a validating invoice and its linked orders."""
    if not data["enabled"] or not data["linkedOrders"]:
        return False
    total = sum(
        (Decimal(order["net"]) for order in data["linkedOrders"]
         if order["state"] in ("validated", "shipment-in-process", "delivered")),
        Decimal(0),
    )
    return data["allowDifferentAmounts"] or rounded_net(total, data["totalPrecision"]) == rounded_net(
        Decimal(data["invoiceNet"]), data["totalPrecision"]
    )


def main():
    scenarios = json.loads(Path(__file__).with_name("scenarios.json").read_text(encoding="utf-8"))
    checks = {
        "allocation": allocation,
        "completion": completion,
        "cumulativeBilling": cumulative_billing,
        "directBilling": direct_billing,
    }
    case_ids = set()
    failures = 0
    for case in scenarios["cases"]:
        case_id = case["id"]
        if case_id in case_ids:
            raise ValueError(f"Duplicate case ID: {case_id}")
        case_ids.add(case_id)
        actual = checks[case["rule"]](case["input"])
        if actual != case["expected"]:
            failures += 1
            print(f"FAIL {case_id}: expected {case['expected']!r}, got {actual!r}", file=sys.stderr)
    print(f"{len(case_ids) - failures}/{len(case_ids)} sales decision scenarios passed")
    return int(failures > 0)


if __name__ == "__main__":
    sys.exit(main())
