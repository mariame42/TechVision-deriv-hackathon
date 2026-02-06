import React from 'react';

import PageHeader from '../../Component/UI/PageHeader/PageHeader';
import ChatContainer from '../../Component/Features/Copilot/ChatContainer';

const CopilotPage: React.FC = () => {
  return (
    <div>
      <PageHeader title="Copilot" />
      <ChatContainer />
    </div>
  );
};

export default CopilotPage;


