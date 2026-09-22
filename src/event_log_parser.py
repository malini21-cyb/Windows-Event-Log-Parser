import csv
import re
from datetime import datetime
from collections import defaultdict

# ============================================
# WINDOWS EVENT LOG PARSER - Event ID 4625
# ============================================

class EventLogParser:
    """Parse Windows Event Logs and analyze failed logon attempts"""
    
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.events = []
        self.failed_logons = []
    
    def read_log(self):
        """Read the CSV log file"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.events = list(reader)
            print(f"✓ Successfully read {len(self.events)} total events")
        except FileNotFoundError:
            print(f"✗ Error: File '{self.csv_file}' not found")
            return False
        return True
    
    def filter_event_4625(self):
        """
        Extract only Event ID 4625 (failed logon attempts)
        Event 4625 = failed logon
        """
        self.failed_logons = [
            event for event in self.events 
            if event.get('EventID', '').strip() == '4625'
        ]
        print(f"✓ Filtered {len(self.failed_logons)} Event ID 4625 events (failed logons)")
        return len(self.failed_logons)
    
    def extract_username(self, message):
        """
        Extract username from the message field
        Windows Event 4625 messages typically contain:
        "Account Name: username" or similar patterns
        """
        # Common patterns in Windows security logs
        patterns = [
            r'Account Name:\s*(\S+)',  # "Account Name: john.doe"
            r'Target Account Name:\s*(\S+)',
            r'User:\s*(\S+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                username = match.group(1).strip()
                # Remove common padding or special chars
                return username if username != '-' else 'UNKNOWN'
        
        return 'UNKNOWN'
    
    def parse_timestamp(self, timestamp_str):
        """
        Parse timestamp and extract hour
        Supports common Windows log formats:
        - "2024-01-15 14:32:45"
        - "1/15/2024 2:32:45 PM"
        """
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%Y %I:%M:%S %p',
            '%Y-%m-%d %H:%M',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(timestamp_str.strip(), fmt)
                return dt
            except ValueError:
                continue
        
        print(f"⚠ Warning: Could not parse timestamp '{timestamp_str}'")
        return None
    
    def count_per_user(self):
        """Generate failed logon count per user"""
        user_count = defaultdict(int)
        
        for event in self.failed_logons:
            username = self.extract_username(event.get('Message', ''))
            user_count[username] += 1
        
        return dict(sorted(user_count.items(), key=lambda x: x[1], reverse=True))
    
    def count_per_hour(self):
        """Generate failed logon count per hour"""
        hour_count = defaultdict(int)
        
        for event in self.failed_logons:
            timestamp_str = event.get('Timestamp', '')
            dt = self.parse_timestamp(timestamp_str)
            
            if dt:
                # Format as "YYYY-MM-DD HH:00"
                hour_key = dt.strftime('%Y-%m-%d %H:00')
                hour_count[hour_key] += 1
        
        return dict(sorted(hour_count.items()))
    
    def generate_summary(self):
        """Generate and display the full summary report"""
        print("\n" + "="*60)
        print("EVENT LOG ANALYSIS SUMMARY - Event ID 4625 (Failed Logons)")
        print("="*60)
        
        # Count per user
        user_stats = self.count_per_user()
        print(f"\n📊 FAILED LOGONS BY USER (Top 10):")
        print("-" * 40)
        
        if user_stats:
            for idx, (user, count) in enumerate(list(user_stats.items())[:10], 1):
                print(f"{idx:2}. {user:30} : {count:4} attempts")
        else:
            print("No data available")
        
        # Count per hour
        hour_stats = self.count_per_hour()
        print(f"\n⏰ FAILED LOGONS BY HOUR:")
        print("-" * 40)
        
        if hour_stats:
            for hour, count in hour_stats.items():
                print(f"{hour} : {count:4} attempts")
        else:
            print("No data available")
        
        # Summary stats
        print(f"\n📈 SUMMARY STATISTICS:")
        print("-" * 40)
        total_failed = len(self.failed_logons)
        total_users = len(user_stats)
        
        print(f"Total Event ID 4625 events: {total_failed}")
        print(f"Unique users with failures: {total_users}")
        
        if user_stats:
            top_user = list(user_stats.items())[0]
            print(f"Top target user: {top_user[0]} ({top_user[1]} attempts)")
        
        if hour_stats:
            peak_hour = max(hour_stats.items(), key=lambda x: x[1])
            print(f"Peak attack hour: {peak_hour[0]} ({peak_hour[1]} attempts)")
        
        print("\n" + "="*60)
    
    def export_to_csv(self, output_file):
        """Export summary results to CSV"""
        user_stats = self.count_per_user()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Failed_Logon_Count'])
            for user, count in user_stats.items():
                writer.writerow([user, count])
        
        print(f"\n✓ Results exported to '{output_file}'")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Initialize parser with your CSV file
    parser = EventLogParser('event_logs.csv')  # Change this to your file name
    
    # Step-by-step execution
    if parser.read_log():
        parser.filter_event_4625()
        parser.generate_summary()
        
        # Optional: Export to CSV
        parser.export_to_csv('failed_logons_summary.csv')