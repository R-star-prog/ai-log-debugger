"""
Main entry point for the AI-Powered Log Debugging Assistant
"""

import sys
import argparse
from pathlib import Path

from src.analyzer import LogAnalyzer
from src.reporter import Reporter
from config.settings import Settings


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Log Debugging Assistant"
    )
    
    parser.add_argument(
        "logfile",
        help="Path to the log file to analyze"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path for the report",
        default=None
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["json", "html", "dict"],
        default="json",
        help="Output format for the report"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file",
        default="config/settings.yaml"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate log file exists
    if not Path(args.logfile).exists():
        print(f"Error: Log file not found: {args.logfile}")
        sys.exit(1)
    
    # Load settings
    settings = Settings(config_file=args.config if Path(args.config).exists() else None)
    
    if args.verbose:
        print(f"Loading configuration from: {args.config}")
        print(f"Analyzing log file: {args.logfile}")
        print(f"Output format: {args.format}")
    
    # Initialize analyzer
    analyzer = LogAnalyzer(config_path=args.config)
    
    # Perform analysis
    if args.verbose:
        print("Starting analysis...")
    
    report = analyzer.analyze_file(args.logfile)
    
    # Generate output
    reporter = Reporter()
    
    if args.format == "json":
        output = reporter.to_json(analyzer._get_report_data())
    elif args.format == "html":
        output = reporter.to_html(analyzer._get_report_data())
    else:
        output = report
    
    # Save or print output
    if args.output:
        reporter.save_report(output, args.output, format=args.format)
        if args.verbose:
            print(f"Report saved to: {args.output}")
    else:
        if isinstance(output, dict):
            import json
            print(json.dumps(output, indent=2, default=str))
        else:
            print(output)
    
    # Print summary
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"Total entries: {report['summary']['total_entries']}")
    print(f"Error rate: {report['summary']['error_rate']}")
    print(f"Unique messages: {report['summary']['unique_messages']}")
    print(f"Anomalies detected: {report['summary']['anomalies_detected']}")
    print("\nRecommendations:")
    for i, rec in enumerate(report.get('recommendations', []), 1):
        print(f"{i}. {rec}")
    print("="*50)


if __name__ == "__main__":
    main()
