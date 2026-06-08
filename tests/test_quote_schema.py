from decimal import Decimal

import pytest
from pydantic import ValidationError

from autoquote_roi_engine.schemas.quote import CostBreakdown, NormalizedQuoteLine


def test_normalized_quote_line_computes_source_and_krw_totals() -> None:
    quote = NormalizedQuoteLine(
        item_code=" STD-001 ",
        description="Bracket Assembly",
        vendor_name="Vietnam Tooling Co.",
        currency="usd",
        exchange_rate=Decimal("1380"),
        material_cost=Decimal("10.50"),
        processing_cost=Decimal("5.25"),
        overhead_cost=Decimal("2.00"),
        local_tax=Decimal("1.00"),
        profit_1=Decimal("1.50"),
        profit_2=Decimal("0.75"),
    )

    assert quote.item_code == "STD-001"
    assert quote.currency == "USD"
    assert quote.total_source_cost == Decimal("21.00")
    assert quote.total_krw_cost == Decimal("28980.00")
    assert quote.material_cost_krw == Decimal("14490.00")
    assert quote.local_tax_krw == Decimal("1380.00")
    assert quote.profit_2_krw == Decimal("1035.00")


def test_optional_tax_and_second_profit_default_to_zero() -> None:
    quote = NormalizedQuoteLine(
        item_code="KR-100",
        description="Injection Mold Part",
        vendor_name="Korea Supplier",
        currency="KRW",
        material_cost=Decimal("1000"),
        processing_cost=Decimal("2000"),
        overhead_cost=Decimal("300"),
        profit_1=Decimal("700"),
    )

    assert quote.exchange_rate == Decimal("1.0")
    assert quote.local_tax == Decimal("0")
    assert quote.profit_2 == Decimal("0")
    assert quote.total_source_cost == Decimal("4000")
    assert quote.total_krw_cost == Decimal("4000.0")


def test_cost_breakdown_conversion_keeps_six_category_shape() -> None:
    breakdown = CostBreakdown(
        material_cost=Decimal("1"),
        processing_cost=Decimal("2"),
        overhead_cost=Decimal("3"),
        local_tax=Decimal("4"),
        profit_1=Decimal("5"),
        profit_2=Decimal("6"),
    )

    converted = breakdown.convert(Decimal("10"))

    assert converted.material_cost == Decimal("10")
    assert converted.processing_cost == Decimal("20")
    assert converted.overhead_cost == Decimal("30")
    assert converted.local_tax == Decimal("40")
    assert converted.profit_1 == Decimal("50")
    assert converted.profit_2 == Decimal("60")
    assert converted.total_cost == Decimal("210")


def test_negative_cost_is_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedQuoteLine(
            item_code="ERR-001",
            description="Invalid negative cost",
            vendor_name="Bad Supplier",
            currency="USD",
            material_cost=Decimal("-1"),
        )


def test_empty_metadata_is_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedQuoteLine(
            item_code="   ",
            description="Valid description",
            vendor_name="Valid Supplier",
            currency="KRW",
        )
