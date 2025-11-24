from pydantic import BaseModel
from typing import List, Optional, Dict
class Message(BaseModel):
    role: str
    content: str
class ResearchQuery(BaseModel):
    company_name: str
    focus_areas: List[str] = ["financials", "competitors", "strategy"]
class ResearchResult(BaseModel):
    source: str
    content: str
    url: Optional[str] = None
class AccountPlanSection(BaseModel):
    title: str
    content: str
class AccountPlan(BaseModel):
    company_name: str
    sections: List[AccountPlanSection]
class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    context: Optional[dict] = None 
class ChatResponse(BaseModel):
    message: str
    action: Optional[str] = None 
    data: Optional[Dict] = None
class PlanUpdateRequest(BaseModel):
    company_name: str
    current_plan: AccountPlan
    topic: str