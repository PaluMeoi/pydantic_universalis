# generated by datamodel-codegen:
#   filename:  all.json
#   timestamp: 2023-06-29T16:28:26+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from datetime import datetime


class MateriaItem(BaseModel):
    slotID: int
    materiaID: int


class Listing(BaseModel):
    lastReviewTime: Optional[datetime] = None
    pricePerUnit: Optional[int] = None
    quantity: Optional[int] = None
    stainID: Optional[int] = None
    creatorName: Optional[str] = None
    creatorID: Optional[str] = None
    hq: Optional[bool] = None
    isCrafted: Optional[bool] = None
    listingID: Optional[str] = None
    materia: List[MateriaItem] = None
    onMannequin: Optional[bool] = None
    retainerCity: Optional[int] = None
    retainerID: Optional[str] = None
    retainerName: Optional[str] = None
    sellerID: Optional[str] = None
    total: Optional[int] = None
    worldName: Optional[str] = None
    worldID: Optional[int] = None


class RecentHistoryItem(BaseModel):
    hq: Optional[bool] = None
    pricePerUnit: Optional[int] = None
    quantity: Optional[int] = None
    timestamp: Optional[datetime] = None
    onMannequin: Optional[bool] = None
    buyerName: Optional[str] = None
    total: Optional[int] = None
    worldName: Optional[str] = None
    worldID: Optional[int] = None


class Current(BaseModel):
    itemID: Optional[int] = None
    worldID: Optional[int] = None
    lastUploadTime: Optional[datetime] = None
    listings: Optional[List[Listing]] = None
    recentHistory: Optional[List[RecentHistoryItem]] = None
    currentAveragePrice: Optional[float] = None
    currentAveragePriceNQ: Optional[float] = None
    currentAveragePriceHQ: Optional[float] = None
    regularSaleVelocity: Optional[float] = None
    nqSaleVelocity: Optional[float] = None
    hqSaleVelocity: Optional[float] = None
    averagePrice: Optional[float] = None
    averagePriceNQ: Optional[float] = None
    averagePriceHQ: Optional[float] = None
    minPrice: Optional[int] = None
    minPriceNQ: Optional[int] = None
    minPriceHQ: Optional[int] = None
    maxPrice: Optional[int] = None
    maxPriceNQ: Optional[int] = None
    maxPriceHQ: Optional[int] = None
    stackSizeHistogram: Optional[dict[int, int]] = None
    stackSizeHistogramNQ: Optional[dict[int, int]] = None
    stackSizeHistogramHQ: Optional[dict[int, int]] = None
    worldName: Optional[str] = None
    dcName: Optional[str] = None
    worldUploadTimes: Optional[dict[str, datetime]] = None
    regionName: Optional[str] = None


class MultiCurrent(BaseModel):
    itemIDs: list[int]
    items: dict[int, Current]
    worldID: Optional[int] = None
    dcName: Optional[str] = None
    regionName: Optional[str] = None
    unresolvedItems: Optional[list[int]] = None
    worldName: Optional[str] = None
