import React from 'react';
import { UserCircleIcon } from '@heroicons/react/24/outline';

const Topbar: React.FC = () => {
  return (
    <div className="h-16 bg-gray-800 border-b border-gray-700 flex items-center justify-between px-6">
      {/* Left side - can add breadcrumbs or title here */}
      <div className="flex items-center">
        <h2 className="text-lg font-semibold text-white">Dashboard</h2>
      </div>

      {/* Right side - User profile */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-3 cursor-pointer hover:bg-gray-700 rounded-lg px-3 py-2 transition-colors">
          <UserCircleIcon className="w-8 h-8 text-gray-400" />
          <div className="hidden md:block">
            <p className="text-sm font-medium text-white">User</p>
            <p className="text-xs text-gray-400">Admin</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Topbar;

