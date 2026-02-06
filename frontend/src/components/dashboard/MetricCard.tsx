import React from 'react';
import { 
  ArrowUpIcon, 
  ArrowDownIcon,
  ChartBarIcon 
} from '@heroicons/react/24/solid';

export interface MetricCardProps {
  title: string;
  value: string | number;
  icon?: React.ComponentType<{ className?: string }>;
  trendDirection?: 'up' | 'down' | 'neutral';
  trendColor?: 'green' | 'red' | 'gray';
  subtitle?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon: Icon = ChartBarIcon,
  trendDirection = 'neutral',
  trendColor = 'gray',
  subtitle,
}) => {
  const trendColors = {
    green: 'text-success',
    red: 'text-danger',
    gray: 'text-gray-400',
  };

  const bgColors = {
    green: 'bg-success/10',
    red: 'bg-danger/10',
    gray: 'bg-gray-700/50',
  };

  const formatValue = (val: string | number): string => {
    if (typeof val === 'number') {
      // Format large numbers
      if (val >= 1000000) {
        return `$${(val / 1000000).toFixed(1)}M`;
      }
      if (val >= 1000) {
        return `$${(val / 1000).toFixed(1)}K`;
      }
      // Format percentages
      if (val < 1 && val > 0) {
        return `${(val * 100).toFixed(1)}%`;
      }
      return val.toString();
    }
    return val;
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-primary-500 transition-colors">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${bgColors[trendColor]}`}>
            <Icon className={`w-6 h-6 ${trendColors[trendColor]}`} />
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-400">{title}</h3>
            {subtitle && (
              <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
            )}
          </div>
        </div>
        
        {trendDirection !== 'neutral' && (
          <div className={`flex items-center space-x-1 ${trendColors[trendColor]}`}>
            {trendDirection === 'up' ? (
              <ArrowUpIcon className="w-4 h-4" />
            ) : (
              <ArrowDownIcon className="w-4 h-4" />
            )}
          </div>
        )}
      </div>

      <div className="mt-2">
        <p className="text-2xl font-bold text-white">{formatValue(value)}</p>
      </div>
    </div>
  );
};

export default MetricCard;

