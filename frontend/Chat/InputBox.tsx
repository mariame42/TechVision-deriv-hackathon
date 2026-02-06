/*
- Role: User input
- Text field
- Send button
- Enter key handling
- Sends text → ChatContainer via onSend.
*/

import React, { KeyboardEvent, ChangeEvent } from 'react';
import { Link } from 'react-router-dom';

interface InputBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (text: string) => void;
}

const InputBox: React.FC<InputBoxProps> = ({ value, onChange, onSend }) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
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
    <div className="box-footer">
      <div className="flex items-center space-x-3 rtl:space-x-reverse">
        <div className="hidden sm:flex">
          <Link
            aria-label="anchor"
            className="ti-btn px-2 py-1 text-gray-500 bg-gray-100 focus:ring-gray-500 dark:text-white/70 dark:bg-dark dark:hover:bg-black/20 dark:hover:text-gray-300 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-xl ti ti-paperclip"></i>
          </Link>
          <Link
            aria-label="anchor"
            className="ti-btn px-2 py-1 text-gray-500 bg-gray-100 focus:ring-gray-500 dark:text-white/70 dark:bg-dark dark:hover:bg-black/20 dark:hover:text-gray-300 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-xl ti ti-mood-smile"></i>
          </Link>
        </div>
        <div className="relative w-full">
          <input
            type="text"
            className="p-3 ti-form-input"
            placeholder="Type your message..."
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className="flex">
          <Link
            aria-label="anchor"
            className="hidden sm:block ti-btn px-2 py-1 text-gray-500 bg-gray-100 focus:ring-gray-500 dark:bg-dark dark:text-white/70 dark:hover:bg-black/20 dark:hover:text-gray-300 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-xl ti ti-microphone"></i>
          </Link>
          <button
            type="button"
            aria-label="send"
            className="ti-btn px-2 py-1 ti-btn-primary"
            onClick={handleSend}
          >
            <i className="text-xl ti ti-send"></i>
          </button>
        </div>
      </div>
    </div>
  );
};

export default InputBox;