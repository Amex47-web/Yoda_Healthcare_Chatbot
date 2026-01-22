"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, AlertTriangle, Terminal } from 'lucide-react';
import MessageBubble from './MessageBubble';
import LoadingIndicator from './LoadingIndicator';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: "Systems Online. Galactic Archives Accessed. \n\nGreetings. How may I be of assistance to your journey?" }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [userId, setUserId] = useState<string>('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        // Initialize User ID
        let storedId = localStorage.getItem('jedi_user_id');
        if (!storedId) {
            storedId = crypto.randomUUID();
            localStorage.setItem('jedi_user_id', storedId);
        }
        setUserId(storedId);

        scrollToBottom();
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            // Connect to FastAPI backend
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userMsg,
                    user_id: userId
                }),
            });

            if (!response.ok) {
                throw new Error('Disturbance in the Force (Network Error)');
            }

            const data = await response.json();
            const botReply = data.reply;

            setMessages(prev => [...prev, { role: 'assistant', content: botReply }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', content: "CONNECTION LOST. Signal intercepted. Attempt retry." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-5xl mx-auto p-2 pt-20 md:p-8 md:pt-24 relative z-10 font-mono">

            {/* Holographic Container */}
            <div className="flex-1 flex flex-col bg-black/40 backdrop-blur-sm border border-cyan-800/50 rounded-lg shadow-[0_0_30px_rgba(0,229,255,0.1)] overflow-hidden relative">

                {/* Top Bar Decoration */}
                <div className="h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-50 shrink-0"></div>

                {/* Header */}
                <header className="flex items-center justify-between px-6 py-4 border-b border-cyan-800 bg-black/90 backdrop-blur-xl z-20 shrink-0">
                    <div className="flex items-center gap-3">
                        <Terminal size={24} className="text-cyan-400" />
                        <h1 className="text-2xl font-bold tracking-widest text-cyan-400 uppercase drop-shadow-[0_0_8px_rgba(0,229,255,0.6)]">
                            Yoda healthcare chatbot
                        </h1>
                    </div>
                    <div className="flex flex-col items-end">
                        <div className="text-[10px] text-cyan-600 tracking-[0.2em] uppercase">Secure Channel</div>
                        <div className="flex items-center gap-1 text-[10px] text-yellow-600">
                            <AlertTriangle size={10} />
                            <span>IP Disclaimer Active</span>
                        </div>
                    </div>
                </header>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 min-h-0 custom-scrollbar bg-[url('/grid.png')] bg-repeat opacity-95">

                    <div className="relative z-10">
                        {messages.map((msg, idx) => (
                            <MessageBubble key={idx} role={msg.role} content={msg.content} />
                        ))}
                        {isLoading && <LoadingIndicator />}
                        <div ref={messagesEndRef} />
                    </div>
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-cyan-900/50 bg-black/40 backdrop-blur-md">
                    <div className="relative flex items-center gap-3 bg-cyan-950/20 p-2 rounded border border-cyan-800/30 focus-within:border-cyan-500/80 focus-within:shadow-[0_0_15px_rgba(0,229,255,0.2)] transition-all duration-300">
                        <input
                            type="text"
                            className="flex-1 bg-transparent text-cyan-100 placeholder-cyan-800 px-4 py-3 outline-none font-mono tracking-wide"
                            placeholder="Enter transmission data..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isLoading}
                            autoFocus
                        />
                        <button
                            onClick={handleSend}
                            disabled={isLoading || !input.trim()}
                            className={`
                p-3 rounded-none flex items-center justify-center transition-all border
                ${isLoading || !input.trim()
                                    ? 'border-cyan-900 text-cyan-900 cursor-not-allowed'
                                    : 'border-cyan-500 bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 hover:shadow-[0_0_10px_rgba(0,229,255,0.4)]'}
              `}
                        >
                            <Send size={18} />
                        </button>
                    </div>
                    <div className="flex justify-between mt-2 text-[9px] text-cyan-800 uppercase tracking-widest">
                        <span>System: Online</span>
                        <span>Encrypted: True</span>
                        <span>Groq: Active</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
