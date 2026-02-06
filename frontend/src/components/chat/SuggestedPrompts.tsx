/**
 * SuggestedPrompts Component
 * Shows clickable prompt suggestions for trading analytics
 */

import React from 'react';

interface SuggestedPromptsProps {
  onSelectPrompt: (text: string) => void;
}

const SuggestedPrompts: React.FC<SuggestedPromptsProps> = ({ onSelectPrompt }) => {
  const prompts = [
    'Why did we lose money today?',
    'How is our volatility compared to the market?',
    'What is our current revenue trend?',
    'Analyze our VIP retention rate',
  ];

  return (
    <div className="px-4 pt-3 pb-2 flex flex-wrap gap-2">
      {prompts.map((prompt, index) => (
        <button
          key={index}
          onClick={() => onSelectPrompt(prompt)}
          className="px-3 py-1.5 text-sm bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded-lg border border-gray-600 hover:border-primary-500 transition-colors"
        >
          {prompt}
        </button>
      ))}
    </div>
  );
};

export default SuggestedPrompts;

