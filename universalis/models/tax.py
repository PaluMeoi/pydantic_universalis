from __future__ import annotations

from pydantic import BaseModel, Field


class TaxRates(BaseModel):
    Limsa_Lominsa: int = Field(..., alias='Limsa Lominsa')
    Gridania: int
    Ul_dah: int = Field(..., alias="Ul'dah")
    Ishgard: int
    Kugane: int
    Crystarium: int
    Old_Sharlayan: int = Field(..., alias='Old Sharlayan')
