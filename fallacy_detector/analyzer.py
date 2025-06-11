"""
AI Agent for detecting logical fallacies in news articles.
"""

import json
import os
import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import SecretStr  # Required for OpenAI API key security

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader  # For article content loading
from bs4 import BeautifulSoup

from .config import AnalysisConfig
from .prompts import (
    FALLACY_DETECTION_PROMPT,
    EDUCATIONAL_EXPLANATION_PROMPT,
    RESULT_SYNTHESIS_PROMPT
)

from .utils import load_fallacies_data, clean_article_text, setup_logging

# Set user agent to avoid warnings
if not os.environ.get('USER_AGENT'):
    os.environ['USER_AGENT'] = 'Fallacy-Detector-AI/1.0'

class FallacyAnalyzer:
    """Main analyzer class for detecting logical fallacies in news articles."""
    
    def __init__(self, config: AnalysisConfig):
        """Initialize the analyzer with configuration."""
        self.config = config
        self.logger = setup_logging()
        
        # Initialize OpenAI chat model
        self.llm = ChatOpenAI(
            temperature=config.temperature,
            model=config.model_name,
            api_key=SecretStr(config.openai_api_key)  # SecretStr required by langchain-openai
        )
        
        # Load fallacies data
        self.fallacies_df = load_fallacies_data()
        self.logger.info(f"Loaded {len(self.fallacies_df)} fallacy definitions")
        
        # Create analysis chains
        self._setup_chains()
    
    def _setup_chains(self):
        """Set up LangChain chains for analysis."""
        # Fallacy detection chain
        self.fallacy_detection_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["content", "fallacies_df"],
                template=FALLACY_DETECTION_PROMPT
            )
        )
        
        # Educational explanation chain
        self.educational_explanation_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["detected_fallacies"],
                template=EDUCATIONAL_EXPLANATION_PROMPT
            )
        )
        
        # Result synthesis chain
        self.result_synthesis_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["summary", "detailed_analysis"],
                template=RESULT_SYNTHESIS_PROMPT
            )
        )
    
    def load_article(self, search_topic: str, domain: str = "") -> Dict[str, Any]:
        """Load article from search results."""
        try:
            query = f"site:{domain} {search_topic}" if domain else search_topic
            self.logger.info(f"Searching for: {query}")
            
            # Use Serper API for Google search
            response = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.config.serper_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "q": query,
                    "num": 5
                }
            )
            search_results = response.json()
            
            # Check if we found any articles
            if not search_results.get('organic'):
                return {'error': 'No articles found for the given search criteria'}
            
            # Get the first article
            first_article = search_results['organic'][0]
            article_url = first_article['link']
            article_title = first_article['title']
            
            # Load article content
            loader = WebBaseLoader(article_url)
            article_content = loader.load()
            
            # Clean and limit content
            article_text = clean_article_text(
                article_content[0].page_content, 
                self.config.article_char_limit
            )
            
            return {
                'url': article_url,
                'title': article_title,
                'content': article_text
            }
            
        except Exception as e:
            self.logger.error(f"Failed to load article: {str(e)}")
            return {'error': f'Article loading failed: {str(e)}'}
    
    def analyze_article(self, search_topic: str, domain: str = "") -> Dict[str, Any]:
        """Complete analysis pipeline for a news article."""
        try:
            # Load article
            article_data = self.load_article(search_topic, domain)
            if 'error' in article_data:
                return article_data
            
            # Detect fallacies - SIMPLE
            detected_fallacies_result = self.fallacy_detection_chain.run(
                content=article_data['content'],
                fallacies_df=self.fallacies_df.to_string()
            )
            
            # Debug output
            print(f"DEBUG - Detected fallacies result: {detected_fallacies_result[:300]}...")
            
            # No JSON parsing needed - just pass as is
            detected_fallacies_cleaned = detected_fallacies_result.strip()
            
            # Generate educational explanations
            educational_explanations = self.educational_explanation_chain.run(
                detected_fallacies=detected_fallacies_cleaned
            )
            
            # Synthesize results
            result = self.result_synthesis_chain.run(
                summary=article_data['content'],  # Assuming summary is the article content for synthesis
                detailed_analysis=educational_explanations
            )
            
            # Compile final result
            final_result = {
                'title': article_data['title'],
                'url': article_data['url'],
                'detected_fallacies': detected_fallacies_result,
                'educational_explanations': educational_explanations,
                'synthesized_result': result
            }
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def get_fallacies_info(self) -> pd.DataFrame:
        """Return information about available fallacies."""
        return self.fallacies_df.copy()
