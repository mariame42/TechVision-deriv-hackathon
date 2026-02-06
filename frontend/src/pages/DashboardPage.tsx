/**
 * DashboardPage Component
 * Main dashboard with 3 sections:
 * A. Domain Health Overview (6 metric cards)
 * B. AI Insights (banner)
 * C. Chatbot (chat interface)
 */

import React, { useEffect, useState } from 'react';
import MetricCard from '../components/dashboard/MetricCard';
import InsightBanner from '../components/dashboard/InsightBanner';
import ChatInterface from '../components/chat/ChatInterface';
import { fetchDashboardData } from '../services/api';
import {
  CurrencyDollarIcon,
  UserGroupIcon,
  ChartBarIcon,
  ClockIcon,
  ArrowPathIcon,
  UserMinusIcon,
} from '@heroicons/react/24/outline';

interface DashboardMetrics {
  internal_arpu?: number;
  internal_vip_retention?: number;
  internal_revenue?: number;
  internal_latency?: number;
  internal_volatility?: number;
  internal_churn?: number;
}

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>({});
  const [insight, setInsight] = useState<{
    headline: string;
    analysis: string;
    sentiment: 'positive' | 'neutral' | 'negative';
  }>({
    headline: 'Welcome to Trading Analytics',
    analysis: 'Loading insights...',
    sentiment: 'neutral',
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await fetchDashboardData();
      
      if (data.cards) {
        setMetrics(data.cards);
        
        // Generate a simple insight based on data
        const revenue = data.cards.internal_revenue || 0;
        const volatility = data.cards.internal_volatility || 0;
        
        if (revenue > 1000000 && volatility < 15) {
          setInsight({
            headline: 'Revenue Stable with Low Volatility',
            analysis: `Revenue stands at $${(revenue / 1000000).toFixed(1)}M with volatility at ${volatility}%. System performance is stable.`,
            sentiment: 'positive',
          });
        } else if (volatility > 15) {
          setInsight({
            headline: 'High Volatility Detected',
            analysis: `Market volatility is elevated at ${volatility}%. Monitor trading patterns closely.`,
            sentiment: 'negative',
          });
        } else {
          setInsight({
            headline: 'System Operating Normally',
            analysis: 'All metrics are within expected ranges. Continue monitoring key indicators.',
            sentiment: 'neutral',
          });
        }
      }
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  // Metric card configurations
  const metricConfigs = [
    {
      key: 'internal_revenue',
      title: 'Revenue',
      icon: CurrencyDollarIcon,
      trendDirection: 'up' as const,
      trendColor: 'green' as const,
      subtitle: 'Total revenue',
    },
    {
      key: 'internal_arpu',
      title: 'ARPU',
      icon: ChartBarIcon,
      trendDirection: 'up' as const,
      trendColor: 'green' as const,
      subtitle: 'Average revenue per user',
    },
    {
      key: 'internal_vip_retention',
      title: 'VIP Retention',
      icon: UserGroupIcon,
      trendDirection: 'up' as const,
      trendColor: 'green' as const,
      subtitle: 'VIP customer retention',
    },
    {
      key: 'internal_latency',
      title: 'Latency',
      icon: ClockIcon,
      trendDirection: 'down' as const,
      trendColor: 'green' as const,
      subtitle: 'Average response time (ms)',
    },
    {
      key: 'internal_volatility',
      title: 'Volatility',
      icon: ArrowPathIcon,
      trendDirection: 'neutral' as const,
      trendColor: 'gray' as const,
      subtitle: 'Market volatility index',
    },
    {
      key: 'internal_churn',
      title: 'Churn Rate',
      icon: UserMinusIcon,
      trendDirection: 'down' as const,
      trendColor: 'green' as const,
      subtitle: 'Customer churn percentage',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Section A: Domain Health Overview */}
      <section>
        <h2 className="text-xl font-semibold text-white mb-4">Domain Health Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {metricConfigs.map((config) => {
            const value = metrics[config.key as keyof DashboardMetrics];
            if (value === undefined) return null;
            
            return (
              <MetricCard
                key={config.key}
                title={config.title}
                value={value}
                icon={config.icon}
                trendDirection={config.trendDirection}
                trendColor={config.trendColor}
                subtitle={config.subtitle}
              />
            );
          })}
        </div>
      </section>

      {/* Section B: AI Insights */}
      <section>
        <h2 className="text-xl font-semibold text-white mb-4">AI Insights</h2>
        <InsightBanner
          headline={insight.headline}
          analysis={insight.analysis}
          sentiment={insight.sentiment}
        />
      </section>

      {/* Section C: Chatbot */}
      <section>
        <h2 className="text-xl font-semibold text-white mb-4">Ask AI Analyst</h2>
        <ChatInterface />
      </section>
    </div>
  );
};

export default DashboardPage;

