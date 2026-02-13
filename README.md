# AI-Powered Log Debugging Assistant

An intelligent Python-based log analysis tool that uses machine learning and AI to detect patterns, anomalies, and identify root causes in application logs. Designed for backend engineers to quickly diagnose and resolve system issues.

## Features

- **Intelligent Log Parsing**: Automatically parse and normalize logs from various sources
- **Pattern Detection**: Identify recurring patterns and group related errors
- **Anomaly Detection**: Statistical methods to detect unusual log patterns
- **AI-Powered Insights**: Uses OpenAI to generate intelligent root cause analysis
- **Comprehensive Reporting**: Generate detailed reports with recommendations
- **Multi-Source Support**: Handle logs from applications, databases, and system services

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-log-debugger
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

## Quick Start

```python
from src.analyzer import LogAnalyzer
from src.ai_engine import AIEngine

# Initialize components
analyzer = LogAnalyzer()
ai_engine = AIEngine()

# Parse logs
logs = analyzer.parse_logs("path/to/logs.txt")

# Detect anomalies
anomalies = analyzer.detect_anomalies(logs)

# Get AI insights
insights = ai_engine.analyze_and_suggest(anomalies)

# Generate report
analyzer.generate_report(insights)
```

## Project Structure

```
ai-log-debugger/
├── src/
│   ├── __init__.py
│   ├── log_parser.py          # Log parsing and normalization
│   ├── analyzer.py            # Core analysis engine
│   ├── ai_engine.py           # AI-powered insights using OpenAI
│   ├── anomaly_detector.py    # Statistical anomaly detection
│   └── reporter.py            # Report generation
├── config/
│   └── settings.yaml          # Configuration file
├── logs/                      # Sample and test logs
├── tests/                     # Unit tests
├── requirements.txt           # Project dependencies
├── setup.py                   # Setup configuration
└── README.md                  # This file
```

## Configuration

Edit `config/settings.yaml` to configure:
- Log format patterns
- Anomaly detection thresholds
- AI model settings
- Report output preferences

## Usage Examples

### Analyze Application Logs

```python
from src.analyzer import LogAnalyzer

analyzer = LogAnalyzer(config_path="config/settings.yaml")
logs = analyzer.parse_logs("logs/app.log")
patterns = analyzer.detect_patterns(logs)
print(f"Found {len(patterns)} patterns")
```

### Detect Anomalies

```python
from src.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
metrics = detector.extract_metrics(logs)
anomalies = detector.detect(metrics)
```

### Get AI Recommendations

```python
from src.ai_engine import AIEngine

ai = AIEngine(api_key="your-openai-key")
recommendations = ai.get_root_cause_analysis(anomalies)
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Development

1. Install dev dependencies:
```bash
pip install -e ".[dev]"
```

2. Format code:
```bash
black src/ tests/
```

3. Lint code:
```bash
flake8 src/ tests/
```

## API Documentation

### LogAnalyzer
- `parse_logs(file_path)`: Parse and normalize logs from file
- `detect_patterns(logs)`: Identify recurring patterns
- `detect_anomalies(logs)`: Find unusual entries
- `generate_report(insights)`: Create formatted report

### AIEngine
- `analyze_and_suggest(anomalies)`: Get AI-powered suggestions
- `get_root_cause_analysis(logs)`: Detailed root cause analysis
- `summarize_errors(logs)`: Generate error summaries

### AnomalyDetector
- `extract_metrics(logs)`: Extract statistical metrics from logs
- `detect(metrics)`: Identify anomalies using statistical methods

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] Support for structured logs (JSON, XML)
- [ ] Real-time log streaming analysis
- [ ] Custom anomaly detection models
- [ ] Integration with popular log aggregation tools
- [ ] Dashboard UI
- [ ] Performance optimization

## Changelog

### v0.1.0
- Initial release
- Basic log parsing
- Pattern detection
- Anomaly detection
- AI-powered insights
