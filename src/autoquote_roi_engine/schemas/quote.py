"""Quote data models for normalized supplier quotation lines."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


Money = Decimal


class CostBreakdown(BaseModel):
    """Six standard cost categories in a single currency."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "description": (
                "Standardized six-category cost structure. The sum of these "
                "fields is the final calculated cost for the represented currency."
            )
        },
    )

    material_cost: Money = Field(
        default=Decimal("0"),
        ge=0,
        description="Material cost.",
    )
    processing_cost: Money = Field(
        default=Decimal("0"),
        ge=0,
        description="Processing or manufacturing cost.",
    )
    overhead_cost: Money = Field(
        default=Decimal("0"),
        ge=0,
        description="Management, administration, or overhead cost.",
    )
    local_tax: Money = Field(
        default=Decimal("0"),
        ge=0,
        description=(
            "Local tax. Usually zero for Korean VAT-exclusive quotes; used for "
            "Vietnam-specific local tooling or supplier delivery tax when present."
        ),
    )
    profit_1: Money = Field(
        default=Decimal("0"),
        ge=0,
        description="Main supplier margin.",
    )
    profit_2: Money = Field(
        default=Decimal("0"),
        ge=0,
        description="Second vendor or subcontractor margin.",
    )

    @computed_field
    @property
    def total_cost(self) -> Money:
        """Total cost in this breakdown's currency."""

        return (
            self.material_cost
            + self.processing_cost
            + self.overhead_cost
            + self.local_tax
            + self.profit_1
            + self.profit_2
        )

    def convert(self, exchange_rate: Money) -> CostBreakdown:
        """Return the same six-category breakdown converted by exchange rate."""

        rate = Decimal(str(exchange_rate))
        return CostBreakdown(
            material_cost=self.material_cost * rate,
            processing_cost=self.processing_cost * rate,
            overhead_cost=self.overhead_cost * rate,
            local_tax=self.local_tax * rate,
            profit_1=self.profit_1 * rate,
            profit_2=self.profit_2 * rate,
        )


class NormalizedQuoteLine(BaseModel):
    """A supplier quote line mapped to the master material code list."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "description": (
                "Normalized quotation line for LLM structured outputs. All six "
                "cost fields are expressed in the source currency. KRW fields "
                "are computed from exchange_rate."
            )
        },
    )

    STANDARD_COST_FIELDS: ClassVar[tuple[str, ...]] = (
        "material_cost",
        "processing_cost",
        "overhead_cost",
        "local_tax",
        "profit_1",
        "profit_2",
    )

    item_code: str = Field(description="Canonical master material code.")
    description: str = Field(description="Canonical master material description.")
    vendor_name: str = Field(description="Supplier or vendor name.")
    currency: str = Field(
        min_length=3,
        max_length=3,
        description="Source currency ISO code, for example KRW or USD.",
    )
    exchange_rate: Money = Field(
        default=Decimal("1.0"),
        gt=0,
        description="KRW conversion rate applied to the source currency.",
    )

    material_cost: Money = Field(default=Decimal("0"), ge=0)
    processing_cost: Money = Field(default=Decimal("0"), ge=0)
    overhead_cost: Money = Field(default=Decimal("0"), ge=0)
    local_tax: Money = Field(default=Decimal("0"), ge=0)
    profit_1: Money = Field(default=Decimal("0"), ge=0)
    profit_2: Money = Field(default=Decimal("0"), ge=0)

    @field_validator("item_code", "description", "vendor_name", "currency")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        """Trim text fields and reject empty values after trimming."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        """Normalize source currency codes for stable grouping."""

        return value.upper()

    @computed_field
    @property
    def source_breakdown(self) -> CostBreakdown:
        """Six cost categories in the original quote currency."""

        return CostBreakdown(
            material_cost=self.material_cost,
            processing_cost=self.processing_cost,
            overhead_cost=self.overhead_cost,
            local_tax=self.local_tax,
            profit_1=self.profit_1,
            profit_2=self.profit_2,
        )

    @computed_field
    @property
    def krw_breakdown(self) -> CostBreakdown:
        """Six cost categories converted to KRW."""

        return self.source_breakdown.convert(self.exchange_rate)

    @computed_field
    @property
    def total_source_cost(self) -> Money:
        """Final calculated unit cost in the source currency."""

        return self.source_breakdown.total_cost

    @computed_field
    @property
    def total_krw_cost(self) -> Money:
        """Final calculated unit cost converted to KRW."""

        return self.total_source_cost * self.exchange_rate

    @computed_field
    @property
    def material_cost_krw(self) -> Money:
        return self.material_cost * self.exchange_rate

    @computed_field
    @property
    def processing_cost_krw(self) -> Money:
        return self.processing_cost * self.exchange_rate

    @computed_field
    @property
    def overhead_cost_krw(self) -> Money:
        return self.overhead_cost * self.exchange_rate

    @computed_field
    @property
    def local_tax_krw(self) -> Money:
        return self.local_tax * self.exchange_rate

    @computed_field
    @property
    def profit_1_krw(self) -> Money:
        return self.profit_1 * self.exchange_rate

    @computed_field
    @property
    def profit_2_krw(self) -> Money:
        return self.profit_2 * self.exchange_rate


class NormalizedQuoteBatch(BaseModel):
    """A collection of normalized quote lines from one ingestion run."""

    model_config = ConfigDict(extra="forbid")

    quotes: list[NormalizedQuoteLine] = Field(
        default_factory=list,
        description="Normalized supplier quote lines.",
    )
