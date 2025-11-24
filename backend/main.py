from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import chat, research, plan
app = FastAPI(title="Company Research Assistant API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(plan.router, prefix="/api/plan", tags=["plan"])
@app.get("/")
async def root():
    return {"message": "Company Research Assistant API is running"}