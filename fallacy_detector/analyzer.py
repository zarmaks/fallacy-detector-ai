"""
Main analyzer class for the Fallacy Detector AI.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.utilities import GoogleSerperAPIWrapper

from .config import AnalysisConfig
from .prompts import SUMMARY_TEMPLATE, FALLACY_ANALYSIS_TEMPLATE
from .utils import load_fallacies_data, clean_article_text, setup_logging

class FallacyAnalyzer:
    """Main analyzer class for detecting logical fallacies in news articles."""
    
    def __init__(self, config: AnalysisConfig):
        """Initialize the analyzer with configuration."""
        self.config = config
        self.logger = setup_logging()
        
        # Initialize OpenAI model
        self.llm = ChatOpenAI(
            temperature=config.temperature,
            model=config.model_name,
            max_tokens=config.max_tokens,
            openai_api_key=config.openai_api_key
        )
        
        # Load fallacies data
        self.fallacies_df = load_fallacies_data()
        self.logger.info(f"Loaded {len(self.fallacies_df)} fallacy definitions")
        
        # Initialize search wrapper
        self.search = GoogleSerperAPIWrapper(
            type="news",
            tbs="qdr:m1",  # Last month
            serper_api_key=config.serper_api_key
        )
        
        # Create analysis chains
        self._setup_chains()
    
    def _setup_chains(self):
        """Set up LangChain chains for analysis."""
        # Summary chain
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["content", "fallacies_df"],
                template=SUMMARY_TEMPLATE
            )
        )
        
        # Fallacy analysis chain
        self.fallacy_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["summary", "fallacies_df"],
                template=FALLACY_ANALYSIS_TEMPLATE
            )
        )
    
    def load_article(self, search_topic: str, domain: str = "") -> Dict[str, Any]:
        """Load article from search results."""
        try:
            query = f"site:{domain} {search_topic}" if domain else search_topic
            self.logger.info(f"Searching for: {query}")
            
            search_results = self.search.results(query)
            
            if not search_results.get('news'):
                return {'error': 'No articles found for the given search criteria'}
            
            # Get the first article
            first_article = search_results['news'][0]
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
        start_time = datetime.now()
        
        try:
            # Load article
            article_data = self.load_article(search_topic, domain)
            if 'error' in article_data:
                return article_data
            
            # Generate summary
            summary = self.summary_chain.run(
                content=article_data['content'],
                fallacies_df=self.fallacies_df.to_string()
            )
            
            # Analyze fallacies
            analysis = self.fallacy_chain.run(
                summary=summary,
                fallacies_df=self.fallacies_df.to_string()
            )
            
            # Compile results
            result = {
                'title': article_data['title'],
                'url': article_data['url'],
                'summary': summary,
                'analysis': analysis,
                'timestamp': datetime.now(),
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
            
            self.logger.info(f"Analysis completed in {result['processing_time']:.2f} seconds")
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def get_fallacies_info(self) -> pd.DataFrame:
        """Return information about available fallacies."""
        return self.fallacies_df.copy()
