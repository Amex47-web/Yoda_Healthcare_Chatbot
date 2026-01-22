import React from 'react';

export default function LoadingIndicator() {
  return (
    <div className="flex items-center space-x-2 p-4 text-[#00ff41] animate-fade-in font-mono text-sm tracking-widest uppercase">
      <div className="flex space-x-1">
        <div className="w-1.5 h-1.5 bg-[#00ff41] rounded-none animate-pulse" style={{ animationDelay: '0s' }}></div>
        <div className="w-1.5 h-1.5 bg-[#00ff41] rounded-none animate-pulse" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-1.5 h-1.5 bg-[#00ff41] rounded-none animate-pulse" style={{ animationDelay: '0.2s' }}></div>
      </div>
      <span className="opacity-80 drop-shadow-[0_0_5px_rgba(0,255,65,0.8)]">Accessing Archives...</span>
    </div>
  );
}
