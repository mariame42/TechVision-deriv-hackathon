/**
 * ChatHeader Component
 * Header for chat interface with title and status
 */

import React from 'react';
import { SparklesIcon } from '@heroicons/react/24/solid';

interface ChatHeaderProps {
  title?: string;
  status?: string;
  onClear?: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ 
  title = 'AI Assistant',
  status = 'Online',
  onClear 
}) => {
  const statusColor = status.toLowerCase() === 'online' 
    ? 'bg-success' 
    : 'bg-gray-500';

  return (
    <div className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="relative">
          <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
            <SparklesIcon className="w-6 h-6 text-white" />
          </div>
          <span className={`absolute bottom-0 right-0 w-3 h-3 ${statusColor} rounded-full border-2 border-gray-800`} />
        </div>
        <div>
          <h3 className="text-base font-semibold text-white">{title}</h3>
          <p className="text-xs text-gray-400">{status}</p>
        </div>
      </div>
      
      {onClear && (
        <button
          onClick={onClear}
          className="px-3 py-1 text-sm text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
        >
          Clear
        </button>
      )}
    </div>
  );
};

export default ChatHeader;

