import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { TypingIndicator } from './components/TypingIndicator';
import { Message, ChatState } from './types';
import { Bot } from 'lucide-react';
import './App.css'
import { chatService } from './services';

function App() {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [
      {
        id: '1',
        content: "Hello! I'm AltoTech Assistant, and I'm here to help you! How can I assist you today? I can help you with information about: - Hotels and their facilities - Floors and rooms - Sensor data - Indoor air quality - Life being detection - Power meter readings Please let me know what information you're looking for, and I'll be happy to help!",
        role: 'assistant',
        timestamp: new Date(),
      },
    ],
    isLoading: false,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
    }));

    try {
      // Call the actual API
      const response = await chatService.sendMessage(content);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data, // Use the actual response
        role: 'assistant',
        timestamp: new Date(),
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, botMessage],
        isLoading: false,
      }));
    } catch (error) {
      console.error('Error:', error);
      setChatState(prev => ({
        ...prev,
        isLoading: false,
      }));
    }
  };

  return (
    <div className="mx-auto h-[93vh] p-4">
        {/* Gradient Header */}
        <div 
          className="px-6 py-4 text-center font-bold text-2xl text-gray-800"
          style={{
            background: 'linear-gradient(to bottom, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%)',
          }}
        >
          AltoTech Intelligent Comfort Assistant
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-6 h-[calc(100%-180px)] space-y-6">
          {chatState.messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {chatState.isLoading && (
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                <Bot size={20} className="text-white" />
              </div>
              <TypingIndicator />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-100">
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={chatState.isLoading}
          />
        </div>
      </div>
  );
}

export default App;