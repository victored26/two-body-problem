import tkinter as tk

class NameEntry(tk.Entry):
    """Represents a name entry box (with char limit)"""

    def __init__(self, app, canvas, body, id:int):
        """Initializes name entry box."""
        self.settings = app.settings
        self.char_lmt = self.settings.entry_char_lmt
        self.canvas = canvas
        self.body = body
        self.id = id

        # Create entry variable and entry
        self.text_var = tk.StringVar()
        self.text_var.set(self.settings.default_name[id])
        self.saved_text = self.settings.default_name[id]
        self.entry = tk.Entry(
            self.canvas, 
            justify='center', 
            textvariable=self.text_var
            )
        self.entry.config(
            font=self.settings.label_dict['n_entry']['font'],
            background=self.settings.label_dict['n_entry']['bg'],
            border=4
            )
        self.text_var.trace_add('write', self.verify)

    def verify(self, *args):
        """Enforces character limit and updates body's text label."""
        if len(self.text_var.get()) <= self.char_lmt:
            self.saved_text = self.text_var.get()
            self.body.update_text_label(self.saved_text)
        else:
            self.text_var.set(self.saved_text)
    
    def create_window(self, x:float, y:float, width:float, height:float):
        """Creates window on canvas for entry."""
        self.canvas.create_window(
            x, 
            y, 
            window=self.entry, 
            width=width, 
            height=height
            )