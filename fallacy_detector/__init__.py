"""
Fallacy Detector AI Package

An intelligent agent that analyzes news articles for logical fallacies 
based on Aristotelian logic principles.
"""

from .analyzer import FallacyAnalyzer
from .config import AnalysisConfig

__version__ = "1.0.0"
__all__ = ["FallacyAnalyzer", "AnalysisConfig"]
