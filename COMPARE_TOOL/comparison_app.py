"""
File Comparison Tool - Main Application Class

The main application window and controller for the text comparison tool.
Manages the GUI layout, panels, and coordination between components.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Optional, Dict, Tuple

from similarity_matcher import SimilarityMatcher
from text_panel import LeftTextPanel, RightTextPanel
from file_manager import FileManager
import json
from settings_manager import SettingsManager


class ComparisonApp:
    """Main application class for the File Comparison Tool"""
    
    def __init__(self):
        self.root = None
        self.left_panel = None
        self.right_panel = None
        self.similarity_matcher = None
        self.file_manager = None
        self.settings_manager = SettingsManager()
        
        # Application state
        self.left_file_path = None
        self.right_file_path = None
        self.similarity_threshold = 0.8
        self.current_matches = {}
        self.highlighting_enabled = False  # Color coding disabled by default for performance
        self.matches_stale = False  # Track if matches need refresh
        self.synced_left_line = None
        self.synced_right_line = None
        self.is_syncing = False
        
        # Remove old find dialog state - now handled by individual panels
        pass
        
        # GUI components
        self.similarity_scale = None
        self.similarity_label = None
        self.status_left = None
        self.status_center = None
        self.status_right = None
        
        self.setup_application()

    
    def setup_application(self):
        """Initialize the complete application"""
        self.create_main_window()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_main_frame()
        self.setup_status_bar()
        self.setup_key_bindings()
        
        self.similarity_matcher = SimilarityMatcher(self.similarity_threshold)
        self.file_manager = FileManager(self)
        
        self._load_initial_settings()
    
    def _load_initial_settings(self):
        """Load settings from settings manager and apply them."""
        # Load file paths
        left_file = self.settings_manager.get_setting('files.left_file')
        right_file = self.settings_manager.get_setting('files.right_file')
        
        if left_file and os.path.exists(left_file):
            self.file_manager.load_file(left_file, 'left', auto_compare=False)
        if right_file and os.path.exists(right_file):
            self.file_manager.load_file(right_file, 'right', auto_compare=False)
            
        # Load similarity threshold
        saved_threshold = self.settings_manager.get_setting('comparison.similarity_threshold')
        if saved_threshold is not None:
            self.similarity_threshold = saved_threshold / 100.0  # Convert percentage to ratio
            self.similarity_scale.set(saved_threshold)
            self.similarity_matcher.set_threshold(self.similarity_threshold)

        # Load word wrap setting
        self.word_wrap_enabled = self.settings_manager.get_setting('ui.word_wrap', False)
        if self.word_wrap_enabled:
            self.btn_word_wrap.config(text="¶ Wrap ON")
        else:
            self.btn_word_wrap.config(text="¶ Word Wrap")
        if self.left_panel:
            self.left_panel.set_word_wrap(self.word_wrap_enabled)
        if self.right_panel:
            self.right_panel.set_word_wrap(self.word_wrap_enabled)
        
        # Perform initial comparison if files were loaded
        if self.left_file_path or self.right_file_path:
            self.refresh_comparison()
    
    def create_main_window(self):
        """Create and configure the main application window"""
        self.root = tk.Tk()
        self.root.title("File Comparison Tool")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)  # Main frame row
    
    def setup_menu(self):
        """Create the application menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Open Left File...", 
                             command=self.open_left_file,
                             accelerator="Ctrl+L")
        file_menu.add_command(label="Open Right File...", 
                             command=self.open_right_file,
                             accelerator="Ctrl+R")
        file_menu.add_separator()
        file_menu.add_command(label="Save Left File", 
                             command=self.save_left_file,
                             accelerator="Ctrl+S")
        file_menu.add_command(label="Save Right File", 
                             command=self.save_right_file,
                             accelerator="Ctrl+Shift+S")
        file_menu.add_command(label="Save Left As...", 
                             command=self.save_left_as)
        file_menu.add_command(label="Save Right As...", 
                             command=self.save_right_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit Menu
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="Find in Left Panel",
                             command=self.focus_search,
                             accelerator="Ctrl+F")
        edit_menu.add_command(label="Go to Line", 
                             command=self.show_goto_dialog,
                             accelerator="Ctrl+G")
        
        # View Menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        view_menu.add_command(label="Refresh Comparison", 
                             command=self.refresh_comparison,
                             accelerator="F5")
        
        # Add menus to menubar
        self.menubar.add_cascade(label="File", menu=file_menu)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        self.menubar.add_cascade(label="View", menu=view_menu)
    
    def setup_toolbar(self):
        """Create the application toolbar"""
        self.toolbar = tk.Frame(self.root, relief=tk.RAISED, bd=1)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        
        # File operation buttons
        btn_open_left = tk.Button(self.toolbar, text="📂 Left File", 
                                 command=self.open_left_file)
        btn_open_left.pack(side=tk.LEFT, padx=2)
        
        btn_open_right = tk.Button(self.toolbar, text="📂 Right File",
                                  command=self.open_right_file)
        btn_open_right.pack(side=tk.LEFT, padx=2)
        
        tk.Frame(self.toolbar, width=2, relief=tk.SUNKEN, bd=1).pack(
            side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Toggle button for color coding
        self.btn_toggle_colors = tk.Button(self.toolbar, text="🎨 Enable Colors",
                                          command=self.toggle_color_coding)
        self.btn_toggle_colors.pack(side=tk.LEFT, padx=2)
        
        # Sync button for scroll synchronization
        self.btn_sync = tk.Button(self.toolbar, text="🔗 Sync Scroll",
                                 command=self.toggle_sync_scroll)
        self.btn_sync.pack(side=tk.LEFT, padx=2)
        self.sync_scroll_enabled = False

        # Word wrap button
        self.btn_word_wrap = tk.Button(self.toolbar, text="¶ Word Wrap",
                                 command=self.toggle_word_wrap)
        self.btn_word_wrap.pack(side=tk.LEFT, padx=2)
        self.word_wrap_enabled = False
        
        tk.Frame(self.toolbar, width=2, relief=tk.SUNKEN, bd=1).pack(
            side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Similarity control
        similarity_frame = tk.Frame(self.toolbar)
        similarity_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(similarity_frame, text="Similarity %:").pack(side=tk.LEFT)
        
        # Slider for similarity threshold
        self.similarity_scale = tk.Scale(similarity_frame,
                                         from_=1,
                                         to=100,
                                         orient=tk.HORIZONTAL,
                                         command=self.on_similarity_scale_change,
                                         length=150) # Adjust length as needed
        self.similarity_scale.pack(side=tk.LEFT, padx=5)
        
        # Set initial threshold from settings
        initial_threshold_percent = int(self.similarity_threshold * 100)
        self.similarity_scale.set(initial_threshold_percent)
        
        # Don't bind events yet - will be bound after initialization completes
        
        # Refresh button
        btn_refresh = tk.Button(self.toolbar, text="🔄 Refresh", 
                               command=self.refresh_comparison)
        btn_refresh.pack(side=tk.RIGHT, padx=2)
    
    def setup_main_frame(self):
        """Create the main content area with dual panels"""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create paned window for resizable panels
        self.paned_window = tk.PanedWindow(self.main_frame, 
                                         orient=tk.HORIZONTAL, 
                                         sashrelief=tk.RAISED,
                                         sashwidth=8)
        self.paned_window.grid(row=0, column=0, sticky="nsew")
        
        # Create text panels
        self.left_panel = LeftTextPanel(self.paned_window, self)
        self.right_panel = RightTextPanel(self.paned_window, self)
        
        # Add panels to paned window
        self.paned_window.add(self.left_panel.frame, width=600)
        self.paned_window.add(self.right_panel.frame, width=600)
    
    def setup_status_bar(self):
        """Create the status bar"""
        self.status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        self.status_frame.grid(row=3, column=0, sticky="ew")
        
        self.status_left = tk.Label(self.status_frame, text="Ready", 
                                   anchor=tk.W, width=20)
        self.status_left.pack(side=tk.LEFT, padx=5)
        
        self.status_center = tk.Label(self.status_frame, 
                                     text="No files loaded", 
                                     anchor=tk.CENTER)
        self.status_center.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.status_right = tk.Label(self.status_frame, text="", 
                                    anchor=tk.E, width=20)
        self.status_right.pack(side=tk.RIGHT, padx=5)
    
    def setup_key_bindings(self):
        """Configure keyboard shortcuts"""
        self.root.bind('<Control-l>', lambda e: self.open_left_file())
        self.root.bind('<Control-r>', lambda e: self.open_right_file())
        self.root.bind('<Control-s>', lambda e: self.save_current_file())
        self.root.bind('<Control-f>', lambda e: self.focus_search())
        self.root.bind('<Control-g>', lambda e: self.show_goto_dialog())
        self.root.bind('<F5>', lambda e: self.refresh_comparison())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # File operations
    def open_left_file(self):
        """Open file in left panel"""
        filename = filedialog.askopenfilename(
            title="Open Left File",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("Markdown files", "*.md"),
                ("Log files", "*.log")
            ]
        )
        if filename:
            # Clear matches when new file is loaded
            self.current_matches = {}
            self.matches_stale = True
            self.file_manager.load_file(filename, 'left', auto_compare=False)
            self.settings_manager.set_setting('files.left_file', filename)
    
    def open_right_file(self):
        """Open file in right panel"""
        filename = filedialog.askopenfilename(
            title="Open Right File",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("Markdown files", "*.md"),
                ("Log files", "*.log")
            ]
        )
        if filename:
            # Clear matches when new file is loaded
            self.current_matches = {}
            self.matches_stale = True
            self.file_manager.load_file(filename, 'right', auto_compare=False)
            self.settings_manager.set_setting('files.right_file', filename)
    
    def save_left_file(self):
        """Save left panel content"""
        if self.left_file_path:
            self.file_manager.save_file(self.left_file_path, 'left')
        else:
            self.save_left_as()
    
    def save_right_file(self):
        """Save right panel content"""
        if self.right_file_path:
            self.file_manager.save_file(self.right_file_path, 'right')
        else:
            self.save_right_as()
    
    def save_left_as(self):
        """Save left panel content with new filename"""
        filename = filedialog.asksaveasfilename(
            title="Save Left File As",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("Markdown files", "*.md"),
                ("Log files", "*.log")
            ]
        )
        if filename:
            self.file_manager.save_file(filename, 'left')
            self.left_file_path = filename
    
    def save_right_as(self):
        """Save right panel content with new filename"""
        filename = filedialog.asksaveasfilename(
            title="Save Right File As",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("JSON files", "*.json"),
                ("XML files", "*.xml"),
                ("Markdown files", "*.md"),
                ("Log files", "*.log")
            ]
        )
        if filename:
            self.file_manager.save_file(filename, 'right')
            self.right_file_path = filename
    
    def save_current_file(self):
        """Save the currently focused file"""
        # Determine which panel has focus and save accordingly
        if self.left_panel and self.left_panel.text_widget.focus_get():
            self.save_left_file()
        else:
            self.save_right_file()
    
    def on_similarity_scale_change(self, value):
        """Handle similarity scale changes"""
        try:
            percent_value = int(value)
            self.similarity_threshold = percent_value / 100.0
            self.similarity_matcher.set_threshold(self.similarity_threshold)
            self.settings_manager.set_setting('comparison.similarity_threshold', percent_value)
            # Optionally refresh comparison immediately
            # self.refresh_comparison()
        except ValueError:
            pass
    
    def refresh_comparison(self):
        """Refresh the file comparison"""
        if self.left_panel and self.right_panel:
            left_content = self.left_panel.get_content()
            right_content = self.right_panel.get_content()
            
            if left_content or right_content:
                # Only do comparison when explicitly requested
                self.current_matches = self.similarity_matcher.compare_texts(
                    left_content, right_content)
                self.matches_stale = False
                self.update_panel_highlighting()
                self.update_status()
            else:
                # Clear matches if no content
                self.current_matches = {}
                self.matches_stale = False
                self.update_status()
    
    def mark_matches_stale(self):
        """Mark matches as needing refresh due to content changes"""
        self.matches_stale = True
        # Clear highlighting immediately when content changes
        if self.left_panel:
            self.left_panel.apply_match_highlighting({}, False)
        if self.right_panel:
            self.right_panel.apply_match_highlighting({}, False)
    
    def update_panel_highlighting(self):
        """Update highlighting in both panels based on matches"""
        if self.left_panel:
            self.left_panel.apply_match_highlighting(self.current_matches, self.highlighting_enabled)
        if self.right_panel:
            self.right_panel.apply_match_highlighting(self.current_matches, self.highlighting_enabled)
    
    def update_status(self):
        """Update status bar with comparison statistics"""
        if self.current_matches:
            total_lines = len(self.left_panel.get_lines()) if self.left_panel else 0
            matched_lines = len(self.current_matches)
            percentage = (matched_lines / total_lines * 100) if total_lines > 0 else 0
            
            self.status_center.config(
                text=f"Lines: {total_lines} | Matches: {matched_lines} ({percentage:.1f}%)")
        else:
            self.status_center.config(text="No comparison available")
    
    def find_and_sync_line(self, left_line_number, left_line_content):
        """Find and sync a single line based on similarity."""
        if not self.right_panel or not self.similarity_matcher:
            return

        right_lines = self.right_panel.get_lines()
        matches = self.similarity_matcher.find_all_matches_for_line(left_line_content, right_lines)

        if matches:
            # Select the best match
            best_match_line_num, best_similarity = matches[0]
            self.right_panel.select_line(best_match_line_num)

            # Store synced lines
            self.synced_left_line = left_line_number
            self.synced_right_line = best_match_line_num

            # Align the matched line with the selected line
            self.root.update_idletasks()
            left_line_info = self.left_panel.text_widget.dlineinfo(f"{left_line_number}.0")
            right_line_info = self.right_panel.text_widget.dlineinfo(f"{best_match_line_num}.0")

            if left_line_info and right_line_info:
                _, left_y, _, _, _ = left_line_info
                _, right_y, _, _, _ = right_line_info
                
                delta_y = right_y - left_y
                
                import tkinter.font as tkFont
                font = tkFont.Font(font=self.right_panel.text_font)
                font_height = font.metrics("linespace")
                
                if font_height > 0:
                    lines_to_scroll = int(round(delta_y / font_height))
                    self.right_panel.text_widget.yview_scroll(lines_to_scroll, "units")

            # Highlight other matches
            other_match_lines = [m[0] for m in matches[1:]]
            self.right_panel.highlight_matches(other_match_lines)

            self.update_status_message(f"{len(matches)} matches found. Best match on line {best_match_line_num} with {best_similarity:.2%} similarity.")
        else:
            self.right_panel.highlight_matches([]) # Clear highlights
            self.right_panel.select_line(-1) # Deselect
            self.update_status_message("No match found for selected line.")
            # Reset synced lines
            self.synced_left_line = None
            self.synced_right_line = None

    # Panel synchronization
    def sync_right_panel_to_line(self, left_line_number):
        """Synchronize right panel to show matching line"""
        if self.left_panel:
            lines = self.left_panel.get_lines()
            if 1 <= left_line_number <= len(lines):
                left_line_content = lines[left_line_number - 1]
                self.find_and_sync_line(left_line_number, left_line_content)

    def sync_right_panel_scroll(self, yview):
        """Sync right panel scroll position to keep selected lines aligned."""
        if self.is_syncing:
            return

        if self.right_panel and self.synced_left_line and self.synced_right_line:
            try:
                self.is_syncing = True
                
                # Calculate approximate top line for left panel based on yview fraction
                total_left_lines = len(self.left_panel.get_lines())
                if total_left_lines == 0: # Avoid division by zero
                    return
                top_left_line_approx = int(yview[0] * total_left_lines) + 1
                
                # Calculate offset from the synced line
                offset = top_left_line_approx - self.synced_left_line
                
                # Calculate target line for the right panel
                target_right_line = self.synced_right_line + offset
                
                # Clamp target_right_line to valid range
                total_right_lines = len(self.right_panel.get_lines())
                if total_right_lines == 0: # Avoid division by zero
                    return
                target_right_line = max(1, min(target_right_line, total_right_lines))
                
                # Convert target line to fraction for right panel
                target_fraction_right = (target_right_line - 1) / total_right_lines
                
                # Apply scroll to right panel
                self.right_panel.text_widget.yview_moveto(target_fraction_right)
                
            finally:
                self.is_syncing = False
        else:
            # Fallback to proportional scrolling if no lines are synced
            if self.right_panel:
                self.right_panel.text_widget.yview_moveto(yview[0])
    
    # Dialog windows
    def focus_search(self):
        """Focus on the search box of the currently active panel."""
        try:
            focused_widget = self.root.focus_get()
            
            # Determine which panel has focus
            if focused_widget:
                if self.left_panel and (focused_widget == self.left_panel.text_widget or focused_widget.winfo_parent() == self.left_panel.frame.winfo_parent()):
                    self.left_panel.search_entry.focus()
                    return "break"
                elif self.right_panel and (focused_widget == self.right_panel.text_widget or focused_widget.winfo_parent() == self.right_panel.frame.winfo_parent()):
                    self.right_panel.search_entry.focus()
                    return "break"

            # Fallback to left panel if no focus is identified
            if self.left_panel and hasattr(self.left_panel, 'search_entry'):
                self.left_panel.search_entry.focus()
                
        except Exception:
            # Fallback in case of any error
            if self.left_panel and hasattr(self.left_panel, 'search_entry'):
                self.left_panel.search_entry.focus()
                
        return "break"
    
    def show_goto_dialog(self):
        """Show go to line dialog"""
        # TODO: Implement goto dialog
        messagebox.showinfo("Go To Line", "Go to line functionality not yet implemented")
    
    def toggle_sync_scroll(self):
        """Toggle scroll synchronization"""
        self.sync_scroll_enabled = not self.sync_scroll_enabled
        
        # Update button text
        if self.sync_scroll_enabled:
            self.btn_sync.config(text="🔗 Sync ON")
        else:
            self.btn_sync.config(text="🔗 Sync Scroll")
        
        # Note: We don't change the right panel's sync_enabled here because
        # that controls line matching, not scroll synchronization.
        # Line matching should always work regardless of sync scroll setting.
    
        # Old find dialog methods removed - search now handled by individual panels
        pass

    def toggle_word_wrap(self):
        """Toggle word wrap on/off"""
        self.word_wrap_enabled = not self.word_wrap_enabled
        self.settings_manager.set_setting('ui.word_wrap', self.word_wrap_enabled)

        # Update button text
        if self.word_wrap_enabled:
            self.btn_word_wrap.config(text="¶ Wrap ON")
        else:
            self.btn_word_wrap.config(text="¶ Word Wrap")

        # Apply to both panels
        if self.left_panel:
            self.left_panel.set_word_wrap(self.word_wrap_enabled)
        if self.right_panel:
            self.right_panel.set_word_wrap(self.word_wrap_enabled)
    
    def update_status_message(self, message: str):
        """Update status bar message"""
        if hasattr(self, 'status_left') and self.status_left:
            self.status_left.config(text=message)
    
    def toggle_color_coding(self):
        """Toggle color coding on/off"""
        self.highlighting_enabled = not self.highlighting_enabled
        
        # Update button text
        if self.highlighting_enabled:
            self.btn_toggle_colors.config(text="🎨 Disable Colors")
        else:
            self.btn_toggle_colors.config(text="🎨 Enable Colors")
        
        # Update highlighting immediately
        self.update_panel_highlighting()
    
    def on_closing(self):
        """Handle application closing"""
        # Save settings before closing
        self.settings_manager.set_setting('files.left_file', self.left_file_path)
        self.settings_manager.set_setting('files.right_file', self.right_file_path)
        
        # Convert similarity threshold back to percentage for saving
        self.settings_manager.set_setting('comparison.similarity_threshold', 
                                         int(self.similarity_threshold * 100))
        self.settings_manager.save_settings()
        
        if self.check_unsaved_changes():
            self.root.quit()
            self.root.destroy()
    
    def check_unsaved_changes(self):
        """Check for unsaved changes before closing"""
        # TODO: Implement unsaved changes check
        return True
    
    def run(self):
        """Start the application"""
        self.root.deiconify()  # Show the window
        self.root.mainloop()