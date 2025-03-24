import json
import os
from pathlib import Path

class SettingsManager: 
    def __init__(self, settings_file='timer_settings.json'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.settings_dir = os.path.join(script_dir, 'settings')
        os.makedirs(self.settings_dir, exist_ok=True)
        
        # Set the full path to the settings file
        self.settings_file = os.path.join(self.settings_dir, settings_file)
    
    def save_settings(self, settings_data):
        try:
            if 'phases' in settings_data and settings_data['phases']:
                settings_data['phases'] = [self._phase_to_dict(phase) for phase in settings_data['phases']]
            
            # Save settings to file
            with open(self.settings_file, 'w') as f:
                json.dump(settings_data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def load_settings(self):
        default_settings = {
            'scale': 1.0,
            'phases': [
                {
                    'name': 'Phase',
                    'minutes': 30,
                    'seconds': 0
                }
            ]
        }
        
        try:
            if not os.path.exists(self.settings_file):
                return default_settings
            
            with open(self.settings_file, 'r') as f:
                settings_data = json.load(f)
            
            return settings_data
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def _phase_to_dict(self, phase):
        return {
            'name': phase.name,
            'minutes': phase.minutes,
            'seconds': phase.seconds
        }