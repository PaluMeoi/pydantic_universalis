# generated by datamodel-codegen:
#   filename:  history.json
#   timestamp: 2023-06-29T17:56:27+00:00

from __future__ import annotations

from datetime import datetime
from functools import cache
from typing import List, Optional

from pydantic import BaseModel, Field, computed_field
import numpy as np


class Entry(BaseModel):
    hq: bool
    pricePerUnit: int
    quantity: int
    buyerName: str
    onMannequin: bool
    timestamp: datetime
    worldName: Optional[str] = None
    worldID: Optional[int] = None


class History(BaseModel):
    itemID: int
    worldID: Optional[int] = None
    lastUploadTime: datetime
    entries: List[Entry]
    stackSizeHistogram: dict[str | int, int]
    stackSizeHistogramNQ: dict[str | int, int]
    stackSizeHistogramHQ: dict[str | int, int]
    regularSaleVelocity: float
    nqSaleVelocity: float
    hqSaleVelocity: float
    worldName: Optional[str] = None
    dcName: Optional[str] = None
    regionName: Optional[str] = None

    @computed_field
    @property
    def averagePrice(self) -> float:
        all_prices = [e.pricePerUnit for e in self.entries]
        return float(np.mean(all_prices)) if len(all_prices) > 0 else 0.0

    @computed_field
    @property
    def averagePriceNQ(self) -> float:
        all_prices = [e.pricePerUnit for e in self.entries if not e.hq]
        return float(np.mean(all_prices)) if len(all_prices) > 0 else 0.0


    @computed_field
    @property
    def averagePriceHQ(self) -> float:
        all_prices = [e.pricePerUnit for e in self.entries if e.hq]
        return float(np.mean(all_prices)) if len(all_prices) > 0 else 0.0

    @computed_field
    @property
    def medianPrice(self) -> float:
        return float(np.median([e.pricePerUnit for e in self.entries]))

    @computed_field
    @property
    def minPrice(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries]
        return int(min(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def minPriceNQ(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries if not e.hq]
        return int(min(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def minPriceHQ(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries if e.hq]
        return int(min(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def maxPrice(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries]
        return int(max(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def maxPriceNQ(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries if not e.hq]
        return int(max(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def maxPriceHQ(self) -> int:
        all_prices = [e.pricePerUnit for e in self.entries if e.hq]
        return int(max(all_prices)) if len(all_prices) > 0 else 0

    @computed_field
    @property
    def volumeUnits(self) -> int:
        return sum(e.quantity for e in self.entries)

    @computed_field
    @property
    def volumeUnitsNQ(self) -> int:
        return sum(e.quantity for e in self.entries if not e.hq)

    @computed_field
    @property
    def volumeUnitsHQ(self) -> int:
        return sum(e.quantity for e in self.entries if e.hq)

    @computed_field
    @property
    def volumeGil(self) -> int:
        return sum(e.pricePerUnit * e.quantity for e in self.entries)

    @computed_field
    @property
    def volumeGilNQ(self) -> int:
        return sum(e.pricePerUnit * e.quantity for e in self.entries if not e.hq)

    @computed_field
    @property
    def volumeGilHQ(self) -> int:
        return sum(e.pricePerUnit * e.quantity for e in self.entries if e.hq)


class MultiHistory(BaseModel):
    itemIDs: list[int]
    items: dict[int, History]
    worldID: Optional[int] = None
    dcName: Optional[str] = None
    regionName: Optional[str] = None
    unresolvedItems: Optional[list[int]] = []
    worldName: Optional[str] = None
