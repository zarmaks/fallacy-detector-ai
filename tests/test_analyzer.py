"""
Test the main analyzer functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from fallacy_detector.analyzer import FallacyAnalyzer
from fallacy_detector.config import AnalysisConfig


class TestFallacyAnalyzer(unittest.TestCase):
    """Test cases for the FallacyAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = AnalysisConfig(
            openai_api_key="test_openai_key",
            serper_api_key="test_serper_key"
        )
    
    @patch('fallacy_detector.analyzer.load_fallacies_data')
    @patch('fallacy_detector.analyzer.ChatOpenAI')
    @patch('fallacy_detector.analyzer.GoogleSerperAPIWrapper')
    def test_analyzer_initialization(self, mock_serper, mock_openai, mock_load_data):
        """Test that analyzer initializes correctly."""
        # Mock the fallacies data
        mock_load_data.return_value = pd.DataFrame({
            'Fallacy': ['Ad Hominem', 'False Dilemma'],
            'Description': ['Attack on person', 'Only two options']
        })
        
        analyzer = FallacyAnalyzer(self.config)
        
        self.assertIsInstance(analyzer, FallacyAnalyzer)
        self.assertEqual(len(analyzer.fallacies_df), 2)
        mock_openai.assert_called_once()
        mock_serper.assert_called_once()
    
    @patch('fallacy_detector.analyzer.load_fallacies_data')
    @patch('fallacy_detector.analyzer.ChatOpenAI')
    @patch('fallacy_detector.analyzer.GoogleSerperAPIWrapper')
    def test_load_article_success(self, mock_serper, mock_openai, mock_load_data):
        """Test successful article loading."""
        # Setup mocks
        mock_load_data.return_value = pd.DataFrame({
            'Fallacy': ['Ad Hominem'], 'Description': ['Attack on person']
        })
        
        mock_search_instance = MagicMock()
        mock_serper.return_value = mock_search_instance
        mock_search_instance.results.return_value = {
            'news': [{
                'link': 'https://example.com/article',
                'title': 'Test Article'
            }]
        }
        
        # Create analyzer
        analyzer = FallacyAnalyzer(self.config)
        
        # Mock WebBaseLoader
        with patch('fallacy_detector.analyzer.WebBaseLoader') as mock_loader:
            mock_content = MagicMock()
            mock_content.page_content = "This is test article content."
            mock_loader.return_value.load.return_value = [mock_content]
            
            result = analyzer.load_article("test topic", "example.com")
            
            self.assertIn('url', result)
            self.assertIn('title', result)
            self.assertIn('content', result)
            self.assertEqual(result['url'], 'https://example.com/article')
    
    @patch('fallacy_detector.analyzer.load_fallacies_data')
    @patch('fallacy_detector.analyzer.ChatOpenAI')
    @patch('fallacy_detector.analyzer.GoogleSerperAPIWrapper')
    def test_load_article_no_results(self, mock_serper, mock_openai, mock_load_data):
        """Test article loading when no results found."""
        # Setup mocks
        mock_load_data.return_value = pd.DataFrame({
            'Fallacy': ['Ad Hominem'], 'Description': ['Attack on person']
        })
        
        mock_search_instance = MagicMock()
        mock_serper.return_value = mock_search_instance
        mock_search_instance.results.return_value = {'news': []}
        
        analyzer = FallacyAnalyzer(self.config)
        result = analyzer.load_article("test topic", "example.com")
        
        self.assertIn('error', result)


if __name__ == '__main__':
    unittest.main()
