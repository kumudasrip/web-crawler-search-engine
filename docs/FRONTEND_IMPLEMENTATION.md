# Phase 6 — React Frontend

Complete production-ready React + TypeScript frontend with search UI and analytics dashboard.

## What Was Built

### Pages (3 total)
- **HomePage** — Landing page with search hero and analytics dashboard
- **SearchResultsPage** — Search results with pagination and result cards
- **AnalyticsPage** — Full-page analytics dashboard

### Components (6 total)
- **SearchBox** — Google-like search input with form submission
- **SearchResultItem** — Individual search result card with title, URL, snippet, score
- **Pagination** — Smart pagination with prev/next and page numbers
- **AnalyticsDashboard** — 6-metric grid dashboard with auto-refresh
- **Header** — Navigation header with logo and links
- **Hero** — Landing page hero section

### Services & Types
- **api.ts** — Centralized API client for all backend calls
- **types/index.ts** — TypeScript interfaces for all API responses
- **utils/formatting.ts** — Helper functions (formatting, truncating, etc.)

### Configuration
- **vite.config.ts** — Vite dev server & build config
- **tailwind.config.js** — Tailwind CSS customization
- **postcss.config.js** — PostCSS for Tailwind
- **tsconfig.json** — TypeScript strict mode config
- **index.html** — HTML entry point

## Key Features

✅ **Google-like search** — Clean search box on landing page  
✅ **Search results** — Paginated results with relevance scores  
✅ **Pagination** — Smart pagination with ellipsis  
✅ **Live analytics** — 6 metrics refreshing every 30 seconds  
✅ **Responsive design** — Mobile, tablet, desktop layouts  
✅ **TailwindCSS** — Utility-first styling  
✅ **TypeScript** — Full type safety  
✅ **React Router** — Client-side routing  
✅ **Vite** — Fast development & build  

## File Structure

```
frontend/
├── src/
│   ├── components/        ← Reusable UI components
│   ├── pages/             ← Page components
│   ├── services/          ← API client
│   ├── types/             ← TypeScript interfaces
│   ├── utils/             ← Helper functions
│   ├── App.tsx            ← Main app with routing
│   └── index.tsx          ← React entry point
├── public/                ← Static assets
├── index.html             ← HTML template
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── package.json
```

## Technologies

| Tech | Purpose |
|------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| React Router 6 | Client-side routing |
| TailwindCSS | Styling |
| Vite | Dev server & bundler |

## Getting Started

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Configure API endpoint
```bash
cp .env.example .env.local
# Edit .env.local to set REACT_APP_API_URL if needed
```

### 3. Run dev server
```bash
npm run dev
```

Visit http://localhost:5173

### 4. Build for production
```bash
npm run build
```

Output goes to `dist/` folder.

## Component Usage Examples

### SearchBox
```tsx
<SearchBox 
  initialQuery="machine learning"
  onSearch={(query) => console.log(query)}
/>
```

### Pagination
```tsx
<Pagination
  currentPage={1}
  totalResults={100}
  resultsPerPage={10}
  onPageChange={(page) => console.log(page)}
/>
```

### AnalyticsDashboard
```tsx
<AnalyticsDashboard />
```

Auto-fetches analytics and refreshes every 30 seconds.

## API Integration

All API calls go through `services/api.ts`:

```typescript
import apiService from '../services/api';

// Search
const results = await apiService.search("python", 10, 0);

// Get page
const page = await apiService.getPage(1);

// Analytics
const stats = await apiService.getAnalytics();

// Crawl
const response = await apiService.startCrawl({
  seed_urls: ["https://example.com"],
  max_depth: 2,
  max_pages: 100
});
```

## Styling

Uses TailwindCSS utility classes throughout:

```tsx
<div className="max-w-4xl mx-auto px-4 py-8">
  <h1 className="text-4xl font-bold mb-6">Search Results</h1>
</div>
```

Responsive breakpoints:
- `sm:` — 640px+
- `md:` — 768px+
- `lg:` — 1024px+
- `xl:` — 1280px+

## Type Safety

Full TypeScript support with interfaces:

```typescript
interface SearchResult {
  page_id: number;
  title: string;
  url: string;
  snippet: string;
  score: number;
}
```

## Responsive Design

All components are mobile-first:

```tsx
{/* Grid: 1 col on mobile, 2 on tablet, 3 on desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  ...
</div>
```

## Routing

React Router handles all navigation:

```
/              → HomePage (search + analytics)
/search?q=...  → SearchResultsPage (results)
/analytics     → AnalyticsPage (full dashboard)
```

## Environment Variables

Create `.env.local`:
```
REACT_APP_API_URL=http://localhost:8000/api
```

## TypeScript Strict Mode

Enabled for maximum type safety:
- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUnusedLocals: true`

## Production Build

```bash
npm run build
```

Outputs optimized bundle to `dist/`:
- Minified CSS/JS
- Tree-shaking applied
- Source maps included

## Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Netlify
```bash
netlify deploy --prod --dir=dist
```

### Docker
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## Performance

- **Lazy loading**: Components load on route change
- **Memoization**: Prevent unnecessary re-renders
- **API caching**: Results cached per query
- **Image optimization**: SVG icons used

## Accessibility

- Semantic HTML5 elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliant

## Code Quality

- TypeScript strict mode
- ESLint ready (add eslint-plugin-react)
- Prettier formatting (add prettier)

## Next Steps

1. Deploy backend to Render/Railway
2. Deploy frontend to Vercel
3. Add authentication (optional)
4. Add search suggestions API
5. Add advanced search filters
