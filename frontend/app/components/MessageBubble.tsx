import React from 'react';
import { User, Sparkles } from 'lucide-react';

interface MessageBubbleProps {
    role: 'user' | 'assistant';
    content: string;
}

export default function MessageBubble({ role, content }: MessageBubbleProps) {
    const isUser = role === 'user';

    return (
        <div className={`flex w-full mb-6 animate-fade-in ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[85%] md:max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-4`}>

                {/* Avatar */}
                <div className={`
          flex-shrink-0 w-10 h-10 rounded-sm flex items-center justify-center border
          ${isUser
                        ? 'border-indigo-400/50 bg-indigo-900/20 text-indigo-300'
                        : 'border-green-400/50 bg-green-900/20 text-green-300 force-pulse'}
        `}>
                    {isUser ? <User size={20} /> : <Sparkles size={20} />}
                </div>

                {/* Bubble */}
                <div className={`
          relative p-5 rounded-sm border backdrop-blur-md
          ${isUser
                        ? 'border-indigo-500/30 bg-indigo-900/10 text-indigo-100'
                        : 'border-green-500/30 bg-green-900/10 text-green-100 shadow-[0_0_15px_rgba(0,255,65,0.1)]'}
        `}>
                    {/* Decorative corners */}
                    <div className={`absolute top-0 left-0 w-2 h-2 border-t border-l ${isUser ? 'border-indigo-500' : 'border-green-500'}`}></div>
                    <div className={`absolute top-0 right-0 w-2 h-2 border-t border-r ${isUser ? 'border-indigo-500' : 'border-green-500'}`}></div>
                    <div className={`absolute bottom-0 left-0 w-2 h-2 border-b border-l ${isUser ? 'border-indigo-500' : 'border-green-500'}`}></div>
                    <div className={`absolute bottom-0 right-0 w-2 h-2 border-b border-r ${isUser ? 'border-indigo-500' : 'border-green-500'}`}></div>

                    <p className="leading-relaxed whitespace-pre-wrap text-md font-mono tracking-wide">
                        {content}
                    </p>
                </div>
            </div>
        </div>
    );
}
