"""
Main entry point for the Fallacy Detector AI.
"""

import argparse
import sys
from pathlib import Path

from .analyzer import FallacyAnalyzer
from .config import AnalysisConfig
from .utils import format_analysis_result

def main():
    """Main function to run the fallacy detector."""
    parser = argparse.ArgumentParser(
        description="AI Agent for Detecting Logical Fallacies in News Articles"
    )
    parser.add_argument("topic", help="Search topic for news articles")
    parser.add_argument("--domain", default="", help="Domain to search within (e.g., 'cnn.com')")
    parser.add_argument("--model", default="gpt-4.1-nano", help="OpenAI model to use")
    parser.add_argument("--output", help="Output file to save results")
    parser.add_argument("--max-articles", type=int, default=5, help="Number of articles to analyze")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    try:
        # Create configuration
        config = AnalysisConfig(model_name=args.model)
        
        # Initialize analyzer
        print("🔍 Initializing Fallacy Detector AI...")
        analyzer = FallacyAnalyzer(config)
        
        # Run analysis
        print(f"Analyzing articles for topic: '{args.topic}'")
        if args.domain:
            print(f"Searching within domain: {args.domain}")
        if args.verbose:
            print(f"Will analyze up to {args.max_articles} articles")
            print(f"Using model: {args.model}")
        
        result = analyzer.analyze_article(args.topic, args.domain)
        
        # Format and display results
        formatted_result = format_analysis_result(result)
        print(formatted_result)
        
        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_result)
            print(f"\nResults saved to: {output_path}")
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def demo():
    """Run a demonstration of the fallacy detector."""
    print("🔍 Fallacy Detector AI - Demo\n")
    
    try:
        config = AnalysisConfig()
        analyzer = FallacyAnalyzer(config)
        
        # Show available fallacies
        fallacies_info = analyzer.get_fallacies_info()
        print("Available Fallacies:")
        print("=" * 50)
        for _, row in fallacies_info.head().iterrows():
            print(f"• {row['Fallacy']}: {row['Description'][:80]}...")
        print()
        
        # Demo analysis
        topic = "climate change policy"
        print(f"Demo: Analyzing '{topic}'")
        print("-" * 50)
        
        result = analyzer.analyze_article(topic, "whitehouse.gov")
        
        if 'error' not in result:
            print(f"✓ Title: {result['title']}")
            print(f"✓ Analysis preview: {result['analysis'][:200]}...")
            print(f"✓ Processing time: {result.get('processing_time', 0):.2f}s")
        else:
            print(f"✗ Error: {result['error']}")
            
    except Exception as e:
        print(f"Demo failed: {str(e)}")

if __name__ == "__main__":
    main()
