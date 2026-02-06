# Trading Analytics Platform - Frontend

React + TypeScript + Tailwind CSS frontend for the Trading Analytics Platform.

## Tech Stack

- **Vite** - Fast build tool
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling with dark mode
- **React Router** - Client-side routing
- **Heroicons** - Icon library

## Project Structure

```
src/
├── components/
│   ├── layout/      # MainLayout, Sidebar, Topbar
│   ├── dashboard/   # MetricCard, InsightBanner
│   └── chat/        # ChatInterface, MessageList, InputBox, etc.
├── pages/           # DashboardPage
├── services/         # api.ts - Backend API integration
└── App.tsx          # Main app with routing
```

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

1. **Build stage**: Compiles the React app
2. **Production stage**: Serves with nginx

### Build and Run

```bash
# From project root
docker-compose up frontend --build
```

Or use the full stack:

```bash
docker-compose up --build
```

## Features

- **Dark Mode**: Trading/financial aesthetic with dark theme
- **Responsive Design**: Works on desktop and tablet
- **Real-time Chat**: AI-powered trading analytics chat
- **Dashboard Metrics**: 6 key trading metrics displayed as cards
- **AI Insights**: Automated insights based on metrics

## API Integration

The frontend connects to the backend API at:
- Dashboard Load: `POST /api/dashboard/load`
- Chat Query: `POST /api/chat/query`

See `src/services/api.ts` for implementation details.

## Environment Variables

- `VITE_BACKEND_URL` - Backend API URL (default: `http://localhost:8000`)

For Docker, the backend URL should be `http://localhost:8000` (browser makes requests, not container).

