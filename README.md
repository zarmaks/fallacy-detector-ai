# AI Agent for Detecting Logical Fallacies in News Articles

🔍 **An intelligent agent that analyzes news articles for logical fallacies based on Aristotelian logic**

## Concept & Inspiration

This project bridges **2,400 years of philosophical wisdom** with modern AI technology. Inspired by **Aristotle's foundational work on logical fallacies** from the 4th century BCE, this tool helps identify flawed reasoning in contemporary media.

### Why This Matters

In today's information-saturated world, the ability to recognize logical fallacies is crucial for:
- **Critical thinking** - Understanding when arguments are fundamentally flawed
- **Media literacy** - Identifying misleading reasoning in news articles
- **Democratic discourse** - Promoting better public debate

### The Vision

Combine classical logic with modern AI to create an educational tool that:
- Detects 19 different Aristotelian logical fallacies
- Analyzes real news articles from any domain
- Provides clear explanations of why reasoning is flawed
- Helps users develop better critical thinking skills

## How It Works

1. **Search** - Finds news articles about any topic you specify
2. **Analyze** - Uses AI to identify logical fallacies in the reasoning
3. **Explain** - Shows exactly what's wrong and why it matters
4. **Educate** - Helps you recognize similar patterns in the future

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/fallacy-detector-ai.git
cd fallacy-detector-ai
```

2. Install:
```bash
pip install -e .
```

3. Set API keys:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_openai_key_here"
$env:SERPER_API_KEY="your_serper_key_here"

# Mac/Linux
export OPENAI_API_KEY="your_openai_key_here"
export SERPER_API_KEY="your_serper_key_here"
```

## Usage

```bash
# Basic usage
python -m fallacy_detector "climate change"

# Specific website
python -m fallacy_detector "AI policy" --domain "techcrunch.com"

# More options
python -m fallacy_detector "economy" --verbose --max-articles 3

# Save results
python -m fallacy_detector "politics" --output "results.txt"
```

## API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Serper**: https://serper.dev/

## Options

- `--domain` - Search specific website
- `--verbose` - Show detailed output  
- `--max-articles` - Number of articles (default: 5)
- `--output` - Save to file
- `--model` - OpenAI model (default: gpt-4o-mini)

## Examples

```bash
python -m fallacy_detector "vaccine policy" --domain "bbc.com"
python -m fallacy_detector "climate change" --verbose --max-articles 2
python -m fallacy_detector "economy" --output "analysis.txt"
```

## Supported Logical Fallacies

The system can detect these classical fallacies based on Aristotelian logic:

- **Ad Hominem** - Attacking the person instead of the argument
- **Appeal to Emotion** - Using emotions instead of logic
- **False Dilemma** - Presenting only two options when more exist
- **Hasty Generalization** - Broad conclusions from limited evidence
- **Circular Reasoning** - Using the conclusion as a premise
- **Strawman** - Misrepresenting someone's argument to make it easier to attack
- **Slippery Slope** - Claiming one event will lead to extreme consequences
- **Appeal to Authority** - Using irrelevant authority as evidence
- And 11 more classical fallacies...

## Philosophy

This tool is built on the principle that **identifying logical fallacies should enhance critical thinking, not replace human judgment**. It serves as an educational aid to help users:

- Recognize patterns of flawed reasoning
- Understand why certain arguments are problematic
- Develop better media literacy skills
- Engage in more thoughtful discourse

**The goal is not to "debunk" every article, but to foster deeper critical thinking about the information we consume.**

## License

MIT License - see LICENSE file for details
