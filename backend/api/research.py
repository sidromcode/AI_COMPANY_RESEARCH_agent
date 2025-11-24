from fastapi import APIRouter
from backend.agent.models import ResearchQuery, ResearchResult
from backend.agent.researcher import Researcher
from typing import List
router = APIRouter()
researcher = Researcher()
@router.post("/", response_model=List[ResearchResult])
async def research_endpoint(query: ResearchQuery):
    results = await researcher.research_company(query.company_name)
    return results