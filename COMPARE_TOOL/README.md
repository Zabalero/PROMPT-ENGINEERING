# File Comparison Tool

A Python application for comparing two text files side by side with configurable similarity matching and synchronized scrolling.

## Features

- **Dual-Panel Interface**: Side-by-side text comparison with left panel as primary controller
- **Configurable Similarity Matching**: Adjustable similarity threshold (0-100%) via slider
- **Synchronized Scrolling**: Right panel automatically scrolls to match left panel navigation
- **Click-to-Navigate**: Click line numbers in left panel to jump to matching lines
- **Text Editing**: Edit content in both panels with syntax highlighting
- **File Operations**: Load, save, and save-as functionality for both panels
- **Visual Highlighting**: Color-coded lines showing match quality (exact, high, medium, low, no match)
- **Line Numbers**: Interactive line numbers for easy navigation

## Requirements

- Python 3.6 or higher
- tkinter (included with Python)
- Optional: chardet for better encoding detection

## Installation

1. Clone or download this repository
2. Install optional dependencies (recommended):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Using the Interface

1. **Load Files**:
   - Use "📂 Left File" button or File → Open Left File to load comparison source
   - Use "📂 Right File" button or File → Open Right File to load comparison target

2. **Adjust Similarity**:
   - Use the similarity slider to set matching threshold (0-100%)
   - Higher values require more exact matches
   - Lower values allow more fuzzy matching

3. **Navigate**:
   - Click line numbers in left panel to jump to matching lines in right panel
   - Use keyboard shortcuts: Ctrl+L (left file), Ctrl+R (right file), Ctrl+S (save)

4. **Edit Content**:
   - Click in either panel to edit text directly
   - Changes are highlighted and can be saved

5. **Save Files**:
   - Use 💾 Save button or File menu to save modifications
   - Files are automatically backed up before saving

## Color Coding

- **🟢 Green (Exact Match)**: Lines are identical (99%+ similarity)
- **🔵 Blue (High Similarity)**: Lines are very similar (90-99% similarity)  
- **🟡 Yellow (Medium Similarity)**: Lines are somewhat similar (70-89% similarity)
- **🔴 Red (Low Similarity)**: Lines are barely similar (threshold-69% similarity)
- **⚫ Gray (No Match)**: No matching line found

## Keyboard Shortcuts

- `Ctrl+L`: Open left file
- `Ctrl+R`: Open right file
- `Ctrl+S`: Save current file
- `Ctrl+Shift+S`: Save right file
- `Ctrl+F`: Find (not yet implemented)
- `Ctrl+G`: Go to line (not yet implemented)
- `F5`: Refresh comparison

## File Structure

```
COMPARE_TOOL/
├── main.py              # Application entry point
├── comparison_app.py    # Main application logic
├── similarity_matcher.py # Text similarity algorithms
├── text_panel.py        # Left/right panel components
├── file_manager.py      # File I/O operations
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Algorithm Details

The similarity matching uses Python's `difflib.SequenceMatcher` which implements:
- Gestalt pattern matching for robust text comparison
- Handles partial matches, word reordering, and typos
- Configurable threshold for match sensitivity
- Context-aware matching for better accuracy

## Future Enhancements

- [ ] Find and replace functionality
- [ ] Go to line dialog
- [ ] Diff export (unified/context diff formats)
- [ ] Recent files menu
- [ ] Configuration persistence
- [ ] Multiple file format support
- [ ] Plugin system for custom similarity algorithms

## License

MIT License - feel free to use and modify as needed.

## Contributing

This is a demonstration project. Contributions welcome for educational purposes.