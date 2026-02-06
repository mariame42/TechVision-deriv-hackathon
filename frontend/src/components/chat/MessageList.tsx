/**
 * MessageList Component
 * Displays chat messages as user or AI bubbles
 */

import React from 'react';

export type ChatSender = 'user' | 'copilot';

export interface ChatMessage {
  id: string;
  sender: ChatSender;
  text: string;
  timestamp: string;
}

interface MessageListProps {
  messages: ChatMessage[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="flex flex-col gap-4 px-4 py-4">
      {messages.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <p>Start a conversation by asking a question</p>
        </div>
      ) : (
        messages.map((msg) => {
          const isUser = msg.sender === 'user';

          return (
            <div
              key={msg.id}
              className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
                <div
                  className={`
                    rounded-lg px-4 py-2
                    ${isUser
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-700 text-gray-100 border border-gray-600'
                    }
                  `}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                </div>
                <p className="text-xs text-gray-500 mt-1 px-1">
                  {msg.timestamp}
                </p>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default MessageList;

