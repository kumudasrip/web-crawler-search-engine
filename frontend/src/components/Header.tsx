import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-800">
          🔍 SearchEngine
        </Link>
        <nav className="flex gap-4">
          <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors">
            Home
          </Link>
          <Link to="/analytics" className="text-gray-600 hover:text-blue-600 transition-colors">
            Analytics
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
