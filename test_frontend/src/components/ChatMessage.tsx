import React from 'react';
import { Bot } from 'lucide-react';
import type { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className="flex gap-4 p-6 bg-gray-800 border-b border-gray-700">
      <div className="flex-shrink-0">
        <div className="w-8 h-8 rounded-full flex items-center justify-center bg-blue-900 text-blue-300">
          <Bot size={20} />
        </div>
      </div>
      <div className="flex-1">
        <div className="prose prose-invert max-w-none text-gray-100">
          {message.content}
        </div>
      </div>
    </div>
  );
}