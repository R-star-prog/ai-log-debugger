"""
Log Parser Module
Handles parsing and normalization of log files
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class LogEntry:
    """Represents a single log entry"""
    timestamp: datetime
    level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message: str
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_line: str = ""

    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.level}: {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "metadata": self.metadata,
        }


class LogParser:
    """Parse and normalize logs from various formats"""

    # Common log patterns
    PATTERNS = {
        "iso8601": r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})",
        "standard": r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})",
        "syslog": r"^(\w+\s+\d+\s+\d{2}:\d{2}:\d{2})",
        "timestamp": r"(\d{10,13})",  # Unix timestamp
        "level": r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL|WARN|ERR)\b",
    }

    def __init__(self):
        """Initialize the log parser"""
        self.compiled_patterns = {
            name: re.compile(pattern) for name, pattern in self.PATTERNS.items()
        }

    def parse_file(self, file_path: str) -> List[LogEntry]:
        """
        Parse a log file and return list of LogEntry objects
        
        Args:
            file_path: Path to the log file
            
        Returns:
            List of parsed LogEntry objects
        """
        entries = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry = self.parse_line(line)
                        if entry:
                            entries.append(entry)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return entries
        
        return entries

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single log line
        
        Args:
            line: Single log line
            
        Returns:
            LogEntry object or None if parsing fails
        """
        if not line:
            return None

        # Extract timestamp
        timestamp = self._extract_timestamp(line)
        if not timestamp:
            timestamp = datetime.now()

        # Extract log level
        level = self._extract_level(line)
        if not level:
            level = "INFO"

        # Extract message (everything after the level indicator)
        message = self._extract_message(line, level)

        # Create metadata
        metadata = self._extract_metadata(line)

        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            metadata=metadata,
            raw_line=line,
        )

    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from log line"""
        for pattern_name in ["iso8601", "standard", "timestamp"]:
            pattern = self.compiled_patterns[pattern_name]
            match = pattern.search(line)
            if match:
                try:
                    timestamp_str = match.group(1)
                    if pattern_name == "timestamp":
                        # Unix timestamp
                        return datetime.fromtimestamp(int(timestamp_str) / 1000)
                    else:
                        # Parse ISO or standard format
                        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                            try:
                                return datetime.strptime(timestamp_str, fmt)
                            except ValueError:
                                continue
                except Exception:
                    continue
        return None

    def _extract_level(self, line: str) -> Optional[str]:
        """Extract log level from line"""
        pattern = self.compiled_patterns["level"]
        match = pattern.search(line)
        if match:
            level = match.group(1).upper()
            # Normalize levels
            level_map = {
                "WARN": "WARNING",
                "ERR": "ERROR",
            }
            return level_map.get(level, level)
        return None

    def _extract_message(self, line: str, level: str) -> str:
        """Extract message from log line"""
        # Remove timestamp and level from the line
        message = line
        message = re.sub(self.PATTERNS["iso8601"], "", message)
        message = re.sub(self.PATTERNS["standard"], "", message)
        message = re.sub(self.PATTERNS["level"], "", message)
        
        # Clean up extra whitespace and brackets
        message = re.sub(r"^\s*[\[\-:]*\s*", "", message)
        message = message.strip()
        
        return message[:500]  # Limit message length

    def _extract_metadata(self, line: str) -> Dict[str, Any]:
        """Extract metadata from log line"""
        metadata = {}
        
        # Extract common fields
        # IP addresses
        ip_pattern = r"(?:\d{1,3}\.){3}\d{1,3}"
        ip_matches = re.findall(ip_pattern, line)
        if ip_matches:
            metadata["ips"] = ip_matches

        # HTTP status codes
        status_pattern = r"(?:HTTP/[\d.]+\s+)?(\d{3})\s"
        status_matches = re.findall(status_pattern, line)
        if status_matches:
            metadata["http_status"] = status_matches[0]

        # Error codes
        error_pattern = r"(?:error|code|errno)\s*:?\s*([A-Z0-9_]+|\d+)"
        error_matches = re.findall(error_pattern, line, re.IGNORECASE)
        if error_matches:
            metadata["error_codes"] = error_matches

        return metadata
