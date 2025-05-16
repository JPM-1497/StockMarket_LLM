// frontend/src/components/NavBar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav className="bg-gray-900 text-white px-6 py-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-blue-400">
          Stock Copilot
        </Link>
        <div className="space-x-6">
          <Link to="/" className="hover:text-blue-300">
            Home
          </Link>
          <Link to="/semantic-search" className="hover:text-blue-300">
            Sector Search
          </Link>
          <Link to="/about" className="hover:text-blue-300">
            About
          </Link>
          <Link to="/saved" className="hover:text-blue-300">
            Saved
          </Link>
          <Link to="/chat" className="hover:text-blue-300">
            Chat
          </Link> 
          <Link to="/news" className="hover:text-blue-300">
            News
          </Link>
          <Link to="/news-archive" className="hover:text-blue-300">
            News Archive
          </Link>
          {/* ✅ New Chat Link */}
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
