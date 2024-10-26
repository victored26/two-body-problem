import tkinter as tk

class Dropdown(tk.Entry):
    """Represents a dropdown."""

    def __init__(self, two_body, canvas, ellipse, type:str):
        """Initializes dropdown."""
        self.settings = two_body.settings
        self.canvas = canvas
        self.ellipse = ellipse
        self.type = type

        # Retrieve dropdown options
        self.options = self.settings.dropdown_options[self.type]
        
        # Create entry variable and entry
        self.clicked = tk.StringVar()
        self.clicked.set(list(self.options)[0])
        self.dropdown = tk.OptionMenu(self.canvas, self.clicked, *self.options)
        self.dropdown.config(
            font=self.settings.label_dict['drop']['font'],
            highlightbackground=self.settings.label_dict['drop']['bg']
            )
        self.clicked.trace_add('write', self.update_ellipse)

    def update_ellipse(self, *args):
        """Updates elipsed based on dropdown choice clicked."""
        if self.type == 'desc':
            self.ellipse.description = self.clicked.get()
            self.ellipse.set_body_runs()
            new_radius = self.settings.body_dict[self.clicked.get()]['radius_mini']
            self.ellipse.reshape_ellipse(new_sma_axis=new_radius)
        elif self.type == 'ecc':
            new_ecc = float(self.clicked.get())
            self.ellipse.restart_elliptical_motion(new_ecc)
    
    def create_window(self, x:float, y:float, width:float, height:float):
        """Creates window on canvas for dropdown."""
        self.canvas.create_window(
            x, 
            y,
            window=self.dropdown, 
            width=width, 
            height=height
            )