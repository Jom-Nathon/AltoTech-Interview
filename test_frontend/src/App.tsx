import React, { useState } from 'react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { RoomVisualization } from './components/RoomVisualization';
import type { Message } from './types';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your Hotel Energy Management Assistant. I can help you monitor energy consumption, analyze efficiency, and provide recommendations. What would you like to know?',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);

    // Simulate bot response
    setTimeout(() => {
      const botMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `Based on current readings, the hotel's energy consumption is 450 kWh. This is 15% lower than yesterday's consumption. The HVAC system is operating at optimal efficiency.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <h2 className="text-lg font-semibold text-center text-gray-100">Hotel Energy Assistant</h2>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Room Visualization */}
          <div className="lg:order-2">
            <RoomVisualization />
          </div>

          {/* Chat Messages */}
          <div className="lg:order-1">
            {messages
              .filter(message => message.role === 'assistant')
              .map((message) => (
                <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="p-4 text-gray-400">
                Assistant is thinking...
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Input */}
      <div className="w-full">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        <div className="text-center text-sm text-gray-400 py-2 border-t border-gray-700">
          Powered by Claude 3.5 Sonnet
        </div>
      </div>
    </div>
  );
}

export default App;