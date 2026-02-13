"""
AI Engine Module
Leverages OpenAI API for intelligent log analysis and recommendations
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEngine:
    """AI-powered log analysis using OpenAI or fallback logic"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize AI engine
        
        Args:
            api_key: OpenAI API key (if None, loads from .env)
            model: Model to use for analysis
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
            except ImportError:
                print("Warning: openai package not installed. Using fallback mode.")

    def analyze_and_suggest(self, anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze anomalies and provide suggestions
        
        Args:
            anomalies: List of detected anomalies
            
        Returns:
            Dictionary with AI-generated suggestions
        """
        if not anomalies:
            return {
                "status": "success",
                "message": "No anomalies detected",
                "suggestions": [],
            }

        # Try to use OpenAI API, fall back to heuristic analysis
        if self.api_key:
            return self._ai_analysis_openai(anomalies)
        else:
            return self._ai_analysis_heuristic(anomalies)

    def get_root_cause_analysis(self, error_logs: List[str]) -> Dict[str, Any]:
        """
        Generate root cause analysis for error logs
        
        Args:
            error_logs: List of error log strings
            
        Returns:
            Root cause analysis with recommendations
        """
        if not error_logs:
            return {"status": "success", "causes": [], "recommendations": []}

        if self.api_key:
            return self._root_cause_openai(error_logs)
        else:
            return self._root_cause_heuristic(error_logs)

    def _ai_analysis_openai(self, anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use OpenAI to analyze anomalies"""
        try:
            import openai
            
            # Prepare anomaly summary for analysis
            anomaly_text = self._format_anomalies(anomalies)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert log analyzer. Provide concise, actionable insights for the detected anomalies.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze these log anomalies and suggest fixes:\n\n{anomaly_text}",
                    },
                ],
                max_tokens=500,
                temperature=0.3,
            )
            
            suggestion = response.choices[0].message.content
            
            return {
                "status": "success",
                "method": "openai",
                "suggestions": [suggestion],
                "anomaly_count": len(anomalies),
            }
        except Exception as e:
            print(f"OpenAI analysis failed: {e}. Falling back to heuristic analysis.")
            return self._ai_analysis_heuristic(anomalies)

    def _ai_analysis_heuristic(self, anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback heuristic-based analysis without OpenAI"""
        suggestions = []
        
        for anomaly in anomalies:
            anomaly_type = anomaly.get("type", "unknown")
            severity = anomaly.get("severity", "low")
            
            if anomaly_type == "error_spike":
                suggestion = self._suggest_error_spike_fix(anomaly, severity)
                suggestions.append(suggestion)
            
            elif anomaly_type == "pattern_anomaly":
                suggestion = self._suggest_pattern_fix(anomaly, severity)
                suggestions.append(suggestion)
            
            elif anomaly_type == "timing_anomaly":
                suggestion = self._suggest_timing_fix(anomaly, severity)
                suggestions.append(suggestion)

        return {
            "status": "success",
            "method": "heuristic",
            "suggestions": suggestions,
            "anomaly_count": len(anomalies),
        }

    def _root_cause_openai(self, error_logs: List[str]) -> Dict[str, Any]:
        """Use OpenAI to determine root causes"""
        try:
            import openai
            
            logs_text = "\n".join(error_logs[:10])  # Limit to first 10 logs
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert system administrator. Analyze error logs and identify root causes.",
                    },
                    {
                        "role": "user",
                        "content": f"What are the likely root causes of these errors?\n\n{logs_text}",
                    },
                ],
                max_tokens=400,
                temperature=0.3,
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "status": "success",
                "method": "openai",
                "analysis": analysis,
                "log_count": len(error_logs),
            }
        except Exception as e:
            print(f"OpenAI root cause analysis failed: {e}")
            return self._root_cause_heuristic(error_logs)

    def _root_cause_heuristic(self, error_logs: List[str]) -> Dict[str, Any]:
        """Fallback heuristic root cause analysis"""
        causes = []
        recommendations = []
        
        error_text = " ".join(error_logs).lower()
        
        # Check for common error patterns
        if any(word in error_text for word in ["connection", "timeout", "refused"]):
            causes.append("Network connectivity or service availability issue")
            recommendations.append("Check network connectivity and service status")
        
        if any(word in error_text for word in ["memory", "out of memory", "heap"]):
            causes.append("Memory exhaustion or memory leak")
            recommendations.append("Increase heap size or investigate memory leak")
        
        if any(word in error_text for word in ["permission", "denied", "unauthorized"]):
            causes.append("Authentication or authorization failure")
            recommendations.append("Check user credentials and permissions")
        
        if any(word in error_text for word in ["database", "sql", "query"]):
            causes.append("Database query or connection issue")
            recommendations.append("Check database connectivity and query syntax")
        
        if not causes:
            causes.append("Requires detailed investigation")
            recommendations.append("Review full error stack trace and logs")
        
        return {
            "status": "success",
            "method": "heuristic",
            "causes": causes,
            "recommendations": recommendations,
        }

    def _suggest_error_spike_fix(self, anomaly: Dict[str, Any], severity: str) -> str:
        """Generate suggestion for error spike"""
        affected = anomaly.get("affected_entries", 0)
        return (
            f"Error Spike Detected (Severity: {severity}): "
            f"{affected} entries affected. "
            f"Action: Review error messages during this period, check system resources, "
            f"and verify external service dependencies."
        )

    def _suggest_pattern_fix(self, anomaly: Dict[str, Any], severity: str) -> str:
        """Generate suggestion for pattern anomaly"""
        message = anomaly.get("message", "Unknown")[:50]
        percentage = anomaly.get("percentage", 0)
        return (
            f"Pattern Anomaly (Severity: {severity}): "
            f"Message '{message}' appears in {percentage:.1f}% of logs. "
            f"Action: Investigate why this pattern is so prevalent or rare."
        )

    def _suggest_timing_fix(self, anomaly: Dict[str, Any], severity: str) -> str:
        """Generate suggestion for timing anomaly"""
        gap = anomaly.get("gap_duration", 0)
        return (
            f"Timing Anomaly (Severity: {severity}): "
            f"Unusual gap of {gap:.2f}s detected in log entries. "
            f"Action: Check for service interruptions or batch processing delays."
        )

    def _format_anomalies(self, anomalies: List[Dict[str, Any]]) -> str:
        """Format anomalies for AI analysis"""
        formatted = []
        for i, anomaly in enumerate(anomalies, 1):
            formatted.append(
                f"{i}. Type: {anomaly.get('type')} | "
                f"Severity: {anomaly.get('severity')} | "
                f"Description: {anomaly.get('description', anomaly.get('message', 'N/A'))}"
            )
        return "\n".join(formatted)
