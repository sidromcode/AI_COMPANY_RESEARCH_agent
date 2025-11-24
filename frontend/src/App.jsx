import React, { useState, useRef } from 'react';
import axios from 'axios';
import ChatInterface from './components/ChatInterface';
import ResearchVisualizer from './components/ResearchVisualizer';
import AccountPlan from './components/AccountPlan';
import { motion } from 'framer-motion';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome. I am your Professional Company Research Assistant. Which company shall we analyze today?' }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [researchStatus, setResearchStatus] = useState('IDLE');
  const [accountPlan, setAccountPlan] = useState(null);

  const [splitRatio, setSplitRatio] = useState(0.4);
  const containerRef = useRef(null);
  const isDragging = useRef(false);

  const handleMouseDown = (e) => {
    isDragging.current = true;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.body.style.cursor = 'row-resize';
  };

  const handleMouseMove = (e) => {
    if (!isDragging.current || !containerRef.current) return;

    const containerRect = containerRef.current.getBoundingClientRect();
    const relativeY = e.clientY - containerRect.top;
    const newRatio = relativeY / containerRect.height;

    if (newRatio > 0.1 && newRatio < 0.9) {
      setSplitRatio(newRatio);
    }
  };

  const handleMouseUp = () => {
    isDragging.current = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
    document.body.style.cursor = 'default';
  };

  const handleSendMessage = async (text) => {
    const newMessages = [...messages, { role: 'user', content: text }];
    setMessages(newMessages);
    setIsProcessing(true);

    try {
      const chatResponse = await axios.post('http://127.0.0.1:8000/api/chat/', {
        message: text,
        history: newMessages,
        context: accountPlan ? {
          company_name: accountPlan.company_name,
          sections: accountPlan.sections
        } : null
      });

      const { message, action, data } = chatResponse.data;

      const safeMessage = typeof message === 'string' ? message : JSON.stringify(message || "");

      setMessages(prev => [...prev, { role: 'assistant', content: safeMessage }]);

      if (action === 'research_start' && data?.company) {
        await performResearch(data.company);
      } else if (action === 'research_update' && data?.topic) {
        await updateResearch(data.company, data.topic);
      }

    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Connection error. Please ensure the backend is running." }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const performResearch = async (company) => {
    setResearchStatus(`INITIALIZING SCAN: ${company.toUpperCase()}`);

    setTimeout(() => setResearchStatus(`ANALYZING FINANCIAL REPORTS...`), 1500);
    setTimeout(() => setResearchStatus(`MAPPING COMPETITIVE LANDSCAPE...`), 3000);
    setTimeout(() => setResearchStatus(`SYNTHESIZING STRATEGIC INSIGHTS...`), 4500);

    try {
      const planResponse = await axios.post('http://127.0.0.1:8000/api/plan/generate', {
        company_name: company
      });

      setAccountPlan(planResponse.data);
      setResearchStatus('COMPLETED');

    } catch (error) {
      console.error("Research Error:", error);
      setResearchStatus('ERROR');
    }
  };

  const updateResearch = async (company, topic) => {
    setResearchStatus(`RESEARCHING TOPIC: ${topic.toUpperCase()}`);

    try {
      const updateResponse = await axios.post('http://127.0.0.1:8000/api/plan/update', {
        company_name: company,
        current_plan: accountPlan,
        topic: topic
      });

      setAccountPlan(updateResponse.data);
      setResearchStatus('COMPLETED');

    } catch (error) {
      console.error("Update Error:", error);
      setResearchStatus('ERROR');
    }
  };

  return (
    <div className="h-screen w-screen text-slate-200 p-6 flex gap-6 overflow-hidden bg-black/90">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-[400px] h-full flex flex-col border-r border-white/5 bg-black/40 backdrop-blur-2xl"
      >
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          isProcessing={isProcessing}
        />
      </motion.div>

      <div
        ref={containerRef}
        className="flex-1 h-full flex flex-col relative"
      >
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          style={{ height: `${splitRatio * 100}%` }}
          className="glass-panel rounded-t-2xl overflow-hidden relative"
        >
          <ResearchVisualizer status={researchStatus} />
        </motion.div>

        <div
          onMouseDown={handleMouseDown}
          className="h-2 bg-black/50 hover:bg-indigo-500/50 cursor-row-resize flex items-center justify-center transition-colors z-10"
        >
          <div className="w-12 h-1 rounded-full bg-white/20" />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          style={{ height: `${(1 - splitRatio) * 100}%` }}
          className="flex-1 min-h-0 glass-panel rounded-b-2xl overflow-hidden border-t border-white/5"
        >
          <AccountPlan plan={accountPlan} />
        </motion.div>
      </div>
    </div>
  );
}

export default App;