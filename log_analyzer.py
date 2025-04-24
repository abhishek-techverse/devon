import re
import csv
from datetime import datetime
from collections import Counter

class LogEntry:
    """Represents a single log entry."""
    def __init__(self, timestamp, service_name, log_level, message):
        self.timestamp = timestamp
        self.service_name = service_name
        self.log_level = log_level
        self.message = message

    @staticmethod
    def parse_line(line):
        """Parses a log line and creates a LogEntry object if valid."""
        log_pattern = r"^(?P<timestamp>[\d\- :]+) - (?P<service_name>\w+) - (?P<log_level>\w+) - (?P<message>.+)$"
        match = re.match(log_pattern, line)
        if match:
            return LogEntry(
                match.group("timestamp"),
                match.group("service_name"),
                match.group("log_level"),
                match.group("message")
            )
        else:
            return None

class LogAnalyzer:
    """Analyzes log files for patterns and statistics."""
    def __init__(self, log_file):
        self.log_file = log_file
        self.entries = []

    def parse_file(self):
        """Reads and parses the log file."""
        with open(self.log_file, 'r') as file:
            for line in file:
                log_entry = LogEntry.parse_line(line.strip())
                if log_entry:
                    self.entries.append(log_entry)
                else:
                    print("Malformed Line: ", line.strip())

    def tally_by_log_level(self):
        """Counts log entries by log level."""
        return Counter(entry.log_level for entry in self.entries)

    def tally_by_service(self):
        """Counts log entries by service."""
        return Counter(entry.service_name for entry in self.entries)

    def most_common_error(self):
        """Finds the most common error message."""
        error_messages = [entry.message for entry in self.entries if entry.log_level == "ERROR"]
        return Counter(error_messages).most_common(1)

    def filter_by_date_range(self, start, end):
        """Filters log entries within a specified date range."""
        start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        matching_lines = []

        for entry in self.entries:
            try:
                entry_dt = datetime.strptime(entry.timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                entry_dt = datetime.strptime(entry.timestamp, "%Y-%m-%d")

            if entry_dt and start_dt <= entry_dt <= end_dt:
                # Process the entry within the date range
                matching_lines.append(f"{entry.timestamp} - {entry.service_name} - {entry.log_level} - {entry.message}")
        return matching_lines

    def generate_summary(self, output_format="console"):
        """Generates a summary of log analysis."""
        log_level_count = self.tally_by_log_level()
        service_count = self.tally_by_service()
        common_error = self.most_common_error()

        if output_format == "console":
            print("Log Summary:")
            print("Log Level Counts:", log_level_count)
            print("Service Counts:", service_count)
            if common_error:
                print("Most Common Error:", common_error)
        elif output_format == "csv":
            with open("log_summary.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Metric", "Value"])
                for level, count in log_level_count.items():
                    writer.writerow([f"Log Level - {level}", count])
                for service, count in service_count.items():
                    writer.writerow([f"Service - {service}", count])
                if common_error:
                    writer.writerow(["Most Common Error", common_error[0]])
        elif output_format == "json":
            import json
            summary = {
                "Log Level Counts": log_level_count,
                "Service Counts": service_count,
                "Most Common Error": common_error[0] if common_error else None
            }
            with open("log_summary.json", "w") as jsonfile:
                json.dump(summary, jsonfile, indent=4)

if __name__ == "__main__":
    analyzer = LogAnalyzer("app.log")
    analyzer.parse_file()

    # Output summary to console
    analyzer.generate_summary(output_format="console")

    # Bonus: Example of filtering by date range
    filtered_logs = analyzer.filter_by_date_range("2023-03-01 08:00:00", "2023-03-01 08:35:10")
    print("Filtered Logs:", filtered_logs)
