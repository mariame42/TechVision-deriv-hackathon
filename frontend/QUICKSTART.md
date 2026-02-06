# Frontend Quick Start Guide

## 🚀 Quick Setup (3 Steps)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Create Environment File
```bash
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

### 3. Start Development Server
```bash
npm run dev
```

Visit: **http://localhost:3000**

## 🐳 Docker Setup

### Option A: Full Stack (Backend + Frontend)
```bash
# From project root
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend: http://localhost:8000

### Option B: Frontend Only
```bash
cd frontend
docker build -t trading-frontend .
docker run -p 3000:80 trading-frontend
```

## 📁 Key Files

- `src/App.tsx` - Main app with routing
- `src/pages/DashboardPage.tsx` - Main dashboard page
- `src/services/api.ts` - Backend API integration
- `src/components/dashboard/MetricCard.tsx` - Reusable metric card
- `src/components/chat/ChatInterface.tsx` - Chat component

## 🎨 Features

✅ Dark mode trading aesthetic  
✅ 6 metric cards (Revenue, ARPU, VIP Retention, Latency, Volatility, Churn)  
✅ AI Insights banner  
✅ Interactive chat with backend API  
✅ Responsive design  
✅ Dockerized with nginx  

## 🔧 Troubleshooting

**Port 3000 already in use?**
```bash
# Change port in vite.config.ts or use:
npm run dev -- --port 3001
```

**Backend not connecting?**
- Check `VITE_BACKEND_URL` in `.env`
- Ensure backend is running on port 8000
- Check browser console for CORS errors

**Docker build fails?**
- Ensure `node_modules` is not in the directory (use .dockerignore)
- Check Docker has enough memory allocated

