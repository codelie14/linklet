"""Deepseek AI client for chat and text generation."""
import aiohttp
import json
import structlog
from typing import Dict, List, Any, Optional

from src.core.config import settings

logger = structlog.get_logger()

class DeepseekClient:
    """Client pour l'API Deepseek."""
    
    def __init__(self, api_key: str = None):
        """Initialize Deepseek client with optional API key."""
        self.api_key = api_key or settings.deepseek_api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.session = None
        
    async def __aenter__(self):
        """Start aiohttp session when entering context."""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session when exiting context."""
        if self.session:
            await self.session.close()
            
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Deepseek API.
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            
        Returns:
            API response data
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context.")
            
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with self.session.post(url, json=data) as response:
                if response.status != 200:
                    error_data = await response.json()
                    raise ValueError(
                        f"API request failed: {response.status} - {error_data.get('error', 'Unknown error')}"
                    )
                return await response.json()
        except aiohttp.ClientError as e:
            raise RuntimeError(f"Request failed: {str(e)}")
            
    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat-7b",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate response using Deepseek chat model.
        
        Args:
            messages: List of message dictionaries with role and content
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Generated response text
        """
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs
        }
        if max_tokens:
            data["max_tokens"] = max_tokens
            
        try:
            async with self as client:
                response = await self._make_request("chat/completions", data)
                return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error("Chat completion failed", error=str(e))
            raise
            
    async def generate_text(
        self,
        prompt: str,
        model: str = "deepseek-coder-33b",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using Deepseek completion model.
        
        Args:
            prompt: Text prompt
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        data = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            **kwargs
        }
        if max_tokens:
            data["max_tokens"] = max_tokens
            
        try:
            async with self as client:
                response = await self._make_request("completions", data)
                return response["choices"][0]["text"].strip()
        except Exception as e:
            logger.error("Text completion failed", error=str(e))
            raise
