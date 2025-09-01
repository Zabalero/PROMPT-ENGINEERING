"""
File Comparison Tool - Settings Manager

Handles loading and saving application settings to a JSON file.
"""

import json
import os
from typing import Dict, Any

class SettingsManager:
    """Manages application settings."""

    def __init__(self, settings_file: str = 'settings.json'):
        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """Loads settings from the JSON file or returns default settings."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {self.settings_file}. Using default settings.")
                return self._get_default_settings()
            except Exception as e:
                print(f"Error loading settings from {self.settings_file}: {e}. Using default settings.")
                return self._get_default_settings()
        return self._get_default_settings()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Returns the default application settings."""
        return {
            "files": {
                "left_file": "",
                "right_file": "",
                "recent_files": []
            },
            "comparison": {
                "similarity_threshold": 50,
                "auto_refresh": True,
                "highlight_matches": True,
                "highlighting_enabled": False
            },
            "window": {
                "geometry": "1200x800",
                "panel_split": 0.5,
                "maximized": False
            },
            "ui": {
                "font_family": "Consolas",
                "font_size": 10,
                "show_line_numbers": True,
                "word_wrap": False,
                "theme": "default"
            }
        }

    def save_settings(self):
        """Saves the current settings to the JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings to {self.settings_file}: {e}")

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Retrieves a setting value using a dot-separated key (e.g., 'files.left_file')."""
        parts = key.split('.')
        current = self.settings
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def set_setting(self, key: str, value: Any):
        """Sets a setting value using a dot-separated key (e.g., 'files.left_file')."""
        parts = key.split('.')
        current = self.settings
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                if isinstance(current, dict):
                    current[part] = value
                else:
                    print(f"Warning: Cannot set '{key}'. Path is not a dictionary at '{'.'.join(parts[:i])}'.")
                    return
            else:
                if isinstance(current, dict) and part in current and isinstance(current[part], dict):
                    current = current[part]
                elif isinstance(current, dict):
                    current[part] = {}
                    current = current[part]
                else:
                    print(f"Warning: Cannot set '{key}'. Path is not a dictionary at '{'.'.join(parts[:i])}'.")
                    return

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    # Create a temporary settings file for testing
    temp_settings_file = "test_settings.json"
    if os.path.exists(temp_settings_file):
        os.remove(temp_settings_file)

    manager = SettingsManager(temp_settings_file)
    print("Initial settings:", manager.settings)

    # Test getting default settings
    print("Default left file:", manager.get_setting('files.left_file'))
    print("Default similarity threshold:", manager.get_setting('comparison.similarity_threshold'))

    # Test setting values
    manager.set_setting('files.left_file', '/path/to/my/left_file.txt')
    manager.set_setting('files.right_file', '/path/to/my/right_file.txt')
    manager.set_setting('comparison.similarity_threshold', 75)
    manager.set_setting('window.geometry', '1024x768')

    print("Modified left file:", manager.get_setting('files.left_file'))
    print("Modified similarity threshold:", manager.get_setting('comparison.similarity_threshold'))

    # Save settings
    manager.save_settings()
    print("Settings saved.")

    # Load settings again to verify
    new_manager = SettingsManager(temp_settings_file)
    print("Loaded left file:", new_manager.get_setting('files.left_file'))
    print("Loaded similarity threshold:", new_manager.get_setting('comparison.similarity_threshold'))

    # Clean up
    if os.path.exists(temp_settings_file):
        os.remove(temp_settings_file)
        print(f"Cleaned up {temp_settings_file}")