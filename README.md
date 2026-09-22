# Windows Event Log Parser (Python)

**🚨 GraySentinel Global Cybersecurity Sprint - Day 1**

---

## 📋 Project Information

| Item | Details |
|------|---------|
| **Participant** | Malini |
| **Country** | India |
| **Team** | Blue Team |
| **Date** | September 22, 2026 |

---

## 🎯 Project Overview

A Python-based **Windows Event Log Parser** that analyzes mock security event logs to detect failed logon attempts (Event ID 4625). The tool identifies brute force attacks, extracts attacker source IPs, and generates risk-based threat reports.

**Core Skills Demonstrated:**
- Log parsing and data extraction
- Pattern detection for security threats
- Data aggregation and analysis
- Risk classification and ranking
- Multi-format reporting (CSV, JSON)

---

## 🔐 What is Event ID 4625?

**Event ID 4625** = Failed Logon Attempt

- Someone tries to log in but fails (wrong password)
- Indicates brute force attacks or credential stuffing
- SOC analysts use this to detect intrusion attempts

---

## ✨ Features

✅ Parse mock Windows Event Logs (CSV)  
✅ Extract Event ID 4625 (failed logons)  
✅ Count failures per user (identify targets)  
✅ Count failures per hour (identify attack windows)  
✅ Detect brute force patterns (>10 attempts)  
✅ Extract attacker source IPs  
✅ Export to CSV and JSON formats  
✅ Risk-level classification (CRITICAL/HIGH/MEDIUM/LOW)  

---

## 🚀 Quick Start

### Prerequisites
✓ Python 3.6+
✓ No external packages (uses standard library only)


### Run It

```bash
# Step 1: Generate mock event logs
python3 generate_mock_logs.py

# Step 2: Run the parser
python3 src/event_log_parser.py

# Step 3: Check results
ls -la results/
```

### Expected Output
✅ Successfully read 1500 total events
✅ Extracted 1278 Event ID 4625 events

📊 FAILED LOGONS BY USER:
admin: 309 attempts (CRITICAL)
service_account: 277 attempts (CRITICAL)
john.doe: 290 attempts (CRITICAL)

🚨 BRUTE FORCE ALERT:
⚠️ admin: 309 failed attempts - INVESTIGATE
⚠️ service_account: 277 failed attempts - INVESTIGATE


---

## 📁 Project Structure
Windows-Event-Log-Parser/
├── src/event_log_parser.py
├── generate_mock_logs.py
├── README.md
├── screenshots/
├── logs/
├── evidence/
└── results/


---

## 🔧 How It Works

1. **Read** → Load CSV file (1,500 events)
2. **Filter** → Keep only Event ID 4625 (1,276 events)
3. **Extract** → Get usernames, timestamps, IPs
4. **Aggregate** → Count by user and by hour
5. **Detect** → Alert if >10 failures per user
6. **Classify** → CRITICAL (>50) / HIGH (>25) / MEDIUM (>10) / LOW
7. **Export** → Save to CSV, JSON, and console report

---

## 📊 Understanding the Output

### Failed Logons by User
admin: 309 attempts (🔴 CRITICAL)
→ High-risk account being attacked
→ Action: Reset password, check for compromise

### Failed Logons by Hour



---

## 📈 Exported Results

### failed_logons_by_user.csv
```csv
Username,Failed_Logon_Count,Risk_Level
admin,309,CRITICAL
service_account,277,CRITICAL
john.doe,290,CRITICAL
```

### failed_logons_by_hour.csv
```csv
Timestamp,Failed_Logon_Count
2024-09-22 14:00,145
2024-09-22 15:00,132
```

### analysis_summary.json
```json
{
  "total_events": 1278,
  "unique_users": 12,
  "top_user": ["admin", 309]
}

---

## 👤 Author

**Malini**
- GraySentinel Sprint 2026 - Day 1
- 📅 September 22, 2026

