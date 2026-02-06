/*  Role:
- UI only
- Title (Copilot / AI Assistant)
- Status (online, typing…)
- Clear / Reset button (optional)
- 👉 No logic here, only display. */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import ALLImages from '../../../../Common/ImagesData.tsx';

interface ChatHeaderProps {
  title: string;          // e.g. "Copilot"
  status: string;         // e.g. "Online", "Typing…"
  clearReset?: boolean;   // show Clear button or not
  onClear?: () => void;   // callback when Clear clicked
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ title, status, clearReset, onClear }) => {
  const [isSearchActive, setIsSearchActive] = useState(false);

  const toggleSearch = () => setIsSearchActive((prev) => !prev);

  const normalizedStatus = status.toLowerCase();
  const statusColorClass =
    normalizedStatus === 'online'
      ? 'bg-success'
      : normalizedStatus === 'typing'
      ? 'bg-warning'
      : 'bg-gray-400';

  return (
    <div className="box-header bg-gray-50 dark:bg-bgdark border border-gray-200 dark:border-white/10 rounded-t-md shadow-sm pb-3">
      <div className="sm:flex justify-between items-center">
        {/* Left: avatar, title, status */}
        <div className="flex items-center space-x-4 rtl:space-x-reverse">
          <div className="flex">
            <Link className="relative inline-block" to="#">
              <img
                className="avatar avatar-sm rounded-full"
                src={ALLImages('jpg58')}
                alt={title}
              />
              <span
                className={`absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full ring-2 ring-white dark:ring-bgdark ${statusColorClass}`}
              />
            </Link>
          </div>
          <div>
            <p className="text-base font-semibold">
              <span className="chatnameperson">{title}</span>
            </p>
            <p className="text-xs text-gray-500 dark:text-white/70">{status}</p>
          </div>
        </div>

        {/* Right: search, actions, optional clear */}
        <div className="flex items-center gap-2 mt-4 sm:mt-0">
          {/* Search */}
          <div className="flex justify-center items-center rounded-sm relative">
            <div className="cursor-pointer search-chat-icon sm:absolute sm:ltr:right-0 sm:rtl:left-0 ti-btn ti-btn-outline rounded-full p-2 border-gray-200 text-gray-500 dark:text-white/70 focus:ring-gray-200 dark:border-white/10 dark:focus:ring-white/10 dark:focus:ring-offset-white/10">
              <input
                type="search"
                className={`search-chat-input focus-visible:outline-0 border-0 focus:border-0 focus:shadow-none focus:ring-0 bg-transparent py-0 leading-[0] ${
                  isSearchActive ? 'active' : ''
                }`}
                placeholder="Search"
              />
              <i className="text-base leading-none ti ti-search" onClick={toggleSearch}></i>
            </div>
          </div>

          {/* Call / video / add user */}
          <Link
            aria-label="call"
            className="ti-btn ti-btn-outline rounded-full p-2 border-gray-200 text-gray-500 dark:text-white/70 hover:text-gray-700 hover:bg-gray-100 hover:border-gray-200 focus:ring-gray-200 dark:hover:bg-black/30 dark:border-white/10 dark:hover:border-white/20 dark:focus:ring-white/10 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-base leading-none ti ti-phone-call"></i>
          </Link>
          <Link
            aria-label="video"
            className="ti-btn ti-btn-outline rounded-full p-2 border-gray-200 text-gray-500 dark:text-white/70 hover:text-gray-700 hover:bg-gray-100 hover:border-gray-200 focus:ring-gray-200 dark:hover:bg-black/30 dark:border-white/10 dark:hover:border-white/20 dark:focus:ring-white/10 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-base leading-none ti ti-video"></i>
          </Link>
          <Link
            aria-label="add user"
            className="ti-btn ti-btn-outline rounded-full p-2 border-gray-200 text-gray-500 dark:text-white/70 hover:text-gray-700 hover:bg-gray-100 hover:border-gray-200 focus:ring-gray-200 dark:hover:bg-black/30 dark:border-white/10 dark:hover:border-white/20 dark:focus:ring-white/10 dark:focus:ring-offset-white/10"
            to="#"
          >
            <i className="text-base leading-none ti ti-user-plus"></i>
          </Link>

          {/* Optional Clear / Reset button */}
          {clearReset && (
            <button
              type="button"
              className="ti-btn ti-btn-outline rounded-full px-3 py-1 border-gray-200 text-gray-600 text-xs dark:text-white/70 hover:bg-gray-100 hover:text-gray-800 dark:hover:bg-black/30 dark:border-white/10 dark:hover:border-white/20"
              onClick={onClear}
            >
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;