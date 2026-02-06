/*  Role:
- Manages state and logic
- Stores messages
- Handles API calls
- Passes data to children
- The brain of the chat. */

import React, { useState } from 'react';

import ChatHeader from '../../UI/Chat/ChatHeader';
import MessageList, { ChatMessage } from '../../UI/Chat/MessageList';
import InputBox from '../../UI/Chat/InputBox';
import { sendCopilotMessage } from '../../../Services/copilot.service';
import SuggestedPrompts from './SuggestedPrompts';

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const staticPrompt =
    'You are ExelRobo Copilot, a helpful assistant focused on robotics, access control, and operations. Keep replies concise and friendly.';

  const handleSend = async (text: string) => {
    const now = new Date();
    const newMessage: ChatMessage = {
      id: `${now.getTime()}`,
      sender: 'user',
      text,
      timestamp: now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    // Add user message immediately
    setMessages((prev) => [...prev, newMessage]);

    try {
      const replyText = await sendCopilotMessage(staticPrompt, text);
      const replyTime = new Date();
      const copilotMessage: ChatMessage = {
        id: `${replyTime.getTime()}`,
        sender: 'copilot',
        text: replyText || '...',
        timestamp: replyTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, copilotMessage]);
    } catch (error: any) {
      const status = error?.response?.status;
      const apiMessage =
        error?.response?.data?.message ||
        error?.response?.data?.error ||
        error?.message;

      const errorTime = new Date();
      const errorMessage: ChatMessage = {
        id: `${errorTime.getTime()}`,
        sender: 'copilot',
        text:
          apiMessage
            ? `Sorry, I could not reach the Copilot service. (${status ?? 'error'}: ${apiMessage})`
            : 'Sorry, I could not reach the Copilot service.',
        timestamp: errorTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

  return (
    <div className="box flex flex-col h-[70vh] w-[60%]">
      <ChatHeader title="Copilot" status="online" clearReset={false} />

      {/* Suggested prompts (click to fill the input box) */}
      <SuggestedPrompts onSelectPrompt={handleSuggestionClick} />

      {/* Scrollable messages area */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
      </div>

      <InputBox value={inputValue} onChange={setInputValue} onSend={handleSend} />
    </div>
  );
};

export default ChatContainer;