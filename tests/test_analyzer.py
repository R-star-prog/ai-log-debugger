"""
Integration tests
"""

import unittest
import os
import tempfile
from src.analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):
    """Integration tests for LogAnalyzer"""

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = LogAnalyzer()
        
        # Create a temporary log file
        self.temp_log = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        self.temp_log.write("2024-01-15 08:00:00 INFO System started\n")
        self.temp_log.write("2024-01-15 08:00:05 INFO Processing request\n")
        self.temp_log.write("2024-01-15 08:00:10 ERROR Database connection failed\n")
        self.temp_log.write("2024-01-15 08:00:15 ERROR Database connection failed\n")
        self.temp_log.write("2024-01-15 08:00:20 WARNING Retrying connection\n")
        self.temp_log.close()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_log.name):
            os.unlink(self.temp_log.name)

    def test_analyze_file(self):
        """Test complete analysis workflow"""
        report = self.analyzer.analyze_file(self.temp_log.name)
        
        self.assertEqual(report["status"], "success")
        self.assertIn("summary", report)
        self.assertIn("metrics", report)
        self.assertIn("anomalies", report)
        self.assertGreater(report["summary"]["total_entries"], 0)

    def test_parse_logs(self):
        """Test log parsing"""
        logs = self.analyzer.parse_logs(self.temp_log.name)
        
        self.assertEqual(len(logs), 5)
        self.assertEqual(logs[0].level, "INFO")

    def test_detect_patterns(self):
        """Test pattern detection"""
        self.analyzer.parse_logs(self.temp_log.name)
        patterns = self.analyzer.detect_patterns()
        
        self.assertIn("top_errors", patterns)
        self.assertGreater(patterns["error_count"], 0)

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        self.analyzer.parse_logs(self.temp_log.name)
        self.analyzer.detect_anomalies()
        recommendations = self.analyzer._generate_recommendations()
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)


if __name__ == "__main__":
    unittest.main()
