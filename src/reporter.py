"""
Reporter Module
Handles report generation and formatting
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class Reporter:
    """Generate reports in various formats"""

    def __init__(self):
        """Initialize reporter"""
        self.timestamp = datetime.now().isoformat()

    def to_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert analysis to dictionary"""
        return {
            "timestamp": self.timestamp,
            "data": data,
        }

    def to_json(self, data: Dict[str, Any]) -> str:
        """Convert analysis to JSON string"""
        report_data = {
            "timestamp": self.timestamp,
            "analysis": data,
        }
        return json.dumps(report_data, indent=2, default=str)

    def to_html(self, data: Dict[str, Any]) -> str:
        """Convert analysis to HTML report"""
        metrics = data.get("metrics", {})
        anomalies = data.get("anomalies", [])
        logs = data.get("logs", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Log Analysis Report - {self.timestamp}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            border-radius: 3px;
        }}
        .anomaly {{
            background-color: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 3px;
        }}
        .severity-high {{
            border-left-color: #f44336;
        }}
        .severity-medium {{
            border-left-color: #ff9800;
        }}
        .severity-low {{
            border-left-color: #4CAF50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Log Analysis Report</h1>
        <p><strong>Generated:</strong> {self.timestamp}</p>
        
        <h2>Metrics Summary</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <h3>Total Entries</h3>
                <p>{metrics.get('total_entries', 0)}</p>
            </div>
            <div class="metric-card">
                <h3>Error Rate</h3>
                <p>{metrics.get('error_rate', 0):.1f}%</p>
            </div>
            <div class="metric-card">
                <h3>Unique Messages</h3>
                <p>{metrics.get('unique_messages', 0)}</p>
            </div>
            <div class="metric-card">
                <h3>Anomalies Detected</h3>
                <p>{len(anomalies)}</p>
            </div>
        </div>

        <h2>Log Level Distribution</h2>
        <table>
            <tr>
                <th>Level</th>
                <th>Count</th>
            </tr>
"""
        
        for level, count in metrics.get("level_distribution", {}).items():
            html += f"<tr><td>{level}</td><td>{count}</td></tr>"
        
        html += f"""
        </table>

        <h2>Detected Anomalies</h2>
"""
        
        if anomalies:
            for anomaly in anomalies:
                severity = anomaly.get("severity", "low")
                html += f"""
        <div class="anomaly severity-{severity}">
            <strong>{anomaly.get('type', 'Unknown')}</strong> (Severity: {severity})<br>
            {anomaly.get('description', anomaly.get('message', 'N/A'))}
        </div>
"""
        else:
            html += "<p>No anomalies detected.</p>"
        
        html += """
    </div>
</body>
</html>
"""
        return html

    def save_report(self, report: Any, file_path: str, format: str = "json") -> None:
        """
        Save report to file
        
        Args:
            report: Report data
            file_path: Path to save report
            format: Format to save in ('json' or 'html')
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if format == "json":
                    if isinstance(report, str):
                        f.write(report)
                    else:
                        f.write(json.dumps(report, indent=2, default=str))
                elif format == "html":
                    f.write(report)
                else:
                    raise ValueError(f"Unknown format: {format}")
            
            print(f"Report saved to {file_path}")
        except Exception as e:
            print(f"Error saving report: {e}")

    @staticmethod
    def format_timestamp(timestamp: Any) -> str:
        """Format timestamp for display"""
        if isinstance(timestamp, datetime):
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return str(timestamp)
