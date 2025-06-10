#!/usr/bin/env python3
"""
Example usage of the Fallacy Detector AI.

This script demonstrates how to use the analyzer in different scenarios.
"""

import os
from fallacy_detector import FallacyAnalyzer, AnalysisConfig

def basic_example():
    """Basic usage example."""
    print("🔍 Basic Usage Example")
    print("=" * 50)
    
    try:
        # Check if API keys are set
        if not os.getenv("OPENAI_API_KEY") or not os.getenv("SERPER_API_KEY"):
            print("⚠️  Please set OPENAI_API_KEY and SERPER_API_KEY environment variables")
            return
        
        # Initialize analyzer
        config = AnalysisConfig()
        analyzer = FallacyAnalyzer(config)
        
        # Analyze an article
        print("Analyzing climate change policy articles...")
        result = analyzer.analyze_article("climate change policy", "whitehouse.gov")
        
        if 'error' not in result:
            print(f"✓ Successfully analyzed: {result['title']}")
            print(f"✓ Processing time: {result.get('processing_time', 0):.2f} seconds")
            print(f"\nAnalysis preview:")
            print(result['analysis'][:300] + "..." if len(result['analysis']) > 300 else result['analysis'])
        else:
            print(f"✗ Error: {result['error']}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 70 + "\n")

def custom_config_example():
    """Example with custom configuration."""
    print("⚙️  Custom Configuration Example")
    print("=" * 50)
    
    try:
        # Custom configuration
        config = AnalysisConfig(
            model_name="gpt-4o-mini",
            article_char_limit=3000  # Shorter articles for faster processing
        )
        
        analyzer = FallacyAnalyzer(config)
        
        print("Analyzing AI regulation articles...")
        result = analyzer.analyze_article("artificial intelligence regulation", "reuters.com")
        
        if 'error' not in result:
            print(f"✓ Custom analysis completed")
            print(f"✓ Model used: {config.model_name}")
            print(f"✓ Article length limit: {config.article_char_limit} chars")
            print(f"✓ Processing time: {result.get('processing_time', 0):.2f}s")
        else:
            print(f"✗ Error: {result['error']}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 70 + "\n")

def fallacies_info_example():
    """Example showing available fallacies."""
    print("📖 Available Fallacies")
    print("=" * 50)
    
    try:
        config = AnalysisConfig()
        analyzer = FallacyAnalyzer(config)
        
        # Get fallacies information
        fallacies_info = analyzer.get_fallacies_info()
        
        print(f"Total fallacies available: {len(fallacies_info)}")
        print("\nTop 5 fallacies:")
        print("-" * 30)
        
        for i, (_, row) in enumerate(fallacies_info.head().iterrows(), 1):
            print(f"{i}. **{row['Fallacy']}**")
            print(f"   {row['Description'][:100]}...")
            print()
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("=" * 70 + "\n")

def main():
    """Run all examples."""
    print("🚀 Fallacy Detector AI - Usage Examples")
    print("=" * 70)
    print()
    
    # Check if API keys are available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found")
        print("Please set your API keys before running examples:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your API keys")
        print("3. Source the environment: source .env (Unix) or set variables manually")
        return
    
    if not os.getenv("SERPER_API_KEY"):
        print("⚠️  Warning: SERPER_API_KEY not found")
        print("Please set your Serper API key.")
        return
    
    # Run examples
    try:
        fallacies_info_example()
        basic_example()
        custom_config_example()
        
        print("🎉 Examples completed successfully!")
        print("\nNext steps:")
        print("- Try the CLI: python -m fallacy_detector 'your topic'")
        print("- Run the demo: python -c 'from fallacy_detector.__main__ import demo; demo()'")
        
    except KeyboardInterrupt:
        print("\n👋 Examples interrupted by user.")
    except Exception as e:
        print(f"✗ Examples failed: {str(e)}")

if __name__ == "__main__":
    main()
