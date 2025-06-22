# SerenityHelp Frontend

AI-Powered Support Center Frontend Application

## Features

- **Dashboard**: View and manage live calls with priority-based sorting
- **Call Management**: Connect calls to human agents or emergency services
- **Risk Assessment**: Real-time risk evaluation for callers
- **Call Transcripts**: View detailed call conversations
- **Responsive Design**: Modern UI built with Tailwind CSS

## Tech Stack

- React 18
- TypeScript
- React Router DOM
- Tailwind CSS
- Lucide React (Icons)
- Vite (Build Tool)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Project Structure

```
frontend/
├── components/
│   ├── Dashboard.tsx          # Main dashboard component
│   ├── CallLogTile.tsx        # Individual call tile component
│   ├── CallDetailsSidebar.tsx # Call details sidebar
│   └── pages/
│       └── CallTransfer.tsx   # Call transfer page
├── utils/
│   └── mockData.ts           # Mock data for calls
├── App.tsx                   # Main app component
├── index.tsx                 # Entry point
├── index.css                 # Global styles with Tailwind
└── package.json             # Dependencies and scripts
```

## Features Overview

### Dashboard
- Displays all calls in a grid layout
- Sorts calls by priority (Emergency > High Priority > Normal > Low Priority)
- Shows active call count
- Click "View Details" to see call information in sidebar
- Click "Connect" to transfer calls to agents

### Call Management
- Emergency calls are automatically connected to 911
- High priority calls can be connected to human agents
- Risk assessment shows percentages for self-harm, homicidal, distress, and psychosis
- Real-time call status tracking

### Call Details
- View complete call transcripts
- See risk assessment metrics
- Access caller information and call summary
- Connect calls directly from the details view

## Styling

The app uses Tailwind CSS for styling with a clean, modern design. The color scheme includes:
- Blue for primary actions and in-progress calls
- Green for connected calls
- Red for emergency calls and high-risk assessments
- Orange for high priority calls
- Gray for low priority and completed calls 