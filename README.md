# Solar Proxy API for Vercel

This is a FastAPI-based proxy server for the Upstage AI Solar API, designed to be deployed on Vercel.

## Features

- **Summary Endpoint** (`/summary`): Proxies requests to Solar 1 Mini Chat model for summarization
- **Google Function Endpoint** (`/solar-google-fc`): Proxies requests to Solar Pro model for advanced summarization
- **Rate Limiting**: 10 requests per minute per IP
- **CORS**: Configured to allow all origins
- **Streaming Response**: Supports Server-Sent Events (SSE) for real-time responses

## Setup

### 1. Environment Variables

Set up the following environment variable in your Vercel project:

```
UPSTAGE_API_KEY=your_upstage_api_key_here
```

### 2. Deploy to Vercel

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy the project:
   ```bash
   vercel
   ```

3. Set environment variables in Vercel dashboard or via CLI:
   ```bash
   vercel env add UPSTAGE_API_KEY
   ```

## API Endpoints

### GET /
Returns API status and version information.

### POST /summary
Proxies summarization requests to Solar 1 Mini Chat model.

**Request Headers:**
- `Authorization: Bearer <your_api_key>` (optional, will use default if not provided)

**Request Body:**
```json
{
  "model": "solar-summarizer",
  "messages": [
    {
      "role": "system",
      "content": "Summarize the following text:"
    },
    {
      "role": "user",
      "content": "Your text to summarize here"
    }
  ]
}
```

### POST /solar-google-fc
Proxies summarization requests to Solar Pro model.

**Request Headers:**
- `Authorization: Bearer <your_api_key>` (optional, will use default if not provided)

**Request Body:**
```json
{
  "model": "solar-summarizer",
  "messages": [
    {
      "role": "system",
      "content": "Summarize the following text:"
    },
    {
      "role": "user",
      "content": "Your text to summarize here"
    }
  ]
}
```

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variable:
   ```bash
   export UPSTAGE_API_KEY=your_api_key_here
   ```

3. Run the server:
   ```bash
   uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
   ```

## Rate Limiting

The API implements rate limiting of 10 requests per minute per IP address. If you exceed this limit, you'll receive a 429 status code.

## Error Handling

The API returns appropriate HTTP status codes:
- `400`: Bad Request (missing API key, invalid model, etc.)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error (upstream API errors)

## CORS

The API is configured to allow all origins, methods, and headers for maximum compatibility.

## API Usage:

Once deployed, you can use your endpoints like this:

```bash
# Test the summary endpoint
curl -X POST "https://your-vercel-domain.vercel.app/summary" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "solar-summarizer",
    "messages": [
      {"role": "system", "content": "Summarize the following text:"},
      {"role": "user", "content": "Your text to summarize here"}
    ]
  }'
```
