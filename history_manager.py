import json
import os
import datetime
from pathlib import Path

class HistoryManager:
    
    def __init__(self, history_dir='history'):
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create history directory if it doesn't exist
        self.history_dir = os.path.join(script_dir, history_dir)
        os.makedirs(self.history_dir, exist_ok=True)
    
    def save_daily_history(self, task_data):
        """Save task history for the current date
        
        Args:
            task_data (dict): Dictionary containing the task data to save
        """
        try:
            # Get today's date in YYYY-MM-DD format
            today = datetime.date.today().strftime('%Y-%m-%d')
            
            # Create filename based on date
            history_file = os.path.join(self.history_dir, f"history_{today}.json")
            
            # Make sure task_data has a task_name
            if 'task_name' not in task_data or not task_data['task_name']:
                task_data['task_name'] = "Unnamed Task"
                
            # Convert phase objects to dictionaries if needed
            if 'phases' in task_data and task_data['phases']:
                serializable_phases = []
                for phase in task_data['phases']:
                    if isinstance(phase, dict):
                        serializable_phases.append(phase)
                    else:
                        # For any non-dict objects
                        serializable_phases.append({
                            'name': getattr(phase, 'name', 'Unknown'),
                            'status': getattr(phase, 'status', 'Unknown'),
                            'cheated': getattr(phase, 'cheated', False)
                        })
                task_data['phases'] = serializable_phases
            
            # Check if file exists and load existing data
            existing_data = []
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        # If file is corrupted, start with empty list
                        existing_data = []
            
            # Add timestamp to this history entry
            now = datetime.datetime.now().strftime('%H:%M:%S')
            history_entry = {
                'timestamp': now,
                'phases': task_data.get('phases', []),
                'status': task_data.get('status', 'Completed'),
                'task_name': task_data.get('task_name', 'Unnamed Task')  # Ensure task_name is included
            }
            
            # Append new entry to existing data
            existing_data.append(history_entry)
            
            # Save updated history to file
            with open(history_file, 'w') as f:
                json.dump(existing_data, f, indent=4)
            
            # Print debug info
            print(f"History saved to {history_file}")
            print(f"Entry: {history_entry}")
            
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False
    
    def load_daily_history(self, date=None):
        """Load history for a specific date
        
        Args:
            date (str, optional): Date in 'YYYY-MM-DD' format. Defaults to today.
            
        Returns:
            list: List of history entries for the specified date
        """
        try:
            # If date not provided, use today
            if date is None:
                date = datetime.date.today().strftime('%Y-%m-%d')
            
            # Create filename based on date
            history_file = os.path.join(self.history_dir, f"history_{date}.json")
            
            # Check if file exists
            if not os.path.exists(history_file):
                return []
            
            # Load history from file
            with open(history_file, 'r') as f:
                history_data = json.load(f)
                
            # Ensure all entries have task_name (for legacy data)
            for i, entry in enumerate(history_data):
                if 'task_name' not in entry or not entry['task_name']:
                    entry['task_name'] = f"Task {i+1}"
            
            return history_data
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
    
    def get_available_dates(self):
        """Get list of dates that have history records
        
        Returns:
            list: List of dates in 'YYYY-MM-DD' format
        """
        try:
            dates = []
            for filename in os.listdir(self.history_dir):
                if filename.startswith('history_') and filename.endswith('.json'):
                    # Extract date from filename (format: history_YYYY-MM-DD.json)
                    date = filename[8:-5]  # Remove 'history_' prefix and '.json' suffix
                    dates.append(date)
            
            # Sort dates newest first
            dates.sort(reverse=True)
            return dates
        except Exception as e:
            print(f"Error getting available dates: {e}")
            return []