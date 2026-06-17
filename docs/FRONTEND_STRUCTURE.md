# Frontend folder structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchBox.tsx           - Search input form
│   │   ├── SearchResultItem.tsx    - Individual result card
│   │   ├── Pagination.tsx          - Pagination controls
│   │   ├── AnalyticsDashboard.tsx  - Analytics metrics
│   │   ├── Header.tsx              - App header/navigation
│   │   └── Hero.tsx                - Landing page hero
│   ├── pages/
│   │   ├── HomePage.tsx            - Landing page
│   │   ├── SearchResultsPage.tsx   - Search results
│   │   └── AnalyticsPage.tsx       - Analytics dashboard
│   ├── services/
│   │   └── api.ts                  - API client service
│   ├── types/
│   │   └── index.ts                - TypeScript types/interfaces
│   ├── utils/
│   │   └── formatting.ts           - Utility functions
│   ├── App.tsx                     - Main App component
│   ├── App.css                     - App styles
│   ├── index.tsx                   - React entry point
│   └── index.css                   - Global styles
├── public/
│   └── (static assets)
├── index.html
├── tsconfig.json                   - TypeScript config
├── tailwind.config.js              - Tailwind config
├── postcss.config.js               - PostCSS config
├── vite.config.ts                  - Vite config
├── package.json
├── .env.example
└── .gitignore
```

## Component Architecture

### Pages
- **HomePage**: Landing page with search box and analytics dashboard
- **SearchResultsPage**: Search results with pagination
- **AnalyticsPage**: Full-page analytics dashboard

### Components
- **SearchBox**: Google-like search input
- **SearchResultItem**: Individual search result card
- **Pagination**: Smart pagination controls
- **AnalyticsDashboard**: Metrics display grid
- **Header**: Navigation header
- **Hero**: Landing page hero section

### Services
- **api.ts**: Centralized API client for all backend calls

### Types
- **index.ts**: TypeScript interfaces for all API responses

### Utils
- **formatting.ts**: Helper functions for text formatting

## Responsive Design

All components use Tailwind CSS and are fully responsive:
- Mobile: 320px+
- Tablet: 768px+
- Desktop: 1024px+

Grid layouts adapt automatically using Tailwind's responsive prefixes.
