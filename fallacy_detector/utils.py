"""
Utility functions for the Fallacy Detector.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_fallacies_data() -> pd.DataFrame:
    """Load fallacies data from CSV file."""
    # Get path relative to this module
    current_dir = Path(__file__).parent
    csv_path = current_dir.parent / "data" / "fallacies.csv"
    
    try:
        fallacies_df = pd.read_csv(csv_path)
        if 'Fallacy' not in fallacies_df.columns or 'Description' not in fallacies_df.columns:
            raise ValueError("CSV must contain 'Fallacy' and 'Description' columns")
        return fallacies_df
    except FileNotFoundError:
        raise FileNotFoundError(f"Fallacies CSV file not found at {csv_path}")

def clean_article_text(text: str, char_limit: int = 5000) -> str:
    """Clean and limit article text for processing."""
    if not text:
        return ""
    
    # Remove extra whitespace and limit length
    cleaned_text = ' '.join(text.split())
    
    if len(cleaned_text) > char_limit:
        # Try to cut at sentence boundary
        limited_text = cleaned_text[:char_limit]
        last_period = limited_text.rfind('.')
        if last_period > char_limit * 0.8:
            return limited_text[:last_period + 1]
        else:
            return limited_text + "..."
    
    return cleaned_text

def format_analysis_result(result_data: Dict[str, Any]) -> str:
    """Format analysis results for display."""
    if 'error' in result_data:
        return f"Error: {result_data['error']}"
    
    return f"""
ARTICLE ANALYSIS RESULTS
{'='*50}

Title: {result_data.get('title', 'Unknown')}
URL: {result_data.get('url', 'Unknown')}
Timestamp: {result_data.get('timestamp', datetime.now())}

LOGICAL FALLACY ANALYSIS:
{'-'*25}
{result_data.get('detected_fallacies', 'No analysis available')}

EDUCATIONAL EXPLANATIONS:
{'-'*25}
{result_data.get('educational_explanations', 'No explanations available')}

SYNTHESIS REPORT:
{'-'*15}
{result_data.get('synthesized_result', 'No synthesis available')}
"""
