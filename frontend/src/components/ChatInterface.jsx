import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Sparkles, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
export default function ChatInterface({ messages, onSendMessage, isProcessing }) {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        onSendMessage(input);
        setInput('');
    };
    return (
        <div className="flex flex-col h-full bg-black/20 backdrop-blur-xl">
            {}
            {}
            <div className="flex-1 overflow-y-auto px-6 pt-4 pb-6 space-y-8 scrollbar-hide">
                <AnimatePresence>
                    {messages.map((msg, idx) => (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            key={idx}
                            className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                        >
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-indigo-500/20 border border-indigo-500/50' : 'bg-emerald-500/20 border border-emerald-500/50'
                                }`}>
                                {msg.role === 'user' ? <User size={14} className="text-indigo-400" /> : <Sparkles size={14} className="text-emerald-400" />}
                            </div>
                            <div className={`flex-1 max-w-[85%] space-y-1 ${msg.role === 'user' ? 'text-right' : ''}`}>
                                <div className={`text-xs font-medium opacity-50 mb-1 ${msg.role === 'user' ? 'text-indigo-300' : 'text-emerald-300'}`}>
                                    {msg.role === 'user' ? 'YOU' : 'AGENT'}
                                </div>
                                <div className={`text-sm leading-relaxed text-slate-300 ${msg.role === 'user' ? 'bg-indigo-500/10 p-3 rounded-2xl rounded-tr-sm border border-indigo-500/20' : ''
                                    }`}>
                                    {}
                                    {typeof msg.content === 'object' ? JSON.stringify(msg.content) : msg.content}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
                {isProcessing && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex gap-4"
                    >
                        <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/50 flex items-center justify-center shrink-0">
                            <Sparkles size={14} className="text-emerald-400" />
                        </div>
                        <div className="flex items-center gap-1 h-8">
                            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
                            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse delay-75"></span>
                            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse delay-150"></span>
                        </div>
                    </motion.div>
                )}
                <div ref={messagesEndRef} />
            </div>
            {}
            <div className="p-5 border-t border-white/5 bg-white/5">
                <form onSubmit={handleSubmit} className="relative group">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Enter command or query..."
                        className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 pr-12 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isProcessing}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-slate-400 hover:text-indigo-400 disabled:opacity-30 transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}