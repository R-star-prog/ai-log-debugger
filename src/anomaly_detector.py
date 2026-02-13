"""
Anomaly Detection Module
Statistical methods for identifying unusual log patterns
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter
from src.log_parser import LogEntry


class AnomalyDetector:
    """Detect anomalies in log data using statistical methods"""

    def __init__(self, threshold: float = 2.0):
        """
        Initialize anomaly detector

        Args:
            threshold: Standard deviation threshold for flagging anomalies
        """
        self.threshold = threshold
        self.baseline_stats = {}

    def extract_metrics(self, entries: List[LogEntry]) -> Dict[str, Any]:
        """
        Extract statistical metrics from log entries

        Args:
            entries: List of LogEntry objects

        Returns:
            Dictionary with extracted metrics
        """
        if not entries:
            return {}

        metrics = {
            "total_entries": len(entries),
            "level_distribution": self._get_level_distribution(entries),
            "error_rate": self._calculate_error_rate(entries),
            "message_length_stats": self._get_message_length_stats(entries),
            "time_gaps": self._calculate_time_gaps(entries),
            "unique_messages": len(set(e.message for e in entries)),
            "top_errors": self._get_top_errors(entries),
        }

        return metrics

    def detect_anomalies(self, entries: List[LogEntry]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in log entries

        Args:
            entries: List of LogEntry objects

        Returns:
            List of detected anomalies with details
        """
        anomalies = []

        # Check for spike in errors
        error_anomalies = self._detect_error_spikes(entries)
        anomalies.extend(error_anomalies)

        # Check for unusual message patterns
        pattern_anomalies = self._detect_pattern_anomalies(entries)
        anomalies.extend(pattern_anomalies)

        # Check for timing anomalies
        timing_anomalies = self._detect_timing_anomalies(entries)
        anomalies.extend(timing_anomalies)

        return anomalies

    def _get_level_distribution(self, entries: List[LogEntry]) -> Dict[str, int]:
        """Get distribution of log levels"""
        distribution = Counter(e.level for e in entries)
        return dict(distribution)

    def _calculate_error_rate(self, entries: List[LogEntry]) -> float:
        """Calculate percentage of error/warning logs"""
        if not entries:
            return 0.0

        error_count = sum(
            1 for e in entries if e.level in ["ERROR", "CRITICAL", "WARNING"]
        )
        return (error_count / len(entries)) * 100

    def _get_message_length_stats(self, entries: List[LogEntry]) -> Dict[str, float]:
        """Get statistics on message lengths"""
        if not entries:
            return {}

        lengths = [len(e.message) for e in entries]
        return {
            "mean": float(np.mean(lengths)),
            "std": float(np.std(lengths)),
            "min": float(np.min(lengths)),
            "max": float(np.max(lengths)),
        }

    def _calculate_time_gaps(self, entries: List[LogEntry]) -> List[float]:
        """Calculate time gaps between consecutive log entries (in seconds)"""
        gaps = []
        for i in range(1, len(entries)):
            prev_time = entries[i - 1].timestamp
            curr_time = entries[i].timestamp
            gap = (curr_time - prev_time).total_seconds()
            gaps.append(gap)

        return gaps

    def _get_top_errors(
        self, entries: List[LogEntry], top_n: int = 5
    ) -> List[Tuple[str, int]]:
        """Get most common error messages"""
        error_entries = [e for e in entries if e.level in ["ERROR", "CRITICAL"]]
        error_counter = Counter(e.message for e in error_entries)
        return error_counter.most_common(top_n)

    def _detect_error_spikes(self, entries: List[LogEntry]) -> List[Dict[str, Any]]:
        """Detect sudden increases in error frequency"""
        anomalies = []

        # Split entries into chunks of 100
        chunk_size = max(10, len(entries) // 10)
        chunks = [
            entries[i : i + chunk_size] for i in range(0, len(entries), chunk_size)
        ]

        error_rates = []
        for chunk in chunks:
            error_count = sum(1 for e in chunk if e.level in ["ERROR", "CRITICAL"])
            rate = (error_count / len(chunk)) * 100 if chunk else 0
            error_rates.append(rate)

        # Calculate mean and std of error rates
        if len(error_rates) > 1:
            mean_rate = np.mean(error_rates)
            std_rate = np.std(error_rates)

            for i, rate in enumerate(error_rates):
                if rate > mean_rate + (self.threshold * std_rate):
                    chunk = chunks[i]
                    anomalies.append(
                        {
                            "type": "error_spike",
                            "severity": (
                                "high"
                                if rate > mean_rate + (2 * std_rate)
                                else "medium"
                            ),
                            "description": f"Error spike detected: {rate:.1f}% error rate (baseline: {mean_rate:.1f}%)",
                            "chunk_start": chunk[0].timestamp if chunk else None,
                            "chunk_end": chunk[-1].timestamp if chunk else None,
                            "affected_entries": len(chunk),
                        }
                    )

        return anomalies

    def _detect_pattern_anomalies(
        self, entries: List[LogEntry]
    ) -> List[Dict[str, Any]]:
        """Detect unusual patterns in messages"""
        anomalies = []

        message_counter = Counter(e.message for e in entries)
        total_entries = len(entries)

        # Find messages that appear very frequently or very rarely
        for message, count in message_counter.most_common(20):
            percentage = (count / total_entries) * 100

            # Flag messages appearing in >30% of logs or very rare
            if percentage > 30 or (count == 1 and total_entries > 100):
                anomalies.append(
                    {
                        "type": "pattern_anomaly",
                        "severity": "high" if percentage > 50 else "medium",
                        "message": message[:100],
                        "occurrence_count": count,
                        "percentage": percentage,
                    }
                )

        return anomalies

    def _detect_timing_anomalies(self, entries: List[LogEntry]) -> List[Dict[str, Any]]:
        """Detect unusual timing patterns"""
        anomalies = []

        gaps = self._calculate_time_gaps(entries)
        if not gaps:
            return anomalies

        gaps = np.array(gaps)
        mean_gap = np.mean(gaps)
        std_gap = np.std(gaps)

        # Find unusually large gaps
        for i, gap in enumerate(gaps):
            if gap > mean_gap + (self.threshold * std_gap):
                anomalies.append(
                    {
                        "type": "timing_anomaly",
                        "severity": "medium",
                        "description": f"Unusual gap between logs: {gap:.2f}s (baseline: {mean_gap:.2f}s)",
                        "gap_duration": gap,
                        "entry_index": i,
                    }
                )

        return anomalies
