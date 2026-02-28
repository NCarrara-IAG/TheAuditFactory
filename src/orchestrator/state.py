from typing import TypedDict, List, Dict, Any, Optional
from src.schemas.models import Finding, Risk, Recommendation, ROIModel

class AuditGraphState(TypedDict):
    """
    Represents the state of an audit as it moves through the LangGraph pipeline.
    """
    audit_id: str
    audit_type: str
    client_context: Dict[str, Any]
    
    # State tracking
    current_phase: str
    errors: List[str]
    
    # Accumulated Data (Outputs from agents)
    findings: List[Finding]
    risks: List[Risk]
    recommendations: List[Recommendation]
    dependencies: List[str]
    
    # Specifics
    scores: Dict[str, float]
    roi_model: Optional[ROIModel]
    
    # Final outputs
    exec_summary: Optional[str]
