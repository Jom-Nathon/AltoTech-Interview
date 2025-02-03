import React from 'react';
import { Message } from '../types';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isBot = message.role === 'assistant';
  
  return (
    <div className={`flex items-start gap-3 ${isBot ? '' : 'flex-row-reverse'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isBot ? 'bg-blue-600' : 'bg-gray-700'
      }`}>
        {isBot ? <Bot size={18} className="text-white" /> : <User size={18} className="text-white" />}
      </div>
      <div className={`flex flex-col max-w-[75%] ${isBot ? 'items-start' : 'items-end'}`}>
        <div className={`rounded-2xl px-4 py-2 ${
          isBot 
            ? 'bg-gray-100 text-gray-900' 
            : 'bg-blue-600 text-white'
        }`}>
          <p className="text-sm">{message.content}</p>
        </div>
        <span className="text-xs text-gray-500 mt-1">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
}