#!/usr/bin/env python3
"""
File Comparison Tool - Main Entry Point

A Python application for comparing two text files with:
- Side-by-side dual panel interface
- Configurable similarity matching
- Synchronized scrolling
- Text editing capabilities
- File save functionality
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comparison_app import ComparisonApp


def main():
    """Main application entry point"""
    try:
        # Create and configure root window
        root = tk.Tk()
        root.withdraw()  # Hide root initially
        
        # Create application instance
        app = ComparisonApp()
        
        # Start application
        app.run()
        
    except ImportError as e:
        messagebox.showerror("Import Error", 
                           f"Failed to import required modules: {e}")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("Application Error", 
                           f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()