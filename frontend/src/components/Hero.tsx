import React from 'react';
import SearchBox from './SearchBox';

const Hero: React.FC = () => {
  return (
    <div className="bg-gradient-to-b from-blue-50 to-white py-20 px-4 text-center">
      <h1 className="text-5xl font-bold text-gray-900 mb-4">🔍 SearchEngine</h1>
      <p className="text-xl text-gray-600 mb-8">Distributed web crawler & search engine</p>
      <SearchBox />
      <p className="text-sm text-gray-500 mt-6">
        Powered by TF-IDF ranking • Built with Python + React
      </p>
    </div>
  );
};

export default Hero;
