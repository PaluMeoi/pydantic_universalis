from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class UploadHistory(BaseModel):
    uploadCountByDay: List[int]


class World(BaseModel):
    count: int
    proportion: float

class UploadCountByWorld(BaseModel):
    pass