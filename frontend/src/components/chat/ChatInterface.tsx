/**
 * ChatInterface Component
 * Main chat container that integrates with backend API
 */

import React, { useState } from 'react';
import ChatHeader from './ChatHeader';
import MessageList, { ChatMessage } from './MessageList';
import InputBox from './InputBox';
import SuggestedPrompts from './SuggestedPrompts';
import { sendChatQuery } from '../../services/api';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (text: string) => {
    const now = new Date();
    const userMessage: ChatMessage = {
      id: `${now.getTime()}-user`,
      sender: 'user',
      text,
      timestamp: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    // Add user message immediately
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API
      const response = await sendChatQuery(text);

      const replyTime = new Date();
      let replyText = '';

      if (response.success && response.data) {
        // Format the response nicely
        const { headline, analysis, action_item } = response.data;
        replyText = headline 
          ? `${headline}\n\n${analysis || ''}${action_item ? `\n\n💡 ${action_item}` : ''}`
          : analysis || 'I received your query, but could not generate a response.';
      } else {
        replyText = response.data?.analysis || 'Sorry, I could not process your query.';
      }

      const copilotMessage: ChatMessage = {
        id: `${replyTime.getTime()}-copilot`,
        sender: 'copilot',
        text: replyText,
        timestamp: replyTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, copilotMessage]);
    } catch (error) {
      const errorTime = new Date();
      const errorMessage: ChatMessage = {
        id: `${errorTime.getTime()}-error`,
        sender: 'copilot',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: errorTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

  const handleClear = () => {
    setMessages([]);
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg flex flex-col h-[600px]">
      <ChatHeader 
        title="AI Trading Analyst" 
        status={isLoading ? 'Thinking...' : 'Online'}
        onClear={messages.length > 0 ? handleClear : undefined}
      />

      {/* Suggested prompts (only show when no messages) */}
      {messages.length === 0 && (
        <SuggestedPrompts onSelectPrompt={handleSuggestionClick} />
      )}

      {/* Scrollable messages area */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <MessageList messages={messages} />
        {isLoading && (
          <div className="px-4 py-2">
            <div className="flex items-center space-x-2 text-gray-400">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
            </div>
          </div>
        )}
      </div>

      <InputBox 
        value={inputValue} 
        onChange={setInputValue} 
        onSend={handleSend}
        disabled={isLoading}
      />
    </div>
  );
};

export default ChatInterface;

