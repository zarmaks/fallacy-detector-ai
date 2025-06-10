"""
Configuration for the Fallacy Detector AI.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AnalysisConfig:
    """Configuration class for fallacy analysis."""
    
    # Model configuration
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 16000
    
    # Article processing
    article_char_limit: int = 5000
    
    # API keys from environment
    openai_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Initialize API keys from environment if not provided."""
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            
        if self.serper_api_key is None:
            self.serper_api_key = os.getenv("SERPER_API_KEY")
        
        # Validate required keys
        if not self.openai_api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
            
        if not self.serper_api_key:
            raise ValueError("Serper API key required. Set SERPER_API_KEY environment variable.")
