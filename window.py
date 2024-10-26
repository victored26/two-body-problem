from tkinter import Tk, PhotoImage, Canvas

class Window:
    """Represents the app window."""
    
    def __init__(self, two_body):
        """Initializes Window."""
        self.settings = two_body.settings
        self.title = self.settings.window_title
        self.width = self.settings.window_width
        self.height = self.settings.window_height

        # Create app root
        self.root = Tk()
        self.root.title(self.title)
        
        # Specify dimensions and center the window
        self._width_offset()
        self._height_offset()
        self._fix_geometry()

        # Open the image
        self.bg = PhotoImage(file = "space.png") 
  
        # Create Canvas 
        self.bg_canvas = Canvas(
            self.root, 
            width = self.width, 
            height = self.height
            ) 
          
        self.bg_canvas.pack(fill = "both", expand = True) 
        
        # Display image 
        self.bg_canvas.create_image( 
            0, 
            0, 
            image = self.bg,  
            anchor = "center"
            ) 


    def _width_offset(self):
        """Calculates the horizontal midpoint of screen."""
        screen_width = self.root.winfo_screenwidth()
        self.width_offset = (screen_width - self.width) // 2
    
    def _height_offset(self):
        """Calculates the vertical midpoint of screen."""
        screen_height = self.root.winfo_screenheight()
        self.height_offset = (screen_height - self.height) // 2

    def _fix_geometry(self):
        """Centers the window and fixes its dimensions."""
        dimensions = f"{self.width}x{self.height}"
        dimensions += f"+{self.width_offset}+{self.height_offset}"
        self.root.geometry(dimensions)