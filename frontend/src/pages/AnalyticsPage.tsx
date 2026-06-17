import React from 'react';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

const AnalyticsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8">Analytics Dashboard</h1>
        <AnalyticsDashboard />
      </div>
    </div>
  );
};

export default AnalyticsPage;
