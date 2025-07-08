#!/usr/bin/env python3
"""
Simple test script for the Solar Proxy API.
Run this script to test the API endpoints locally.
"""

import httpx
import json
import asyncio
import os

# Set your API key here or in environment variable
API_KEY = os.getenv('UPSTAGE_API_KEY', 'your_api_key_here')
BASE_URL = "http://localhost:8000"

async def test_root_endpoint():
    """Test the root endpoint."""
    print("Testing root endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()

async def test_summary_endpoint():
    """Test the summary endpoint."""
    print("Testing summary endpoint...")
    
    payload = {
        "model": "solar-summarizer",
        "messages": [
            {
                "role": "system",
                "content": "Summarize the following text:"
            },
            {
                "role": "user",
                "content": "This is a test message for summarization. The AI should be able to process this text and return a summary."
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/summary",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("Response received (streaming):")
                async for line in response.aiter_lines():
                    if line:
                        print(line)
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        print()

async def test_solar_google_fc_endpoint():
    """Test the solar-google-fc endpoint."""
    print("Testing solar-google-fc endpoint...")
    
    payload = {
        "model": "solar-summarizer",
        "messages": [
            {
                "role": "system",
                "content": "Summarize the following text:"
            },
            {
                "role": "user",
                "content": "This is a test message for the solar-google-fc endpoint. It should use the Solar Pro model for advanced summarization."
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/solar-google-fc",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("Response received (streaming):")
                async for line in response.aiter_lines():
                    if line:
                        print(line)
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        print()

async def main():
    """Run all tests."""
    print("Solar Proxy API Test Script")
    print("=" * 40)
    
    if API_KEY == 'your_api_key_here':
        print("Warning: Please set your UPSTAGE_API_KEY environment variable or update the API_KEY in this script.")
        print()
    
    await test_root_endpoint()
    await test_summary_endpoint()
    await test_solar_google_fc_endpoint()
    
    print("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
