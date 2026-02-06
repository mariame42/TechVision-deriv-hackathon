// 3️⃣ MessageList (Chatbox)
//     Role: Shows conversation
//     Displays user + AI messages
//     Scrolls automatically
//     Maps messages
//     Inside it:
//         MessageItem
//         One message (user / AI)
//     Different styles

/*
- Role: present chat messages.
- Pure UI: given a list of messages, render them as user or copilot bubbles.
*/

import React from 'react';

export type ChatSender = 'user' | 'copilot';

export interface ChatMessage {
  id: string;
  sender: ChatSender;     // "user" | "copilot"
  text: string;           // message content
  timestamp: string;      // already formatted, e.g. "08:10 AM"
}

interface MessageListProps {
  messages: ChatMessage[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="flex flex-col gap-0 px-4">
      {messages.map((msg, index) => {
        const isUser = msg.sender === 'user';

        const bubbleClasses = isUser
          ? 'bg-primary text-white border border-primary'
          : 'bg-primary/20 text-primary dark:text-white border border-gray-200 dark:border-white/10';

        const containerClasses = isUser
          ? 'chat-right flex flex-col items-end mr-2 max-w-[80%] self-end'
          : 'chat-left flex flex-col items-start ml-2 max-w-[80%] self-start';

        const timeClasses = isUser
          ? 'text-end text-xs text-gray-500 dark:text-white/70'
          : 'text-start text-xs text-gray-500 dark:text-white/70';

        return (
          <div key={`${msg.id}-${index}`} className={containerClasses}>
            <div className="chat-inner-msg">
              <span className={`p-2 rounded-sm inline-block ${bubbleClasses}`}>
                {msg.text}
              </span>
            </div>
            <p className={timeClasses}>{msg.timestamp}</p>
          </div>
        );
      })}
    </div>
  );
};

export default MessageList;