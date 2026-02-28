from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SourceReference(BaseModel):
    doc_id: str
    section: Optional[str] = None
    snippet: str

class Finding(BaseModel):
    id: str
    category: str
    description: str
    severity: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    sources: List[SourceReference]

class Risk(BaseModel):
    id: str
    title: str
    description: str
    impact: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    probability: str = Field(..., description="LOW, MEDIUM, HIGH")
    mitigations: List[str]
    sources: List[SourceReference]

class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    effort: str = Field(..., description="LOW, MEDIUM, HIGH")
    impact: str = Field(..., description="LOW, MEDIUM, HIGH")
    timeframe: str = Field(..., description="QUICK_WIN, 3_MONTHS, 6_MONTHS, 12_MONTHS")

class ROIModel(BaseModel):
    capex_estimate: float
    opex_estimate: float
    payback_period_months: float
    assumptions: List[str]
