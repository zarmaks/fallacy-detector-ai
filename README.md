# Fallacy Detector AI

AI tool that detects logical fallacies in news articles.

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
