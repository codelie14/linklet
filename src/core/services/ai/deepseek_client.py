"""Deepseek AI client for chat and text generation."""
import deepseek_ai as deepseek
import structlog
from typing import Dict, List

from src.core.config import settings

logger = structlog.get_logger()

class DeepseekClient:
    """Client pour l'API Deepseek."""
    
    def __init__(self, api_key: str = None):
        """Initialize Deepseek client with optional API key."""
        self.api_key = api_key or settings.deepseek_api_key
        deepseek.api_key = self.api_key
        
    async def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response using Deepseek chat model.
        
        Args:
            messages: List of message dictionaries with role and content
            **kwargs: Additional parameters for the model
            
        Returns:
            Generated response text
        """
        try:
            completion = await deepseek.ChatCompletion.acreate(
                model="deepseek-chat",  # ou autre modèle disponible
                messages=messages,
                **kwargs
            )
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error("Deepseek API error", error=str(e))
            raise
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Deepseek completion model.
        
        Args:
            prompt: Text prompt for generation
            **kwargs: Additional parameters for the model
            
        Returns:
            Generated text
        """
        try:
            completion = await deepseek.Completion.acreate(
                model="deepseek-coder",  # ou autre modèle disponible
                prompt=prompt,
                **kwargs
            )
            return completion.choices[0].text.strip()
            
        except Exception as e:
            logger.error("Deepseek API error", error=str(e))
            raise
