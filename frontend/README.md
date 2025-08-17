# Sentiment Analyzer Frontend

A minimal Next.js application for analyzing sentiment of text using AI.

## Features

- Clean, modern UI with Tailwind CSS
- Text input area for sentiment analysis
- POSTs text to `http://127.0.0.1:8000/sentiment` endpoint
- Displays sentiment label and confidence score
- Built with TypeScript and Next.js App Router

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create environment configuration:
   ```bash
   # Create .env.local file in the frontend directory
   echo "NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000" > .env.local
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

The app uses the following environment variable:

- `NEXT_PUBLIC_API_BASE`: The base URL for your backend API
  - Development: `http://127.0.0.1:8000`
  - Production: `https://your-production-domain.com`

## API Endpoint

The app expects a backend API running at the URL specified in `NEXT_PUBLIC_API_BASE` with the `/sentiment` endpoint that accepts POST requests with the following format:

**Request:**
```json
{
  "text": "Your text to analyze"
}
```

**Response:**
```json
{
  "label": "positive|negative|neutral",
  "confidence": 0.95
}
```

## Development

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks (useState)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint