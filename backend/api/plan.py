from fastapi import APIRouter
from backend.agent.models import AccountPlan, ResearchQuery
from backend.agent.researcher import Researcher
from backend.agent.planner import Planner
router = APIRouter()
researcher = Researcher()
planner = Planner()
@router.post("/generate", response_model=AccountPlan)
async def generate_plan_endpoint(query: ResearchQuery):
    results = await researcher.research_company(query.company_name)
    plan = planner.generate_plan(query.company_name, results)
    return plan
from backend.agent.models import PlanUpdateRequest
@router.post("/update", response_model=AccountPlan)
async def update_plan_endpoint(request: PlanUpdateRequest):
    results = await researcher.research_topic(request.company_name, request.topic)
    updated_plan = planner.update_plan(request.current_plan, results, request.topic)
    return updated_plan