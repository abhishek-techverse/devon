import pytest
from log_analyzer import LogEntry, LogAnalyzer

class TestLogEntry:
    """Test cases for LogEntry class."""

    def test_parse_line_valid(self):
        """Test valid log line parsing."""
        line = "2023-03-01 08:15:27 - ServiceA - INFO - Started processing request #123"
        entry = LogEntry.parse_line(line)
        assert entry is not None
        assert entry.timestamp == "2023-03-01 08:15:27"
        assert entry.service_name == "ServiceA"
        assert entry.log_level == "INFO"
        assert entry.message == "Started processing request #123"

    def test_parse_line_invalid(self):
        """Test invalid log line handling."""
        line = "Invalid log line"
        entry = LogEntry.parse_line(line)
        assert entry is None

class TestLogAnalyzer:
    """Test cases for LogAnalyzer class."""

    @pytest.fixture
    def analyzer_with_sample_entries(self):
        """Fixture to provide a LogAnalyzer instance with sample entries."""
        analyzer = LogAnalyzer("dummy.log")
        analyzer.entries = [
            LogEntry("2023-03-01 08:15:27", "ServiceA", "INFO", "Started processing request #123"),
            LogEntry("2023-03-01 08:15:28", "ServiceB", "ERROR", "Null pointer exception"),
            LogEntry("2023-03-01 08:20:05", "ServiceC", "WARN", "Disk usage is at 85%"),
        ]
        return analyzer

    def test_tally_by_log_level(self, analyzer_with_sample_entries):
        """Test tallying by log level."""
        log_level_count = analyzer_with_sample_entries.tally_by_log_level()
        assert log_level_count["INFO"] == 1
        assert log_level_count["ERROR"] == 1
        assert log_level_count["WARN"] == 1

    def test_tally_by_service(self, analyzer_with_sample_entries):
        """Test tallying by service name."""
        service_count = analyzer_with_sample_entries.tally_by_service()
        assert service_count["ServiceA"] == 1
        assert service_count["ServiceB"] == 1
        assert service_count["ServiceC"] == 1

    def test_most_common_error(self, analyzer_with_sample_entries):
        """Test identifying the most common error message."""
        common_error = analyzer_with_sample_entries.most_common_error()
        assert common_error[0][0] == "Null pointer exception"
        assert common_error[0][1] == 1

    def test_filter_by_date_range(self, analyzer_with_sample_entries):
        """Test filtering log entries by date range."""
        filtered_entries = analyzer_with_sample_entries.filter_by_date_range(
            "2023-03-01 08:15:00", "2023-03-01 08:16:00"
        )
        assert len(filtered_entries) == 2
        assert filtered_entries[0] == "2023-03-01 08:15:27 - ServiceA - INFO - Started processing request #123"
        assert filtered_entries[1] == "2023-03-01 08:15:28 - ServiceB - ERROR - Null pointer exception"
