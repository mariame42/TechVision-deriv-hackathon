/**
 * InputBox Component
 * User input field with send button
 */

import React, { KeyboardEvent, ChangeEvent } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

interface InputBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (text: string) => void;
  disabled?: boolean;
}

const InputBox: React.FC<InputBoxProps> = ({ 
  value, 
  onChange, 
  onSend, 
  disabled = false 
}) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    onChange('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-700 p-4 bg-gray-800">
      <div className="flex items-center space-x-3">
        <div className="flex-1">
          <input
            type="text"
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="Ask about your trading analytics..."
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
          />
        </div>
        <button
          type="button"
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          className={`
            px-4 py-3 rounded-lg transition-colors
            ${disabled || !value.trim()
              ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700'
            }
          `}
        >
          <PaperAirplaneIcon className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default InputBox;

