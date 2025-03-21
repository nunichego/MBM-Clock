import json
import os
from pathlib import Path

class SettingsManager:
    """Class to manage saving and loading application settings"""
    
    def __init__(self, settings_file='timer_settings.json'):
        """Initialize the settings manager with the settings file path"""
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create settings directory if it doesn't exist
        self.settings_dir = os.path.join(script_dir, 'settings')
        os.makedirs(self.settings_dir, exist_ok=True)
        
        # Set the full path to the settings file
        self.settings_file = os.path.join(self.settings_dir, settings_file)
    
    def save_settings(self, settings_data):
        """Save settings data to the settings file
        
        Args:
            settings_data (dict): Dictionary containing the settings to save
        """
        try:
            # Convert phase objects to dictionaries if present
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
        """Load settings from the settings file
        
        Returns:
            dict: Dictionary containing the loaded settings, or default settings if file not found
        """
        # Default settings
        default_settings = {
            'scale': 1.0,
            'phases': [
                {
                    'name': 'Phase',
                    'minutes': 30,
                    'seconds': 0,
                    'break_minutes': 5,
                    'break_seconds': 0
                }
            ]
        }
        
        try:
            # Check if settings file exists
            if not os.path.exists(self.settings_file):
                return default_settings
            
            # Load settings from file
            with open(self.settings_file, 'r') as f:
                settings_data = json.load(f)
            
            return settings_data
        except Exception as e:
            print(f"Error loading settings: {e}")
            return default_settings
    
    def _phase_to_dict(self, phase):
        """Convert a PhaseSettings object to a dictionary
        
        Args:
            phase (PhaseSettings): The phase object to convert
            
        Returns:
            dict: Dictionary representation of the phase
        """
        return {
            'name': phase.name,
            'minutes': phase.minutes,
            'seconds': phase.seconds,
            'break_minutes': phase.break_minutes,
            'break_seconds': phase.break_seconds
        }