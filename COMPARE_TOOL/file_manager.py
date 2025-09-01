"""
File Comparison Tool - File Manager

Handles file I/O operations including loading and saving text files
for both left and right panels.
"""

import os
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False


class FileManager:
    """Manages file operations for the comparison tool"""
    
    def __init__(self, app_controller):
        self.app = app_controller
        self.left_file_encoding = 'utf-8'
        self.right_file_encoding = 'utf-8'
        
    def load_file(self, filepath: str, panel: str, auto_compare: bool = True) -> bool:
        """
        Load file content into specified panel
        
        Args:
            filepath: Path to file to load
            panel: 'left' or 'right'
            auto_compare: Whether to automatically trigger comparison after loading
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Detect encoding
            encoding = self.detect_encoding(filepath)
            
            # Read file content
            with open(filepath, 'r', encoding=encoding) as file:
                content = file.read()
            
            # Get the appropriate panel
            target_panel = self.app.left_panel if panel == 'left' else self.app.right_panel
            
            if target_panel:
                # Set content in panel
                target_panel.set_content(content)
                
                # Update panel title with filename
                filename = os.path.basename(filepath)
                if panel == 'left':
                    target_panel.set_title(f"Left File: {filename}")
                    self.app.left_file_path = filepath
                    self.left_file_encoding = encoding
                else:
                    target_panel.set_title(f"Right File: {filename}")
                    self.app.right_file_path = filepath
                    self.right_file_encoding = encoding
                
                # Update status
                self.update_status(f"Loaded {filename}")
                
                # Trigger comparison refresh only if requested
                if auto_compare:
                    self.app.refresh_comparison()
                
                return True
            
        except Exception as e:
            error_msg = f"Error loading file {filepath}: {str(e)}"
            messagebox.showerror("File Load Error", error_msg)
            self.update_status(f"Failed to load file: {str(e)}")
            
        return False
    
    def save_file(self, filepath: str, panel: str) -> bool:
        """
        Save panel content to file
        
        Args:
            filepath: Path where to save file
            panel: 'left' or 'right'
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the appropriate panel
            source_panel = self.app.left_panel if panel == 'left' else self.app.right_panel
            
            if not source_panel:
                return False
            
            # Get content from panel
            content = source_panel.get_content()
            
            # Determine encoding
            encoding = self.left_file_encoding if panel == 'left' else self.right_file_encoding
            
            # Create backup if file exists
            if os.path.exists(filepath):
                self.create_backup(filepath)
            
            # Write file content
            with open(filepath, 'w', encoding=encoding) as file:
                file.write(content)
            
            # Update panel title
            filename = os.path.basename(filepath)
            if panel == 'left':
                source_panel.set_title(f"Left File: {filename}")
                self.app.left_file_path = filepath
            else:
                source_panel.set_title(f"Right File: {filename}")
                self.app.right_file_path = filepath
            
            # Update status
            self.update_status(f"Saved {filename}")
            
            # Mark file as not modified
            if hasattr(self.app, 'set_file_modified'):
                self.app.set_file_modified(panel, False)
            
            return True
            
        except Exception as e:
            error_msg = f"Error saving file {filepath}: {str(e)}"
            messagebox.showerror("File Save Error", error_msg)
            self.update_status(f"Failed to save file: {str(e)}")
            
        return False
    
    def detect_encoding(self, filepath: str) -> str:
        """
        Detect file encoding
        
        Args:
            filepath: Path to file
            
        Returns:
            Detected encoding string
        """
        try:
            # Read raw bytes to detect encoding
            with open(filepath, 'rb') as file:
                raw_data = file.read()
            
            if HAS_CHARDET:
                # Use chardet to detect encoding
                result = chardet.detect(raw_data)
                
                if result['encoding']:
                    confidence = result['confidence']
                    detected_encoding = result['encoding']
                    
                    # If confidence is low, fall back to common encodings
                    if confidence < 0.7:
                        # Try common encodings
                        for encoding in ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']:
                            try:
                                raw_data.decode(encoding)
                                return encoding
                            except UnicodeDecodeError:
                                continue
                    
                    return detected_encoding
            else:
                # Fallback when chardet is not available
                for encoding in ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']:
                    try:
                        raw_data.decode(encoding)
                        return encoding
                    except UnicodeDecodeError:
                        continue
            
        except Exception:
            pass
        
        # Default to utf-8
        return 'utf-8'
    
    def create_backup(self, filepath: str):
        """
        Create backup of existing file
        
        Args:
            filepath: Path to file to backup
        """
        try:
            backup_path = filepath + '.backup'
            counter = 1
            
            # Find unique backup name
            while os.path.exists(backup_path):
                backup_path = f"{filepath}.backup{counter}"
                counter += 1
            
            # Copy file to backup
            with open(filepath, 'rb') as src:
                with open(backup_path, 'wb') as dst:
                    dst.write(src.read())
                    
        except Exception:
            pass  # Backup failed, but don't stop save operation
    
    def update_status(self, message: str):
        """Update application status"""
        if hasattr(self.app, 'status_left') and self.app.status_left:
            self.app.status_left.config(text=message)
    
    def get_file_info(self, filepath: str) -> Optional[dict]:
        """
        Get file information
        
        Args:
            filepath: Path to file
            
        Returns:
            Dictionary with file info or None
        """
        try:
            if not os.path.exists(filepath):
                return None
            
            stat = os.stat(filepath)
            
            return {
                'name': os.path.basename(filepath),
                'path': filepath,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'encoding': self.detect_encoding(filepath)
            }
            
        except Exception:
            return None
    
    def validate_file_access(self, filepath: str, mode: str = 'r') -> Tuple[bool, str]:
        """
        Validate file access permissions
        
        Args:
            filepath: Path to file
            mode: Access mode ('r' for read, 'w' for write)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            if mode == 'r':
                if not os.path.exists(filepath):
                    return False, "File does not exist"
                
                if not os.access(filepath, os.R_OK):
                    return False, "No read permission"
                    
            elif mode == 'w':
                # Check if directory exists and is writable
                directory = os.path.dirname(filepath)
                
                if not os.path.exists(directory):
                    return False, "Directory does not exist"
                
                if not os.access(directory, os.W_OK):
                    return False, "No write permission to directory"
                
                # If file exists, check write permission
                if os.path.exists(filepath) and not os.access(filepath, os.W_OK):
                    return False, "No write permission to file"
            
            return True, ""
            
        except Exception as e:
            return False, str(e)
    
    def is_text_file(self, filepath: str) -> bool:
        """
        Check if file appears to be a text file
        
        Args:
            filepath: Path to file
            
        Returns:
            True if appears to be text file
        """
        try:
            # Check file extension
            ext = os.path.splitext(filepath)[1].lower()
            text_extensions = {
                '.txt', '.md', '.py', '.js', '.html', '.css', '.json',
                '.xml', '.csv', '.log', '.cfg', '.ini', '.yaml', '.yml',
                '.sql', '.sh', '.bat', '.ps1', '.c', '.cpp', '.h',
                '.java', '.php', '.rb', '.go', '.rs', '.swift', '.kt'
            }
            
            if ext in text_extensions:
                return True
            
            # Try to read as text and check for binary content
            with open(filepath, 'rb') as file:
                chunk = file.read(1024)
                
            # Check for null bytes (common in binary files)
            if b'\0' in chunk:
                return False
            
            # Try to decode as text
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                # Try other encodings
                for encoding in ['latin1', 'cp1252']:
                    try:
                        chunk.decode(encoding)
                        return True
                    except UnicodeDecodeError:
                        continue
            
            return False
            
        except Exception:
            return False
    
    def get_recent_files(self) -> list:
        """
        Get list of recently accessed files
        (Placeholder for future implementation)
        
        Returns:
            List of recent file paths
        """
        # TODO: Implement recent files tracking
        return []
    
    def add_to_recent_files(self, filepath: str):
        """
        Add file to recent files list
        (Placeholder for future implementation)
        
        Args:
            filepath: Path to file to add
        """
        # TODO: Implement recent files tracking
        pass