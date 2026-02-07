/**
 * API Service Layer
 * 
 * Centralized backend communication.
 * Switch between mock and real data easily.
 */

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export interface DashboardData {
  type: string;
  cards: {
    [key: string]: number;
  };
}

export interface ChatResponse {
  success: boolean;
  data: {
    value?: number;  // The calculated number from insights
    headline?: string;
    analysis?: string;
    action_item?: string;
    sentiment?: 'positive' | 'neutral' | 'negative';
    data?: any;
  };
  errors: string[];
}

/**
 * Fetch dashboard overview data (6 metric cards)
 * 
 * @returns Dashboard data with 6 key metrics
 */
export async function fetchDashboardData(): Promise<DashboardData> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/dashboard/load`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result.data;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    // Return mock data as fallback
    return getMockDashboardData();
  }
}

/**
 * Send a chat query to the backend
 * 
 * @param message User's question
 * @returns Chat response with analysis
 */
export async function sendChatQuery(message: string): Promise<ChatResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_query: message,
        chat_history: [],
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error sending chat query:', error);
    return {
      success: false,
      data: {
        headline: 'Connection Error',
        analysis: 'Unable to connect to the backend. Please check if the API server is running.',
        sentiment: 'neutral',
      },
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

/**
 * Mock dashboard data for development/fallback
 */
function getMockDashboardData(): DashboardData {
  return {
    type: 'dashboard_view',
    cards: {
      internal_arpu: 105.2,
      internal_vip_retention: 0.94,
      internal_revenue: 1500000,
      internal_latency: 45,
      internal_volatility: 12.5,
      internal_churn: 0.04,
    },
  };
}

