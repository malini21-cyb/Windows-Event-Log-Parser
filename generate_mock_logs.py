#!/usr/bin/env python3
"""
Generate Mock Windows Event Logs (CSV)
"""

import csv
import random
from datetime import datetime, timedelta

def generate_event_logs(output_file='event_logs.csv', num_events=1500):
    """Generate mock Windows event logs"""
    
    usernames = [
        'admin', 'john.doe', 'jane.smith', 'service_account',
        'backup_user', 'root', 'test_user', 'bob.johnson',
        'alice.williams', 'carlos.lopez', 'manager1', 'dba_user'
    ]
    
    sources = ['DC1', 'DC2', 'DC3', 'SERVER01', 'SERVER02', 
               'WORKSTATION01', 'WORKSTATION02', 'EXCHANGE01']
    
    reasons = [
        'Incorrect Password',
        'Account Locked Out',
        'Account Disabled',
        'Password Expired',
        'Logon Type Not Allowed',
    ]
    
    base_time = datetime.now() - timedelta(hours=48)
    events = []
    
    print(f"Generating {num_events} mock Windows Event Logs...")
    
    for i in range(num_events):
        if random.random() < 0.85:
            event_id = '4625'
            reason = random.choice(reasons)
        else:
            event_id = '4624'
            reason = 'Successful Logon'
        
        random_hours = random.randint(0, 47)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        timestamp = base_time + timedelta(hours=random_hours, minutes=random_minutes, seconds=random_seconds)
        
        if random.random() < 0.6:
            username = random.choice(['admin', 'john.doe', 'service_account'])
        else:
            username = random.choice(usernames)
        
        source = random.choice(sources)
        source_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 254)}"
        
        if event_id == '4625':
            message = f"Account Name: {username} | Source Network Address: {source_ip} | Reason: {reason} | Logon Type: 3"
        else:
            message = f"Account Name: {username} | Source Network Address: {source_ip} | Successful Logon | Logon Type: 3"
        
        events.append({
            'EventID': event_id,
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Source': source,
            'Message': message
        })
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['EventID', 'Timestamp', 'Source', 'Message'])
        writer.writeheader()
        writer.writerows(events)
    
    failed_count = sum(1 for e in events if e['EventID'] == '4625')
    success_count = sum(1 for e in events if e['EventID'] == '4624')
    
    print(f"\n✅ Generated mock event log: '{output_file}'")
    print(f"   Total events: {len(events)}")
    print(f"   Event 4625 (Failed Logons): {failed_count}")
    print(f"   Event 4624 (Successful): {success_count}")

if __name__ == "__main__":
    generate_event_logs()