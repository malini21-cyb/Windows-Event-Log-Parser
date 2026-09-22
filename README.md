# Windows Event Log Parser (Python)

**GraySentinel Global Cybersecurity Sprint - Day 1**  
**Participant:** Malini  
**Country:** India  
**Team:** Blue Team  

## Project Overview

A Python script that analyzes Windows Event Logs to detect failed logon attempts (Event ID 4625).

## Features

✅ Parse mock Windows Event Log (CSV format)  
✅ Extract Event ID 4625 (failed logon events)  
✅ Count failed logons per user  
✅ Count failed logons per hour  
✅ Detect brute force attacks (>10 failures)  
✅ Identify source IPs  
✅ Export to CSV and JSON  

## Quick Start

```bash
# 1. Generate mock event logs
python3 generate_mock_logs.py

# 2. Run the parser
python3 src/event_log_parser.py
```

## Expected Output