import React, { useState, useEffect } from 'react';
import { Analytics, CrawlerMetrics } from '../types';
import apiService from '../services/api';
import { formatNumber } from '../utils/formatting';

const AnalyticsDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [crawlerMetrics, setCrawlerMetrics] = useState<CrawlerMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const data = await apiService.getAnalytics();
        setAnalytics(data);
        // fetch crawler metrics too
        try {
          const cm = await apiService.getCrawlerMetrics();
          setCrawlerMetrics(cm);
        } catch (e) {
          // ignore crawler metrics failures
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !analytics) {
    return <div className="text-center text-gray-500">Loading analytics...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>;
  }

  if (!analytics) {
    return <div className="text-center text-gray-500">No analytics available</div>;
  }

  const metrics = [
    { label: 'Pages Crawled', value: analytics.pages_crawled, icon: '📄' },
    { label: 'Unique URLs', value: analytics.unique_urls, icon: '🔗' },
    { label: 'Pending URLs', value: analytics.pending_urls, icon: '⏳' },
    { label: 'Failed URLs', value: analytics.failed_urls, icon: '❌' },
    { label: 'Search Queries', value: analytics.search_queries, icon: '🔍' },
    { label: 'Index Size', value: analytics.index_size, icon: '📊' },
  ];

  const crawlerMetricsList = crawlerMetrics
    ? [
        { label: 'Queue Size', value: crawlerMetrics.queue_size, icon: '📥' },
        { label: 'Failed Jobs', value: crawlerMetrics.failed_count, icon: '⚠️' },
        { label: 'Pages Crawled (RL)', value: crawlerMetrics.pages_crawled, icon: '🏁' },
      ]
    : [];

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Analytics Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.concat(crawlerMetricsList).map((metric) => (
          <div key={metric.label} className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{metric.label}</p>
                <p className="text-2xl font-bold text-blue-600">{formatNumber(metric.value)}</p>
              </div>
              <div className="text-3xl">{metric.icon}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 text-xs text-gray-500 text-right">
        Updated at {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
