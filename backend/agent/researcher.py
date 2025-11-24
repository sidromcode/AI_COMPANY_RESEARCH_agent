import asyncio
import os
from typing import List
from backend.agent.models import ResearchResult
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()
class Researcher:
    def __init__(self):
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        if self.tavily_key:
            self.client = TavilyClient(api_key=self.tavily_key)
        else:
            self.client = None
    async def search(self, query: str, max_results: int = 5) -> List[ResearchResult]:
        """
        Generic search method for any query.
        """
        if not self.client:
            return [
                ResearchResult(
                    source="System",
                    content="Tavily API Key missing. Cannot perform live search.",
                    url="#"
                )
            ]
        print(f"DEBUG: Searching Tavily for: {query}")
        try:
            response = await asyncio.to_thread(
                self.client.search,
                query=query,
                search_depth="advanced",
                max_results=max_results
            )
            results = []
            for result in response.get('results', []):
                results.append(ResearchResult(
                    source=result.get('title', 'Unknown Source'),
                    content=result.get('content', ''),
                    url=result.get('url', '#')
                ))
            return results
        except Exception as e:
            print(f"ERROR: Tavily search failed: {e}")
            return [ResearchResult(source="System", content=f"Search failed: {str(e)}")]
    async def research_company(self, company_name: str) -> List[ResearchResult]:
        """
        Specific research for company analysis.
        """
        query = f"detailed analysis of {company_name} financial performance strategy and competitors 2024 2025"
        return await self.search(query)
    async def research_topic(self, company_name: str, topic: str) -> List[ResearchResult]:
        """
        Targeted research for a specific topic about a company.
        """
        query = f"{company_name} {topic} details analysis 2024 2025"
        return await self.search(query)