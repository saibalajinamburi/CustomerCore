from typing import TypedDict, Optional, List, Annotated
from langgraph.graph.message import add_messages
from src.agent.schemas import TriageOutput

class TicketInput(TypedDict):
    ticket_id: str
    body: str
    customer_id: str
    tenant_id: str
    customer_tier: str

class AgentState(TypedDict):
    # Input
    ticket: TicketInput

    # Populated by each sub-agent
    category: Optional[str]
    priority: Optional[str]
    routing_team: Optional[str]
    sla_breach_risk: Optional[float]
    churn_risk: Optional[float]
    confidence: Optional[float]
    summary: Optional[str]
    suggested_resolution: Optional[str]
    kb_citations: Optional[List[str]]
    recalled_memories: Optional[List[str]]
    incident_detected: Optional[bool]
    hitl_required: Optional[bool]
    hitl_reason: Optional[str]
    models_used: Optional[List[str]]

    # Workflow metadata
    current_step: Optional[str]
    error: Optional[str]
    final_output: Optional[TriageOutput]

    # Messages (for LangGraph message passing)
    messages: Annotated[list, add_messages]
