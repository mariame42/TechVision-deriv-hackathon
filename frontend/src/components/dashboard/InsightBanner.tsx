import React from 'react';
import { 
  LightBulbIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon 
} from '@heroicons/react/24/outline';

export interface InsightBannerProps {
  headline: string;
  analysis: string;
  sentiment?: 'positive' | 'neutral' | 'negative';
  actionItem?: string;
}

const InsightBanner: React.FC<InsightBannerProps> = ({
  headline,
  analysis,
  sentiment = 'neutral',
  actionItem,
}) => {
  const sentimentConfig = {
    positive: {
      bg: 'bg-success/10',
      border: 'border-success/30',
      icon: CheckCircleIcon,
      iconColor: 'text-success',
    },
    negative: {
      bg: 'bg-danger/10',
      border: 'border-danger/30',
      icon: ExclamationTriangleIcon,
      iconColor: 'text-danger',
    },
    neutral: {
      bg: 'bg-primary/10',
      border: 'border-primary/30',
      icon: InformationCircleIcon,
      iconColor: 'text-primary-400',
    },
  };

  const config = sentimentConfig[sentiment];
  const Icon = config.icon;

  return (
    <div className={`${config.bg} ${config.border} border rounded-lg p-6 mb-6`}>
      <div className="flex items-start space-x-4">
        <div className={`flex-shrink-0 ${config.iconColor}`}>
          <Icon className="w-6 h-6" />
        </div>
        
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-2">{headline}</h3>
          <p className="text-gray-300 mb-3">{analysis}</p>
          
          {actionItem && (
            <div className="mt-4 pt-4 border-t border-gray-700">
              <div className="flex items-start space-x-2">
                <LightBulbIcon className="w-5 h-5 text-warning flex-shrink-0 mt-0.5" />
                <p className="text-sm text-gray-400">
                  <span className="font-medium text-gray-300">Action:</span> {actionItem}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InsightBanner;

