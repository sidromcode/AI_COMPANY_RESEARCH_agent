from typing import List
from backend.agent.models import AccountPlan, AccountPlanSection, ResearchResult
from groq import Groq
import os
import json
class Planner:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.3-70b-versatile"
        else:
            self.client = None
    def generate_plan(self, company_name: str, research_results: List[ResearchResult]) -> AccountPlan:
        if not self.client:
            return AccountPlan(
                company_name=company_name,
                sections=[
                    AccountPlanSection(title="Error", content="No Groq API Key provided.")
                ]
            )
        context = "\n\n".join([f"Source: {r.source} ({r.url})\nContent: {r.content}" for r in research_results])
        prompt = f"""
        You are a PROFESSIONAL COMPANY RESEARCH ASSISTANT.
        Your goal is to generate a comprehensive research report for {company_name}.
        Use the following REAL-TIME research data to generate the report. 
        Do not hallucinate facts. If the data is missing, state that.
        RESEARCH DATA:
        {context}
        Generate a JSON object with the following structure:
        {{
            "company_name": "{company_name}",
            "sections": [
                {{ "title": "Company Overview", "content": "..." }},
                {{ "title": "Founding & History", "content": "..." }},
                {{ "title": "Products & Services", "content": "..." }},
                {{ "title": "Competitors & Market Share", "content": "..." }},
                {{ "title": "Latest News & Updates", "content": "..." }}
            ]
        }}
        Select the most relevant sections for {company_name} from the following list.
        IMPORTANT: Every company must have DIFFERENT sections. NO fixed 4 domains.
        Choose sections that depend on the company type (tech, automotive, finance, AI, healthcare, etc.).
        Possible Sections (pick only relevant ones):
        - Company Overview
        - Founding & History
        - Vision & Mission
        - Business Model
        - Products & Services
        - Technology Stack (for tech firms)
        - Funding & Valuation (for startups)
        - Competitive Landscape
        - SWOT Analysis (only when relevant)
        - Industry Positioning
        - Recent News / Developments
        - Strategic Opportunities
        - Challenges & Risks
        - Future Outlook
        Return ONLY the JSON.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2500
            )
            text = response.choices[0].message.content
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            text = text.strip()
            try:
                data = json.loads(text)
                return AccountPlan(**data)
            except json.JSONDecodeError:
                print(f"ERROR: JSON Decode Failed. Raw text: {text}")
                return AccountPlan(
                    company_name=company_name,
                    sections=[
                        AccountPlanSection(title="Analysis Result (Raw)", content=text)
                    ]
                )
        except Exception as e:
            print(f"ERROR: Plan generation failed: {e}")
            return AccountPlan(
                company_name=company_name,
                sections=[AccountPlanSection(title="Generation Error", content=str(e))]
            )
    def update_plan(self, current_plan: AccountPlan, research_results: List[ResearchResult], topic: str) -> AccountPlan:
        if not self.client:
            return current_plan
        context = "\n\n".join([f"Source: {r.source} ({r.url})\nContent: {r.content}" for r in research_results])
        prompt = f"""
        You are a PROFESSIONAL COMPANY RESEARCH ASSISTANT.
        You are updating an existing research report for {current_plan.company_name}.
        The user wants to know about: "{topic}".
        EXISTING SECTIONS:
        {[s.title for s in current_plan.sections]}
        NEW RESEARCH DATA:
        {context}
        Generate a JSON object representing the NEW or UPDATED section.
        If the topic fits into an existing section, provide the updated content for that section.
        If it's a new topic, provide a new section title and content.
        Structure:
        {{
            "title": "Section Title",
            "content": "Detailed content..."
        }}
        Return ONLY the JSON.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            text = response.choices[0].message.content
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            text = text.strip()
            try:
                new_section_data = json.loads(text)
                new_section = AccountPlanSection(**new_section_data)
                updated_sections = []
                replaced = False
                for section in current_plan.sections:
                    if section.title.lower() == new_section.title.lower():
                        updated_sections.append(new_section)
                        replaced = True
                    else:
                        updated_sections.append(section)
                if not replaced:
                    updated_sections.append(new_section)
                return AccountPlan(company_name=current_plan.company_name, sections=updated_sections)
            except json.JSONDecodeError:
                 print(f"ERROR: JSON Decode Failed in Update. Raw text: {text}")
                 return current_plan
        except Exception as e:
            print(f"ERROR: Plan update failed: {e}")
            return current_plan