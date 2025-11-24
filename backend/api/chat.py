from fastapi import APIRouter, HTTPException
from backend.agent.models import ChatRequest, ChatResponse
from groq import Groq
import os
import json
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()
api_key = os.getenv("GROQ_API_KEY")
print(f"DEBUG: chat.py loaded. API Key present: {bool(api_key)}")
if api_key:
    client = Groq(api_key=api_key)
    model_name = "llama-3.3-70b-versatile"
else:
    client = None
    model_name = None
from backend.agent.researcher import Researcher
researcher = Researcher()
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not client:
        user_msg = request.message.lower()
        if "research" in user_msg:
            company = user_msg.replace("research", "").strip()
            return ChatResponse(
                message=f"I'll start researching {company} for you.",
                action="research_start",
                data={"company": company}
            )
        return ChatResponse(message="Please provide a Groq API Key to enable natural language understanding.")
    context_str = ""
    if request.context and request.context.get("company_name"):
        context_str = f"""
        **CURRENT CONTEXT:**
        You have already generated a research report for **{request.context['company_name']}**.
        The user might ask follow-up questions to expand the report.
        Current Report Sections: {[s['title'] for s in request.context.get('sections', [])]}
        """
    prompt = f"""
    You are a PROFESSIONAL COMPANY RESEARCH ASSISTANT with GPT-like conversational intelligence.
    {context_str}
    **CORE BEHAVIORS (FOLLOW STRICTLY):**
    1. **New Research:** If user mentions a company (e.g., "Research Tesla"), return 'research_company'.
    2. **Update Report:** If user asks about CURRENT company (e.g., "History?", "Products?"), return 'research_update'. Extract 'topic'.
       - **CRITICAL:** You MUST provide a brief conversational answer AND a follow-up question in 'response_message'.
       - Example: "Tesla was founded in 2003... I've added the full history to the right panel. Would you like to explore their funding or competitors next?"
    3. **Chat:** If unrelated, return 'chat'. Be friendly, smart, insightful. Guide back to research if off-topic.
    **RESPONSE FORMAT:**
    - 'research_company' -> "Initial company research generated on the right panel. Let me know what you'd like to explore further!"
    - 'research_update' -> "[Brief Answer]. I've updated the right panel. [Follow-up Question]"
    - 'chat' -> Conversational response.
    **INPUT:** "{request.message}"
    **OUTPUT FORMAT (JSON ONLY):**
    {{
        "intent": "research_company" | "research_update" | "chat",
        "company": "Company Name" (if research_company),
        "topic": "Topic" (if research_update),
        "response_message": "Response string"
    }}
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400 
        )
        raw_response = response.choices[0].message.content
        print(f"DEBUG: Raw Groq Response: {raw_response}")
        text = raw_response.replace('```json', '').replace('```', '').strip()
        data = json.loads(text)
        intent = data.get("intent")
        if intent == "research_company" and data.get("company"):
            return ChatResponse(
                message=data.get("response_message", "Research generated on the right side."),
                action="research_start",
                data={"company": data.get("company")}
            )
        elif intent == "research_update" and data.get("topic"):
            return ChatResponse(
                message=data.get("response_message", f"{data.get('topic')} added to report."),
                action="research_update",
                data={
                    "company": request.context.get("company_name") if request.context else None,
                    "topic": data.get("topic")
                }
            )
        else:
            return ChatResponse(
                message=data.get("response_message"),
                action="chat"
            )
    except Exception as e:
        print(f"ERROR: Chat processing failed: {e}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            message="I'm having trouble connecting to my brain right now. Please try again.",
            action="chat"
        )