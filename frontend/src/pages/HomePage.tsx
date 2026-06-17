import React from 'react';
import Hero from '../components/Hero';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Hero />
      <div className="max-w-6xl mx-auto px-4 py-12">
        <AnalyticsDashboard />
      </div>
    </div>
  );
};

export default HomePage;
