"""
Unit tests for Log Parser
"""

import unittest
from datetime import datetime
from src.log_parser import LogParser, LogEntry


class TestLogParser(unittest.TestCase):
    """Test cases for LogParser"""

    def setUp(self):
        """Set up test fixtures"""
        self.parser = LogParser()

    def test_parse_line_with_timestamp(self):
        """Test parsing a line with timestamp"""
        line = "2024-01-15 10:30:45 INFO Application started"
        entry = self.parser.parse_line(line)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "INFO")
        self.assertIn("Application", entry.message)

    def test_extract_log_level(self):
        """Test log level extraction"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in levels:
            line = f"2024-01-15 10:30:45 {level} Test message"
            entry = self.parser.parse_line(line)
            self.assertEqual(entry.level, level)

    def test_parse_line_without_timestamp(self):
        """Test parsing a line without clear timestamp"""
        line = "INFO No timestamp message"
        entry = self.parser.parse_line(line)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "INFO")

    def test_metadata_extraction(self):
        """Test metadata extraction from log line"""
        line = "2024-01-15 10:30:45 ERROR HTTP 500 error code ERR_DB_CONN from 192.168.1.1"
        entry = self.parser.parse_line(line)
        
        self.assertIsNotNone(entry.metadata)
        self.assertIn("ips", entry.metadata)
        self.assertIn("http_status", entry.metadata)


if __name__ == "__main__":
    unittest.main()
