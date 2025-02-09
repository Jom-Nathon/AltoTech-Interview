import React, { useState, useRef, useEffect } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Focus input on component mount
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    // Re-focus input after sending a message
    if (!disabled && !input) {
      inputRef.current?.focus();
    }
  }, [disabled, input]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700 bg-gray-800">
      <input
        ref={inputRef}
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about energy consumption, efficiency tips, or system status..."
        className="w-full p-3 rounded-lg bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        disabled={disabled}
      />
    </form>
  );
}