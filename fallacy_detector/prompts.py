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

# Missing prompts that analyzer.py needs:
FALLACY_DETECTION_PROMPT = """You are an expert in classical logic and Aristotelian fallacies. Analyze this article content for logical fallacies.

AVAILABLE FALLACIES:
{fallacies_df}

ARTICLE CONTENT:
{content}

Instructions:
- Identify logical fallacies present in the text
- Quote the exact text that contains each fallacy
- Explain why it constitutes that particular fallacy
- Rate confidence level (Low/Medium/High)

Format your response as simple text, not JSON:

FALLACY ANALYSIS:
1. **[Fallacy Name]** (Confidence: High)
   - Text: "[exact quote]"
   - Reason: [explanation]

2. **[Fallacy Name]** (Confidence: Medium)
   - Text: "[exact quote]"
   - Reason: [explanation]

If no fallacies detected, write: "No significant logical fallacies detected."

ANALYSIS:"""

EDUCATIONAL_EXPLANATION_PROMPT = """You are an educator explaining logical fallacies to help people develop critical thinking skills.

DETECTED FALLACIES:
{detected_fallacies}

For each detected fallacy, provide:
1. **What it is**: Clear definition
2. **Why it's problematic**: How it misleads reasoning
3. **How to recognize it**: Warning signs to watch for
4. **Better approach**: How the argument could be improved

Make your explanations accessible and educational.

EDUCATIONAL EXPLANATION:"""

RESULT_SYNTHESIS_PROMPT = """You are synthesizing a comprehensive analysis report.

ARTICLE SUMMARY:
{summary}

DETAILED ANALYSIS:
{detailed_analysis}

Create a final report that:
1. Summarizes key findings
2. Explains the educational value
3. Provides actionable insights for readers
4. Maintains a balanced, educational tone

FINAL REPORT:"""
