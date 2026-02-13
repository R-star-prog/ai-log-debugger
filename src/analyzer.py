"""
Main Analyzer Module
Orchestrates log analysis workflow
"""

from typing import List, Dict, Any, Optional
from src.log_parser import LogParser, LogEntry
from src.anomaly_detector import AnomalyDetector
from src.ai_engine import AIEngine
from src.reporter import Reporter


class LogAnalyzer:
    """Main analyzer orchestrating the log analysis pipeline"""

    def __init__(
        self,
        config_path: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        """
        Initialize LogAnalyzer

        Args:
            config_path: Path to configuration file
            openai_api_key: OpenAI API key for AI analysis
        """
        self.parser = LogParser()
        self.anomaly_detector = AnomalyDetector(threshold=2.0)
        self.ai_engine = AIEngine(api_key=openai_api_key)
        self.reporter = Reporter()
        self.config_path = config_path
        self.logs: List[LogEntry] = []
        self.metrics: Dict[str, Any] = {}
        self.anomalies: List[Dict[str, Any]] = []

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Complete analysis workflow for a log file

        Args:
            file_path: Path to log file

        Returns:
            Complete analysis report
        """
        # Parse logs
        self.logs = self.parser.parse_file(file_path)
        if not self.logs:
            return {"status": "error", "message": f"No logs found in {file_path}"}

        # Extract metrics
        self.metrics = self.anomaly_detector.extract_metrics(self.logs)

        # Detect anomalies
        self.anomalies = self.anomaly_detector.detect_anomalies(self.logs)

        # Get AI suggestions
        ai_analysis = self.ai_engine.analyze_and_suggest(self.anomalies)

        # Generate report
        report = self._generate_report(file_path, ai_analysis)

        return report

    def parse_logs(self, file_path: str) -> List[LogEntry]:
        """Parse logs from file"""
        self.logs = self.parser.parse_file(file_path)
        return self.logs

    def detect_patterns(self, logs: Optional[List[LogEntry]] = None) -> Dict[str, Any]:
        """Detect patterns in logs"""
        logs = logs or self.logs
        if not logs:
            return {}

        from collections import Counter

        # Get message patterns
        messages = [log.message for log in logs]
        message_counter = Counter(messages)

        # Get error patterns
        errors = [log.message for log in logs if log.level in ["ERROR", "CRITICAL"]]
        error_counter = Counter(errors)

        return {
            "top_messages": message_counter.most_common(10),
            "top_errors": error_counter.most_common(5),
            "unique_message_count": len(message_counter),
            "error_count": len(errors),
        }

    def detect_anomalies(
        self, logs: Optional[List[LogEntry]] = None
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in logs"""
        logs = logs or self.logs
        self.anomalies = self.anomaly_detector.detect_anomalies(logs)
        return self.anomalies

    def get_insights(self) -> Dict[str, Any]:
        """Get AI-powered insights"""
        if not self.anomalies:
            return {
                "status": "success",
                "message": "No anomalies detected",
                "insights": [],
            }

        return self.ai_engine.analyze_and_suggest(self.anomalies)

    def generate_report(
        self,
        file_path: Optional[str] = None,
        output_format: str = "dict",
    ) -> Any:
        """
        Generate final report

        Args:
            file_path: Optional file path for output
            output_format: Format for report ('dict', 'json', 'html')

        Returns:
            Report in specified format
        """
        if output_format == "dict":
            return self._generate_report(file_path or "analysis", {})
        elif output_format == "json":
            return self.reporter.to_json(self._get_report_data())
        elif output_format == "html":
            return self.reporter.to_html(self._get_report_data())
        else:
            raise ValueError(f"Unknown format: {output_format}")

    def _generate_report(
        self,
        file_path: str,
        ai_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate complete analysis report"""
        return {
            "status": "success",
            "file": file_path,
            "summary": {
                "total_entries": self.metrics.get("total_entries", 0),
                "error_rate": f"{self.metrics.get('error_rate', 0):.1f}%",
                "unique_messages": self.metrics.get("unique_messages", 0),
                "anomalies_detected": len(self.anomalies),
            },
            "metrics": self.metrics,
            "anomalies": self.anomalies,
            "ai_analysis": ai_analysis,
            "recommendations": self._generate_recommendations(),
        }

    def _get_report_data(self) -> Dict[str, Any]:
        """Get data for report generation"""
        return {
            "metrics": self.metrics,
            "anomalies": self.anomalies,
            "logs": [log.to_dict() for log in self.logs[:100]],  # First 100 logs
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate action recommendations"""
        recommendations = []

        error_rate = self.metrics.get("error_rate", 0)
        if error_rate > 10:
            recommendations.append(
                f"High error rate ({error_rate:.1f}%). Investigate root causes immediately."
            )

        anomaly_count = len(self.anomalies)
        if anomaly_count > 5:
            recommendations.append(
                f"Multiple anomalies detected ({anomaly_count}). Review system health."
            )

        top_errors = self.metrics.get("top_errors", [])
        if top_errors:
            top_error_msg, count = top_errors[0]
            recommendations.append(
                f"Most common error: '{top_error_msg}' (appears {count} times). "
                "Consider implementing a fix or monitor closely."
            )

        if not recommendations:
            recommendations.append("System appears to be running normally.")

        return recommendations
