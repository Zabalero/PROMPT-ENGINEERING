import tkinter as tk

class TextEditorWithLineNumbers(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.scroll_callback = kwargs.pop("scroll_callback", None)
        super().__init__(parent)
        self.text_font = kwargs.get("font", ("Courier New", 10))

        self.text = tk.Text(self, *args, **kwargs)
        self.linenumbers = tk.Canvas(self, width=40, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        
        self.text.configure(yscrollcommand=self.on_scroll)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.text.bind("<<Modified>>", self.on_modified)
        self.text.bind("<Configure>", self.on_modified)
        self.text.bind("<MouseWheel>", self.on_modified)

    def on_scroll(self, *args):
        self.scrollbar.set(*args)
        self.redraw_line_numbers()
        if self.scroll_callback:
            self.scroll_callback(self.text.yview())

    def on_modified(self, event=None):
        self.text.edit_modified(False)
        self.redraw_line_numbers()

    def redraw_line_numbers(self):
        self.linenumbers.delete("all")
        
        first_line = int(self.text.index("@0,0").split('.')[0])
        last_line = int(self.text.index(f"@0,{self.text.winfo_height()}").split('.')[0])
        
        for i in range(first_line, last_line + 1):
            dlineinfo = self.text.dlineinfo(f"{i}.0")
            if dlineinfo:
                x, y, width, height, baseline = dlineinfo
                self.linenumbers.create_text(38, y, anchor="ne", text=str(i), font=self.text_font, fill="#666666")

    def __getattr__(self, name):
        return getattr(self.text, name)
