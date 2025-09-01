"""
File Comparison Tool - Text Panel Components

Implements the left and right text panels with line numbers, highlighting,
synchronized scrolling, and click-to-navigate functionality.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable

from custom_text import TextEditorWithLineNumbers


class BaseTextPanel:
    """Base class for text panels with common functionality"""
    
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.frame = None
        self.text_widget = None  # This will be the TextEditorWithLineNumbers instance
        self.h_scrollbar = None
        self.current_line = 1
        self.lines_cache = []
        self._search_timer = None
        
        self.setup_panel()
        self.configure_tags()
        self.setup_events()
    
    def setup_panel(self):
        """Create the panel frame and components"""
        self.frame = tk.Frame(self.parent)
        
        # Header frame with title and search
        self.header = tk.Frame(self.frame, bg='lightgray', height=50)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        # Title row
        title_frame = tk.Frame(self.header, bg='lightgray')
        title_frame.pack(fill=tk.X, pady=2)
        
        self.title_label = tk.Label(title_frame, text="", bg='lightgray', font=('Arial', 10, 'bold'))
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        # Search row
        search_frame = tk.Frame(self.header, bg='lightgray')
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(search_frame, text="Find:", bg='lightgray', font=('Arial', 9)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 9))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Bind search events
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        self.search_entry.bind('<Return>', self.find_next_match)
        self.search_entry.bind('<Shift-Return>', self.find_previous_match)
        
        # Search state
        self.search_results = []
        self.current_search_index = -1
        
        # Text area frame
        self.text_frame = tk.Frame(self.frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)
        
        # Define font
        self.text_font = ('Courier New', 10, 'normal')
        
        # Create the custom text widget
        self.text_widget = TextEditorWithLineNumbers(
            self.text_frame,
            wrap=tk.NONE,
            undo=True,
            maxundo=50,
            font=self.text_font,
            spacing1=0,
            spacing2=0,
            spacing3=0,
            selectbackground='#316AC5',
            selectforeground='white',
            insertbackground='black',
            bg='white',
            fg='black',
            exportselection=False,
            scroll_callback=self.on_text_scroll
        )
        self.text_widget.grid(row=0, column=0, sticky='nsew')

        # Horizontal Scrollbar
        self.h_scrollbar = tk.Scrollbar(self.text_frame, orient=tk.HORIZONTAL, command=self.text_widget.text.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.text_widget.text.configure(xscrollcommand=self.h_scrollbar.set)

    def configure_tags(self):
        """Configure text highlighting tags"""
        self.text_widget.tag_config('exact_match', background='#d4edda', foreground='#155724')
        self.text_widget.tag_config('high_match', background='#d1ecf1', foreground='#0c5460')
        self.text_widget.tag_config('medium_match', background='#fff3cd', foreground='#856404')
        self.text_widget.tag_config('low_match', background='#f8d7da', foreground='#721c24')
        self.text_widget.tag_config('no_match', background='#e2e3e5', foreground='#383d41')
        self.text_widget.tag_config('selected_line', background='#007bff', foreground='white')
        self.text_widget.tag_config('sync_highlight', background='#ffc107', foreground='#212529')
        self.text_widget.tag_config('search_result', background='#ffff99', foreground='#000000')
        self.text_widget.tag_config('current_search', background='#ff6600', foreground='#ffffff')
        self.text_widget.tag_config('multi_match', background='#ADD8E6', foreground='#000000')

    def setup_events(self):
        """Setup event handlers"""
        self.text_widget.text.bind('<KeyRelease>', self.on_text_changed)
        self.text_widget.text.bind('<Button-1>', self.on_cursor_moved)

    def on_text_scroll(self, yview):
        if hasattr(self.app, 'sync_scroll_enabled') and self.app.sync_scroll_enabled:
            if isinstance(self, LeftTextPanel):
                self.app.sync_right_panel_scroll(yview)

    def on_text_changed(self, event=None):
        """Handle text modifications"""
        self.update_lines_cache()

        if hasattr(self.app, 'mark_matches_stale'):
            self.app.mark_matches_stale()

        if hasattr(self.app, 'set_file_modified'):
            panel_name = 'left' if isinstance(self, LeftTextPanel) else 'right'
            self.app.set_file_modified(panel_name, True)

    def on_cursor_moved(self, event):
        """Handle cursor movement"""
        self.app.root.after_idle(self.update_current_line)

        if isinstance(self, LeftTextPanel):
            self.app.root.after_idle(self.on_text_click)

    def on_text_click(self):
        """Handle clicks anywhere in the text widget for left panel"""
        if not isinstance(self, LeftTextPanel):
            return

        cursor_pos = self.text_widget.index(tk.INSERT)
        line_number = int(cursor_pos.split('.')[0])

        self.select_line(line_number)

    def update_current_line(self):
        """Update current line tracking"""
        cursor_pos = self.text_widget.index(tk.INSERT)
        line_number = int(cursor_pos.split('.')[0])

        if line_number != self.current_line:
            self.current_line = line_number

    def select_line(self, line_number):
        """Select and highlight a specific line"""
        if line_number < 1:
            return

        self.current_line = line_number

        self.text_widget.tag_remove('selected_line', '1.0', tk.END)
        self.text_widget.tag_remove(tk.SEL, '1.0', tk.END)

        start = f"{line_number}.0"
        end = f"{line_number}.end+1c"

        try:
            self.text_widget.tag_add('selected_line', start, end)
            self.text_widget.see(start)
            self.text_widget.mark_set(tk.INSERT, start)
        except tk.TclError:
            pass

    def on_search_change(self, event=None):
        """Handle search text changes with debouncing"""
        if event and event.keysym in ("Return", "Shift_L", "Shift_R"):
            return

        if self._search_timer:
            self.app.root.after_cancel(self._search_timer)

        self._search_timer = self.app.root.after(250, self._perform_search)

    def _perform_search(self):
        """Perform the actual search"""
        search_text = self.search_entry.get().strip()

        self.text_widget.tag_remove('search_result', '1.0', tk.END)
        self.text_widget.tag_remove('current_search', '1.0', tk.END)
        self.search_results = []
        self.current_search_index = -1

        if not search_text:
            return

        content = self.get_content()
        lines = content.split('\n')

        for line_num, line_text in enumerate(lines, 1):
            line_lower = line_text.lower()
            search_lower = search_text.lower()

            start_pos = 0
            while True:
                pos = line_lower.find(search_lower, start_pos)
                if pos == -1:
                    break

                self.search_results.append({
                    'line': line_num,
                    'start': pos,
                    'end': pos + len(search_text),
                    'text': line_text[pos:pos + len(search_text)]
                })

                start_index = f"{line_num}.{pos}"
                end_index = f"{line_num}.{pos + len(search_text)}"
                self.text_widget.tag_add('search_result', start_index, end_index)

                start_pos = pos + 1

        if self.search_results:
            self.current_search_index = 0
            self.highlight_current_match()

        self.app.root.update_idletasks()

    def find_next_match(self, event=None):
        """Find next search match"""
        if not self.search_results:
            return

        if self.current_search_index < len(self.search_results) - 1:
            self.current_search_index += 1
            self.highlight_current_match()

        return "break"

    def find_previous_match(self, event=None):
        """Find previous search match"""
        if not self.search_results:
            return

        if self.current_search_index > 0:
            self.current_search_index -= 1
            self.highlight_current_match()

        return "break"

    def highlight_current_match(self):
        """Highlight the current search match"""
        if not self.search_results or self.current_search_index < 0:
            return

        self.text_widget.tag_remove('current_search', '1.0', tk.END)

        result = self.search_results[self.current_search_index]
        start_index = f"{result['line']}.{result['start']}"
        end_index = f"{result['line']}.{result['end']}"
        self.text_widget.tag_add('current_search', start_index, end_index)

        self.scroll_to_line(result['line'], center_view=False)
        self.app.root.update_idletasks()

    def update_lines_cache(self):
        """Update internal lines cache"""
        content = self.text_widget.get('1.0', tk.END)
        self.lines_cache = content.splitlines()

    def get_content(self) -> str:
        """Get all text content"""
        return self.text_widget.get('1.0', 'end-1c')

    def set_content(self, content: str):
        """Set text content"""
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', content)
        self.update_lines_cache()

    def get_lines(self) -> List[str]:
        """Get lines as list"""
        return self.lines_cache

    def set_title(self, title: str):
        """Set panel title"""
        self.title_label.config(text=title)

    def set_word_wrap(self, enabled: bool):
        """Enable or disable word wrap"""
        if enabled:
            self.text_widget.text.config(wrap=tk.WORD)
        else:
            self.text_widget.text.config(wrap=tk.NONE)

    def apply_match_highlighting(self, matches: Dict, enable_highlighting: bool = True):
        """Apply color coding based on similarity matches"""
        for tag in ['exact_match', 'high_match', 'medium_match', 'low_match', 'no_match']:
            self.text_widget.tag_remove(tag, '1.0', tk.END)

        if not enable_highlighting:
            return

        line_count = len(self.lines_cache)

        for line_num in range(1, line_count + 1):
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"

            try:
                if line_num in matches:
                    match_type = matches[line_num]['match_type']

                    if match_type == 'exact':
                        tag = 'exact_match'
                    elif match_type == 'high':
                        tag = 'high_match'
                    elif match_type == 'medium':
                        tag = 'medium_match'
                    else:
                        tag = 'low_match'
                else:
                    tag = 'no_match'

                self.text_widget.tag_add(tag, line_start, line_end)
            except tk.TclError:
                pass

    def scroll_to_line(self, line_number: int, center_view: bool = True):
        """Scroll to show specific line"""
        if line_number < 1:
            return

        line_index = f"{line_number}.0"

        try:
            if center_view:
                visible_lines = self.get_visible_line_range()
                if visible_lines:
                    viewport_height = visible_lines[1] - visible_lines[0]
                    center_offset = viewport_height // 2
                    center_line = max(1, line_number - center_offset)
                    self.text_widget.yview(f"{center_line}.0")
                else:
                    self.text_widget.see(line_index)
            else:
                self.text_widget.see(line_index)

        except tk.TclError:
            pass

    def get_visible_line_range(self) -> Optional[tuple]:
        """Get currently visible line range"""
        try:
            top_line = int(self.text_widget.index("@0,0").split('.')[0])
            bottom_line = int(self.text_widget.index(f"@0,{self.text_widget.winfo_height()}").split('.')[0])
            return (top_line, bottom_line)
        except (tk.TclError, ValueError):
            return None


class LeftTextPanel(BaseTextPanel):
    """Left text panel - main panel that controls synchronization"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, app_controller)
        self.set_title("Left File (Main)")

    def select_line(self, line_number):
        """Select line and trigger synchronization"""
        super().select_line(line_number)

        if hasattr(self.app, 'sync_right_panel_to_line'):
            self.app.sync_right_panel_to_line(line_number)


class RightTextPanel(BaseTextPanel):
    """Right text panel - synchronized with left panel"""
    
    def __init__(self, parent, app_controller):
        super().__init__(parent, app_controller)
        self.set_title("Right File (Synced)")

    def highlight_matches(self, line_numbers):
        """Highlight multiple lines with the multi_match tag."""
        self.text_widget.tag_remove('multi_match', '1.0', tk.END)

        for line_num in line_numbers:
            start = f"{line_num}.0"
            end = f"{line_num}.end+1c"
            try:
                self.text_widget.tag_add('multi_match', start, end)
            except tk.TclError:
                pass