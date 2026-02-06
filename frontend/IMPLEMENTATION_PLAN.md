# Frontend Implementation Plan

## Analysis of Existing Files

### What We Have:
1. **Chat Components** (TypeScript/React):
   - `ChatHeader.tsx` - Header with status, avatar, actions
   - `InputBox.tsx` - Input field with send button
   - `MessageList.tsx` - Message display with user/AI bubbles
   - `ChatContainer.tsx` - Main chat logic container
   - `SuggestedPrompts.tsx` - Prompt suggestions

### What Needs to Change:
1. **Path References**: Existing files reference non-existent paths:
   - `../../../../Common/ImagesData.tsx` ❌
   - `../../UI/Chat/...` ❌
   - `../../../Services/copilot.service` ❌
   - `../../Component/UI/...` ❌

2. **Dependencies**: References to external UI libraries (ti-btn, OutlineButton) that may not exist

3. **Integration**: Need to connect to our backend API (`/api/chat/query`)

## Implementation Strategy

### Phase 1: Project Setup
1. Initialize Vite + React + TypeScript project
2. Install and configure Tailwind CSS with dark mode
3. Set up project structure
4. Create `.env` for backend URL

### Phase 2: Refactor Existing Chat Components
1. **Keep & Adapt**:
   - `MessageList.tsx` - Good structure, just fix imports
   - `InputBox.tsx` - Good, just simplify styling
   - `ChatHeader.tsx` - Adapt for trading platform (remove unnecessary buttons)
   - `SuggestedPrompts.tsx` - Adapt prompts for trading analytics

2. **Refactor**:
   - `ChatContainer.tsx` - Connect to our backend API
   - Remove dependencies on non-existent UI libraries
   - Use Tailwind classes instead

### Phase 3: New Components
1. **Layout Components**:
   - `MainLayout.tsx` - Main app layout
   - `Sidebar.tsx` - Navigation sidebar
   - `Topbar.tsx` - Top bar with user profile

2. **Dashboard Components**:
   - `MetricCard.tsx` - Reusable metric card (props: title, value, icon, trendDirection, trendColor)
   - `InsightBanner.tsx` - AI insights display

3. **Chat Components** (refactored):
   - `ChatInterface.tsx` - Wrapper combining ChatContainer + integration

### Phase 4: Pages & Services
1. **Pages**:
   - `DashboardPage.jsx` - Main dashboard with 3 sections

2. **Services**:
   - `api.js` - Backend API integration
     - `fetchDashboardData()` - Mock for now, real later
     - `sendChatQuery(message)` - Connect to `/api/chat/query`

### Phase 5: Dockerization
1. Create `Dockerfile` for React app
2. Update `docker-compose.yml` to include frontend service
3. Configure nginx or serve for production

## File Structure (Final)

```
frontend/
├── public/
├── src/
│   ├── assets/
│   │   └── (images, icons)
│   ├── components/
│   │   ├── layout/
│   │   │   ├── MainLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Topbar.tsx
│   │   ├── dashboard/
│   │   │   ├── MetricCard.tsx
│   │   │   └── InsightBanner.tsx
│   │   └── chat/
│   │       ├── ChatInterface.tsx (new wrapper)
│   │       ├── ChatHeader.tsx (refactored)
│   │       ├── InputBox.tsx (refactored)
│   │       ├── MessageList.tsx (refactored)
│   │       └── SuggestedPrompts.tsx (refactored)
│   ├── pages/
│   │   └── DashboardPage.tsx
│   ├── services/
│   │   └── api.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.example
├── Dockerfile
├── package.json
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
```

## Key Decisions

1. **Keep TypeScript**: Existing files are TS, maintain consistency
2. **Tailwind Only**: Remove dependencies on external UI libraries
3. **Simple Icons**: Use heroicons or similar, not custom icon fonts
4. **Mock First**: Start with mock data, switch to real API easily
5. **Dark Mode**: Trading/financial aesthetic with dark theme

## Next Steps

1. ✅ Analyze existing files (DONE)
2. ⏳ Initialize Vite project
3. ⏳ Set up Tailwind with dark mode
4. ⏳ Refactor chat components
5. ⏳ Create layout components
6. ⏳ Create dashboard components
7. ⏳ Build DashboardPage
8. ⏳ Create API service
9. ⏳ Dockerize
10. ⏳ Update docker-compose.yml

