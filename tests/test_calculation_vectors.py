"""Test-only arithmetic oracle for synthetic payroll calculation vectors.

This is not application code and does not implement Kenyan statutory rules.
"""

from __future__ import annotations

import json
import re
import unittest
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "tests" / "vectors" / "payroll-calculation-vectors.json"
MONEY_PATTERN = re.compile(r"^(?:0|[1-9]\d*)(?:\.\d{1,2})?$")
QUANTITY_PATTERN = re.compile(r"^(?:0|[1-9]\d*)(?:\.\d{1,4})?$")
CENT = Decimal("0.01")
ZERO = Decimal("0.00")


class CalculationError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _decimal(value: Any, pattern: re.Pattern[str], error: str) -> Decimal:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise CalculationError(error)
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise CalculationError(error) from exc


def _period(value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise CalculationError("INVALID_PERIOD")
    try:
        start = date.fromisoformat(value["start"])
        end = date.fromisoformat(value["end"])
    except (KeyError, TypeError, ValueError) as exc:
        raise CalculationError("INVALID_PERIOD") from exc
    if value.get("frequency") not in {"weekly", "biweekly", "monthly"} or end < start:
        raise CalculationError("INVALID_PERIOD")


def _earning_amount(earning: dict[str, Any]) -> Decimal:
    if not isinstance(earning, dict):
        raise CalculationError("INVALID_EARNING")
    has_amount = "amount" in earning
    has_quantity = "quantity" in earning and "unit_rate" in earning
    has_partial_quantity = ("quantity" in earning) != ("unit_rate" in earning)
    if has_partial_quantity:
        raise CalculationError("INVALID_QUANTITY")
    if has_amount == has_quantity:
        raise CalculationError("INVALID_EARNING")
    if has_amount:
        return _decimal(earning["amount"], MONEY_PATTERN, "INVALID_MONEY")
    if "quantity" not in earning or "unit_rate" not in earning:
        raise CalculationError("INVALID_EARNING")
    quantity = _decimal(earning["quantity"], QUANTITY_PATTERN, "INVALID_QUANTITY")
    rate = _decimal(earning["unit_rate"], MONEY_PATTERN, "INVALID_MONEY")
    return (quantity * rate).quantize(CENT, rounding=ROUND_HALF_UP)


def _deduction_amount(deduction: dict[str, Any]) -> Decimal:
    if not isinstance(deduction, dict) or "amount" not in deduction:
        raise CalculationError("INVALID_DEDUCTION")
    if deduction.get("tax_treatment") not in {
        "pre_tax",
        "post_tax",
        "externally_calculated_statutory",
    }:
        raise CalculationError("INVALID_DEDUCTION")
    return _decimal(deduction.get("amount"), MONEY_PATTERN, "INVALID_MONEY")


def _check_ids(lines: list[dict[str, Any]]) -> None:
    identifiers = [line.get("id") for line in lines]
    if any(not isinstance(identifier, str) or not identifier for identifier in identifiers):
        raise CalculationError("DUPLICATE_LINE_ID")
    if len(set(identifiers)) != len(identifiers):
        raise CalculationError("DUPLICATE_LINE_ID")


def _allocate(allocation: dict[str, Any]) -> list[dict[str, str]]:
    if not isinstance(allocation, dict):
        raise CalculationError("INVALID_ALLOCATION")
    base = _decimal(allocation.get("allocation_base"), MONEY_PATTERN, "INVALID_MONEY")
    entries = allocation.get("allocations")
    if not isinstance(entries, list) or not entries or any(
        not isinstance(entry, dict) for entry in entries
    ):
        raise CalculationError("INVALID_ALLOCATION")
    identifiers = [entry.get("cost_centre_id") for entry in entries]
    if (
        any(not isinstance(identifier, str) or not identifier for identifier in identifiers)
        or len(set(identifiers)) != len(identifiers)
    ):
        raise CalculationError("INVALID_ALLOCATION")
    if any(
        isinstance(entry.get("basis_points"), bool)
        or not isinstance(entry.get("basis_points"), int)
        or entry["basis_points"] <= 0
        for entry in entries
    ):
        raise CalculationError("INVALID_ALLOCATION")
    if sum(entry["basis_points"] for entry in entries) != 10000:
        raise CalculationError("INVALID_ALLOCATION")

    cents = int(base * 100)
    shares = []
    for entry in entries:
        exact = Decimal(cents * entry["basis_points"]) / Decimal(10000)
        floor = int(exact.to_integral_value(rounding=ROUND_DOWN))
        shares.append(
            {
                "cost_centre_id": entry["cost_centre_id"],
                "cents": floor,
                "remainder": exact - floor,
            }
        )
    residual = cents - sum(share["cents"] for share in shares)
    order = sorted(
        range(len(shares)),
        key=lambda index: (
            -shares[index]["remainder"],
            shares[index]["cost_centre_id"],
        ),
    )
    for index in order[:residual]:
        shares[index]["cents"] += 1
    return [
        {
            "cost_centre_id": share["cost_centre_id"],
            "amount": f"{Decimal(share['cents']) / Decimal(100):.2f}",
        }
        for share in sorted(shares, key=lambda item: item["cost_centre_id"])
    ]


def calculate(case_input: dict[str, Any]) -> dict[str, Any]:
    _period(case_input.get("pay_period", {}))
    earnings = case_input.get("earnings")
    deductions = case_input.get("deductions")
    if not isinstance(earnings, list) or not isinstance(deductions, list):
        raise CalculationError("INVALID_EARNING")

    earning_lines = [
        {"id": line.get("id"), "amount": f"{_earning_amount(line):.2f}"}
        for line in earnings
    ]
    _check_ids(earnings)
    deduction_amounts = [_deduction_amount(line) for line in deductions]
    _check_ids(deductions)
    gross = sum((Decimal(line["amount"]) for line in earning_lines), ZERO)
    deductions_total = sum(deduction_amounts, ZERO)
    if deductions_total > gross:
        raise CalculationError("DEDUCTIONS_EXCEED_GROSS")

    result: dict[str, Any] = {
        "earning_lines": earning_lines,
        "gross": f"{gross:.2f}",
        "deductions_total": f"{deductions_total:.2f}",
        "net": f"{gross - deductions_total:.2f}",
    }
    if "allocation" in case_input:
        result["cost_centre_allocations"] = _allocate(case_input["allocation"])
    return result


with VECTOR_PATH.open(encoding="utf-8") as vector_file:
    VECTORS = json.load(vector_file)


class CalculationVectorTests(unittest.TestCase):
    def test_valid_vectors_match_expected_results(self) -> None:
        for vector in VECTORS["valid_cases"]:
            with self.subTest(vector=vector["id"]):
                self.assertEqual(calculate(vector["input"]), vector["expected"])

    def test_invalid_vectors_return_expected_error(self) -> None:
        for vector in VECTORS["invalid_cases"]:
            with self.subTest(vector=vector["id"]):
                with self.assertRaises(CalculationError) as raised:
                    calculate(vector["input"])
                self.assertEqual(raised.exception.code, vector["error"])


if __name__ == "__main__":
    unittest.main()
