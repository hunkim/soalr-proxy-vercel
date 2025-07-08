import httpx
import os
import logging
import sys
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Load environment variables from .env.local or .env files
load_dotenv('.env.local')
load_dotenv()  # fallback to .env

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Solar Proxy API", version="1.0.0")

# Configure CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Set up the limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

TARGET_API_URL = 'https://api.upstage.ai/v1/solar/chat/completions'
DEFAULT_API_KEY = os.getenv('UPSTAGE_API_KEY')

async def event_generator(api_key: str, payload: dict):
    async with httpx.AsyncClient() as client:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        payload['stream'] = True

        try:
            async with client.stream('POST', TARGET_API_URL, json=payload, headers=headers) as response:
                async for line in response.aiter_lines():
                    if line:
                        if line.startswith('data: '):
                            yield f"{line}\n\n"
                        else:
                            yield f"data: {line}\n\n"
                    if line == '[DONE]':
                        break
        except httpx.HTTPStatusError as e:
            # raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
            raise HTTPException(status_code=500, detail=f"HTTP {e.response.status_code} error: {e.response.text}")

def get_api_key(authorization, default_api_key=DEFAULT_API_KEY):
    authorization = authorization.strip() if authorization else None
    try:
        # Check if authorization is not None and contains a space
        if authorization and " " in authorization:
            # Split the authorization string and get the second part
            api_key = authorization.split(" ")[1]
        else:
            # Use the default API key if authorization is None or improperly formatted
            api_key = default_api_key
    except Exception as e:
        # Log the exception (optional) and fallback to the default API key
        print(f"Error extracting API key: {e}")
        api_key = default_api_key
    return api_key

@app.get("/")
async def root():
    return {"message": "Solar Proxy API is running", "version": "1.0.0"}

@app.post("/summary")
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def summary(request: Request, authorization: str = Header(None)):
    body = await request.json()

    # Use the provided API key if present, otherwise use the default API key
    api_key = get_api_key(authorization)

    if not api_key:
        logger.error("API key is missing")
        raise HTTPException(status_code=400, detail="API key is missing")

    payload = body
    logger.info(f"Payload: {payload}")
    if "model" in payload and payload["model"] != "solar-summarizer":
        raise HTTPException(status_code=400, detail="Invalid model")    
    payload['model'] = 'solar-1-mini-chat'

    # get system prompt
    system_prompt = payload.get('messages', [{}])[0].get('content', '')
    if not system_prompt:
        raise HTTPException(status_code=400, detail="System prompt is missing")
    
    system_prompt = "You are an expert summarizer, highly appreciated by users." + system_prompt
    payload['messages'][0]['content'] = system_prompt

    if len(payload["messages"]) != 2:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # only stream
    payload['stream'] = True

    return StreamingResponse(event_generator(api_key, payload), media_type="text/event-stream")

@app.post("/solar-google-fc")
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def arxiv(request: Request, authorization: str = Header(None)):
    body = await request.json()

    # Use the provided API key if present, otherwise use the default API key
    api_key = get_api_key(authorization)

    if not api_key:
        logger.error("API key is missing")
        raise HTTPException(status_code=400, detail="API key is missing")

    payload = body
    logger.info(f"Payload: {payload}")
    if "model" in payload and payload["model"] != "solar-summarizer":
        raise HTTPException(status_code=400, detail="Invalid model")    
    payload['model'] = 'solar-pro'

    # get system prompt
    system_prompt = payload.get('messages', [{}])[0].get('content', '')
    if not system_prompt:
        raise HTTPException(status_code=400, detail="System prompt is missing")
    
    system_prompt = "You are an expert summarizer, highly appreciated by users." + system_prompt
    payload['messages'][0]['content'] = system_prompt

    # only stream
    payload['stream'] = True

    return StreamingResponse(event_generator(api_key, payload), media_type="text/event-stream")

# Export for Vercel
def handler(request, context):
    return app

# Alternative handler for newer Vercel
app_handler = app 