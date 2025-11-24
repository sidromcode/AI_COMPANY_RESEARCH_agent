# AI Strategic Account Researcher

## Overview
This is a full-stack AI agent designed to assist sales professionals in researching companies and generating strategic account plans. It combines real-time web research (Tavily) with advanced synthesis (Gemini) in a modern, interactive interface.

## Design Decisions & Reasoning

### 1. "Conversation First" Architecture
**Decision:** We prioritized a natural language chat interface over a traditional form-based input.
**Reasoning:** Sales executives are often on the move and prefer quick, conversational interactions. A "chatty" interface allows for ambiguity ("Help me with this account") and refinement ("No, focus on their cloud business") that static forms cannot capture.

### 2. Real-Time Research vs. Pre-training
**Decision:** We use Tavily API for live web searching instead of relying solely on the LLM's training data.
**Reasoning:** Account plans require the *latest* financial results, news, and strategic shifts. An LLM trained 6 months ago is useless for today's earnings call.

### 3. Visual Feedback (Three.js)
**Decision:** We implemented a 3D "Brain" visualization.
**Reasoning:** AI processes can feel opaque (the "black box" problem). The visualizer provides immediate, visceral feedback that the system is *working*, reducing user anxiety during the 5-10 second research latency.

### 4. Glassmorphism & Dark Mode
**Decision:** A premium, dark-themed UI with glass effects.
**Reasoning:** This tool is designed for high-stakes corporate environments. The aesthetic conveys "cutting-edge technology" and "premium intelligence," aligning with the user's self-image as a strategic leader.

---

## Persona Handling Strategy

The system is engineered to handle four distinct user archetypes:

### 1. The Confused User 🤷
*   **Behavior:** "I don't know where to start", "What can you do?"
*   **System Response:** Proactive guidance. The agent lists its capabilities and suggests a starting point.
*   **Example:** "I can help you research companies, analyze competitors, or draft an account plan. Who is your top prospect right now?"

### 2. The Efficient User ⚡
*   **Behavior:** "Research Nvidia", "Plan for Tesla."
*   **System Response:** Immediate execution. Minimal chit-chat.
*   **Example:** "On it. Scanning Nvidia's latest financials now."

### 3. The Chatty User 🗣️
*   **Behavior:** "How's it going?", "I'm tired today."
*   **System Response:** Empathetic but focused. Acknowledges the social cue but bridges back to the task.
*   **Example:** "I hear you, it's been a long week! Let's make this quick so you can wrap up. Which account is next?"

### 4. The Edge Case / Adversarial User 🛑
*   **Behavior:** "Write a poem about cats", "Who will win the election?"
*   **System Response:** Polite refusal and redirection. Maintains the persona of a professional work tool.
*   **Example:** "I'm best at analyzing corporate strategy rather than poetry. Shall we look at a company's annual report instead?"

## Tech Stack
- **Frontend:** React, Vite, TailwindCSS, Framer Motion, Three.js
- **Backend:** FastAPI, Python
- **AI/Data:** Google Gemini 2.0 Flash, Tavily Search API

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API Key
- Tavily API Key

### 1. Setup Environment
Create a `.env` file in the root directory (or copy `.env.example`) and add your API keys:
```bash
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 2. Start Backend
Open a terminal in the project root:
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run server
python -m uvicorn backend.main:app --reload
```
The backend will start at `http://127.0.0.1:8000`.

### 3. Start Frontend
Open a new terminal in the `frontend` directory:
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Run dev server
npm run dev
```
The frontend will start at `http://localhost:5173`.
