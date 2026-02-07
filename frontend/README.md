# Trading Analytics Platform - Frontend

React + TypeScript + Tailwind CSS frontend for the Trading Analytics Platform.

## Tech Stack

- **Vite** - Fast build tool and dev server
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling with dark mode
- **React Router** - Client-side routing
- **Heroicons** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/           # Layout components
│   │   │   ├── MainLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Topbar.tsx
│   │   ├── dashboard/       # Dashboard components
│   │   │   ├── MetricCard.tsx
│   │   │   └── InsightBanner.tsx
│   │   └── chat/            # Chat components
│   │       ├── ChatInterface.tsx
│   │       ├── ChatHeader.tsx
│   │       ├── MessageList.tsx
│   │       ├── InputBox.tsx
│   │       └── SuggestedPrompts.tsx
│   ├── pages/               # Page components
│   │   └── DashboardPage.tsx
│   ├── services/            # API integration
│   │   └── api.ts           # Backend API client
│   ├── App.tsx              # Main app with routing
│   └── main.tsx             # Entry point
├── Dockerfile               # Multi-stage build with Nginx
├── nginx.conf              # Nginx configuration
├── package.json             # Dependencies
└── README.md               # This file
```

## Features

- **Dark Mode UI**: Trading/financial aesthetic with dark theme
- **Responsive Design**: Works on desktop and tablet
- **Real-time Dashboard**: 
  - 6 key trading metrics displayed as cards
  - Auto-refresh every 30 seconds
  - Manual refresh button
- **AI Chat Interface**: 
  - Natural language queries
  - Displays insight results with:
    - Headline (insight ID and name)
    - Calculated value
    - Analysis text
    - Action items
  - Suggested prompts for quick queries
- **AI Insights Banner**: Automated insights based on metrics with sentiment indicators

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   # Create .env file
   echo "VITE_BACKEND_URL=http://localhost:8000" > .env
   ```

   Or copy from example:
   ```bash
   cp .env.example .env
   # Edit .env and set VITE_BACKEND_URL
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Docker

The frontend is dockerized using a multi-stage build:

1. **Build stage**: Compiles the React app with Vite
2. **Production stage**: Serves static files with nginx

### Build and Run

```bash
# From project root
docker-compose up frontend --build
```

Or use the full stack (backend + frontend):

```bash
docker-compose up --build
```

The frontend will be available at `http://localhost:3000`

## API Integration

The frontend connects to the backend API at the URL specified in `VITE_BACKEND_URL`.

### Endpoints

#### Dashboard Load
- **Method**: `POST`
- **URL**: `/api/dashboard/load`
- **Request**: `{}`
- **Response**: 
  ```typescript
  {
    success: boolean;
    data: {
      type: string;
      cards: {
        [key: string]: number;
      };
    };
  }
  ```

#### Chat Query
- **Method**: `POST`
- **URL**: `/api/chat/query`
- **Request**: 
  ```typescript
  {
    user_query: string;
    chat_history: any[];
  }
  ```
- **Response**: 
  ```typescript
  {
    success: boolean;
    data: {
      value?: number;           // Calculated numeric result
      headline?: string;         // Insight headline
      analysis?: string;         // Analysis text
      action_item?: string;      // Action item
      sentiment?: 'positive' | 'neutral' | 'negative';
      data?: any;               // Raw data for debugging
    };
    errors: string[];
  }
  ```

### Implementation

See `src/services/api.ts` for the complete API client implementation with:
- TypeScript interfaces for type safety
- Error handling with fallback to mock data
- Environment variable configuration

## Environment Variables

- `VITE_BACKEND_URL` - Backend API URL (default: `http://localhost:8000`)

**Note**: For Docker, the backend URL should be `http://localhost:8000` because the browser makes requests from the host machine, not from within the container.

## Component Details

### DashboardPage
- Displays 6 metric cards (revenue, volatility, churn, etc.)
- Shows AI insights banner with sentiment
- Includes chat interface for queries
- Auto-refreshes every 30 seconds

### ChatInterface
- Message list with user and copilot messages
- Input box with send button
- Suggested prompts when no messages
- Displays full response: headline, value, analysis, action item

### MetricCard
- Displays metric name and value
- Color-coded based on metric type
- Responsive grid layout

### InsightBanner
- Shows insight headline and analysis
- Sentiment indicator (positive/neutral/negative)
- Auto-updates with dashboard refresh

## Styling

The app uses Tailwind CSS with a custom dark theme:
- Dark gray backgrounds (`gray-800`, `gray-900`)
- Accent colors for metrics (green, blue, red, etc.)
- Smooth transitions and hover effects
- Custom scrollbar styling

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Troubleshooting

### Backend Connection Issues
- Verify `VITE_BACKEND_URL` is correct in `.env`
- Check that backend is running on the specified port
- Check browser console for CORS errors

### Build Issues
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

### Docker Issues
- Ensure port 3000 is not in use
- Check Docker logs: `docker-compose logs frontend`
- Rebuild if needed: `docker-compose up frontend --build --force-recreate`
