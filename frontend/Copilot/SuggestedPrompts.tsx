import React from 'react';
import OutlineButton from '../../UI/Buttons/OutlineButtons';

interface SuggestedPromptsProps {
  onSelectPrompt: (text: string) => void;
}

const SuggestedPrompts: React.FC<SuggestedPromptsProps> = ({ onSelectPrompt }) => {
  return (
    <div className="px-4 pt-3 pb-2 flex flex-wrap gap-2">
      <OutlineButton
        color="blue"
        text="why was [Employee Name] denied?"
        onClick={() => onSelectPrompt('why was [Employee Name] denied?')}
      />
      <OutlineButton
        color="blue"
        text="What does the robot do?"
        onClick={() => onSelectPrompt('What does the robot do?')}
      />
      <OutlineButton
        color="blue"
        text="Summarize yesterday`s access"
        onClick={() => onSelectPrompt('Summarize yesterday`s access')}
      />
      <OutlineButton
        color="blue"
        text="Check the main camera status"
        onClick={() => onSelectPrompt('Check the main camera status')}
      />
    </div>
  );
};

export default SuggestedPrompts;


