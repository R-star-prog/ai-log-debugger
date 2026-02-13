# AI-Powered Log Debugging Assistant - Quick Start Guide

## Installation & Setup

### 1. Clone/Navigate to Project
```bash
cd /Users/rayobelihomji/python-AI/AI-Powered\ Log\ Debugging\ Assistant
```

### 2. Activate Virtual Environment
The project automatically creates a Python virtual environment when first accessed.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Analysis
```bash
python main.py logs/sample.log
```

#### Generate HTML Report
```bash
python main.py logs/sample.log --format html --output report.html
```

#### Generate JSON Report
```bash
python main.py logs/sample.log --format json --output report.json
```

#### Verbose Output
```bash
python main.py logs/sample.log --verbose
```

### Python API

```python
from src.analyzer import LogAnalyzer
from src.reporter import Reporter

# Initialize analyzer
analyzer = LogAnalyzer()

# Analyze log file
report = analyzer.analyze_file("logs/sample.log")

# Print summary
print(f"Error Rate: {report['summary']['error_rate']}")
print(f"Anomalies: {report['summary']['anomalies_detected']}")

# Generate formatted report
reporter = Reporter()
html_report = reporter.to_html(analyzer._get_report_data())
reporter.save_report(html_report, "output.html", format="html")
```

## Core Features

### 1. Log Parsing (`src/log_parser.py`)
- Parses multiple log formats (ISO8601, standard, syslog)
- Extracts metadata (IPs, HTTP status codes, error codes)
- Normalizes log entries

```python
from src.log_parser import LogParser

parser = LogParser()
logs = parser.parse_file("logs/sample.log")
for log in logs[:5]:
    print(log)
```

### 2. Anomaly Detection (`src/anomaly_detector.py`)
- Statistical anomaly detection
- Error spike detection
- Pattern anomaly detection
- Timing anomaly detection

```python
from src.anomaly_detector import AnomalyDetector
from src.log_parser import LogParser

parser = LogParser()
logs = parser.parse_file("logs/sample.log")

detector = AnomalyDetector(threshold=2.0)
anomalies = detector.detect_anomalies(logs)
for anomaly in anomalies:
    print(f"{anomaly['type']}: {anomaly['description']}")
```

### 3. AI-Powered Insights (`src/ai_engine.py`)
- Heuristic-based analysis (no API key required)
- OpenAI-powered analysis (optional, with API key)
- Root cause analysis
- Recommendations

```python
from src.ai_engine import AIEngine

ai = AIEngine(api_key="your-openai-key")
analysis = ai.analyze_and_suggest(anomalies)
for suggestion in analysis['suggestions']:
    print(suggestion)
```

### 4. Pattern Detection
```python
from src.analyzer import LogAnalyzer

analyzer = LogAnalyzer()
analyzer.parse_logs("logs/sample.log")
patterns = analyzer.detect_patterns()

print(f"Top errors: {patterns['top_errors']}")
print(f"Error count: {patterns['error_count']}")
```

## Configuration

Edit `config/settings.yaml` to customize:

```yaml
log_format: standard
anomaly_threshold: 2.0
error_rate_threshold: 10.0
report_format: json
openai:
  enabled: true
  model: gpt-3.5-turbo
  max_tokens: 500
  temperature: 0.3
```

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
.
├── main.py                 # CLI entry point
├── src/
│   ├── __init__.py
│   ├── log_parser.py       # Log parsing
│   ├── analyzer.py         # Main analysis engine
│   ├── ai_engine.py        # AI-powered insights
│   ├── anomaly_detector.py # Anomaly detection
│   └── reporter.py         # Report generation
├── config/
│   ├── settings.py         # Settings manager
│   └── settings.yaml       # Configuration file
├── logs/
│   └── sample.log          # Sample log file
├── tests/                  # Unit tests
├── requirements.txt        # Dependencies
└── README.md              # Full documentation
```

## Examples

### Analyze Application Logs
```python
from src.analyzer import LogAnalyzer

analyzer = LogAnalyzer()
logs = analyzer.parse_logs("app.log")
metrics = analyzer.detect_patterns(logs)
print(f"Total entries: {metrics.get('unique_message_count')}")
```

### Get AI Insights (Fallback Mode - No API Key)
```python
from src.analyzer import LogAnalyzer

analyzer = LogAnalyzer()
report = analyzer.analyze_file("system.log")

for rec in report['recommendations']:
    print(f"• {rec}")
```

### Export Analysis
```python
from src.analyzer import LogAnalyzer
from src.reporter import Reporter

analyzer = LogAnalyzer()
report = analyzer.analyze_file("app.log")

reporter = Reporter()
reporter.save_report(report, "analysis.json", format="json")
reporter.save_report(
    reporter.to_html(analyzer._get_report_data()),
    "analysis.html",
    format="html"
)
```

## Next Steps

1. **Configure OpenAI API** (optional): Set `OPENAI_API_KEY` in `.env` for AI-powered insights
2. **Customize Settings**: Update `config/settings.yaml` for your environment
3. **Add Your Logs**: Place log files in `logs/` directory and analyze
4. **Integrate**: Use the Python API in your own scripts

## Troubleshooting

### Module Not Found Error
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### OpenAI API Connection Issues
- Ensure `OPENAI_API_KEY` is set in `.env`
- Check API key validity at https://platform.openai.com
- Project works fine without API key using fallback heuristic mode

### Log Parsing Issues
- Ensure log format matches one of the supported formats
- Check `config/settings.yaml` for format configuration
- View logs with: `python -c "from src.log_parser import LogParser; p = LogParser(); logs = p.parse_file('your.log'); print(logs[0])"`

## Performance Tips

- For large log files (>100MB), consider splitting into chunks
- Adjust `chunk_size` in settings for optimal analysis
- Use `pytest --cov` to identify bottlenecks

## License

MIT License - See LICENSE file for details
