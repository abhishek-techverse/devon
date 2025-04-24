# Devon Assignment

## Log File Analyzer

## Overview

The **Log File Analyzer** is a Python script (`log_analyzer.py`) designed to parse, analyze, and summarize application logs. 

---

## Features

1. **Log Parsing**:
   - Extracts essential components: `timestamp`, `service_name`, `log_level`, and `message`.
   - Handles malformed lines gracefully, logging or skipping them with meaningful warnings.

2. **Data Aggregation**:
   - Tally log entries by log level (`INFO`, `ERROR`, `WARN`, etc.).
   - Tally log entries by service name.
   - Identify the most common `ERROR` message.

3. **Summary Outputs**:
   - Prints a concise summary of log statistics.
   - Supports multiple output formats: console, CSV, and JSON.

4. **Date Range Filtering** (Bonus):
   - Filters log entries within a specified date/time range.
   - Returns only matching log lines for further analysis.

5. **Error Handling**:
   - Ensures robustness against unexpected or malformed log lines without crashing.

6. **Testing**:
   - Includes unit tests (using `pytest`) to confirm parsing logic and filtering functionality.

---

## Log File Format

Each log entry in the file (e.g., `app.log`) must follow the


### Example Logs:

```plaintext
2023-03-01 08:15:27 - ServiceA - INFO - Started processing request #123
2023-03-01 08:15:28 - ServiceB - ERROR - Null pointer exception
2023-03-01 08:15:29 - ServiceA - INFO - Completed request #123 in 2ms
```

---

## Assumptions

1. **Log Format Consistency**:
   - Each log entry follows the structure: `timestamp - service_name - log_level - message`.
   - Malformed lines (e.g., missing fields or invalid formatting) are handled gracefully. Such lines are logged or skipped without causing the script to crash.

2. **Timestamp Formats**:
   - The script supports two formats for timestamps:
     - `"%Y-%m-%d %H:%M:%S"` (date and time).
     - `"%Y-%m-%d"` (date-only).

3. **Error Handling**:
   - Invalid lines are excluded from analysis and printed for debugging purposes.
   - The script continues processing other valid lines seamlessly.

4. **Output Options**:
   - Results can be displayed in the console or saved in either CSV or JSON formats for further analysis.

---

## Installation

1. Clone the repository or download the `log_analyzer.py` script.
2. Ensure Python 3.7 or higher is installed on your machine.
3. Optionally, install `pytest` for running unit tests:
   ```
   pip install pytest
   ```
   
---

## Usage

1. **Run the Script**:
   - Place the log file (e.g., `app.log`) in the same directory as `log_analyzer.py`.
   - Execute the script by running:
     ```
     python log_analyzer.py
     ```

2. **Filter by Date Range** (Optional Bonus):
   - Use the date range filtering feature to extract logs within a specific time frame:
     ```python
     filtered_logs = analyzer.filter_by_date_range("2023-03-01 08:00:00", "2023-03-01 08:35:10")
     for log in filtered_logs:
         print(log)
     ```

3. **Run Unit Tests**:
   - To validate the functionality and parsing logic, execute the unit tests using `pytest`:
     ```
     pytest test_log_analyzer.py
     ```

---

## Outputs

### Console Output

```
Log Level Counts: {'INFO': 5, 'ERROR': 3, 'WARN': 2, 'DEBUG': 1} Service Counts: {'ServiceA': 3, 'ServiceB': 4, 'ServiceC': 2, 'ServiceD': 1, 'ServiceE': 1} Most Common Error: ('Null pointer exception', 2)
```

### CSV Output

```
Metric,Value
Log Level - INFO,5
Log Level - ERROR,3
Log Level - WARN,2
Log Level - DEBUG,1
Service - ServiceA,3
Service - ServiceB,4
Service - ServiceC,2
Service - ServiceD,1
Service - ServiceE,1
Most Common Error,Null pointer exception
```

---

### JSON Output

```
{
    "Log Level Counts": {
        "INFO": 5,
        "ERROR": 3,
        "WARN": 2,
        "DEBUG": 1
    },
    "Service Counts": {
        "ServiceA": 3,
        "ServiceB": 4,
        "ServiceC": 2,
        "ServiceD": 1,
        "ServiceE": 1
    },
    "Most Common Error": {
        "Null pointer exception": 2
    }
}
```