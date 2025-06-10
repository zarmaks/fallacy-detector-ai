"""
AI prompt templates for the Fallacy Detector.
"""

# Summary prompt template
SUMMARY_TEMPLATE = """You are a communications expert. Analyze this news article and create a precise 5-sentence summary.

INSTRUCTIONS:
- Be accurate, do not invent information
- Focus on main arguments and evidence
- Think step by step

LOGICAL FALLACIES TO WATCH FOR:
{fallacies_df}

ARTICLE:
{content}

SUMMARY (5 sentences):"""

# Fallacy analysis prompt template  
FALLACY_ANALYSIS_TEMPLATE = """You are an ethics professor analyzing this article summary for logical fallacies.

RESPONSE FORMAT:
1. **Primary Fallacy**: The most significant fallacy identified
2. **Impact**: How this fallacy might mislead readers  
3. **Alternative Interpretation**: Possible innocent explanation

ARTICLE SUMMARY:
{summary}

FALLACY DEFINITIONS:
{fallacies_df}

ANALYSIS:"""
