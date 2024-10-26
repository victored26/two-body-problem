from math import sqrt

class Ellipse:
    """Represents an ellipse."""

    def __init__(self, canvas, center_x:float, center_y:float, ecc:float, sma_axis:float):
        """Initializes the properties of the ellipse."""
        self.canvas = canvas
        self.x = center_x
        self.y = center_y
        self.birth_x = self.x
        self.birth_y = self.y
        self.ecc = ecc
        self.a = sma_axis
        self.b = self.a * sqrt(1 - self.ecc**2)
        self.boundary_coordinates()
        self.color = ''
        self.label_text = ''
    
    def boundary_coordinates(self):
        """Determines the boundary coordinates of ellipse."""
        self.x0 = (self.x - self.a)
        self.y0 = (self.y - self.b)
        self.x1 = (self.x + self.a)
        self.y1 = (self.y + self.b)

    def draw_ellipse(self, fill:str='', label_text:str=''):
        """Draws ellipse (and text label) on the canvas"""
        self.ellipse = self.canvas.create_oval(
            self.x0, self.y0, self.x1, self.y1)
        if fill:
            self.update_color(fill)
        if hasattr(self, 'color'):
            self.update_color(self.color)
        if label_text:
            self.label_text = label_text
            self.draw_text_label()

    def update_color(self, fill:str):
        """Updates the ellipse's fill color."""
        self.canvas.itemconfig(self.ellipse, fill=f"{fill}")
        self.color = fill

    def draw_text_label(self):
        """Draws ellipse's text label on the canvas"""
        self.label = self.canvas.create_text(
            self.x, 
            self.y0-15, 
            text=self.label_text
            )
        self.label_rect = self.canvas.create_rectangle(
            self._bbox_padding(self.label), 
            fill='white',
            outline='light blue',
            width=1.5
            )
        self.canvas.lower(self.label_rect, self.label)

    def _bbox_padding(self, box, padx:float=1, pady:float=0.5):
        """Returns a new bbox with padding."""
        bbox = self.canvas.bbox(box)
        new_bbox = (bbox[0]-padx, bbox[1]-pady, bbox[2]+padx, bbox[3]+pady)
        return new_bbox
    
    def update_text_label(self, new_label_text:str=''):
        """Updates the ellipse's text label on the canvas."""
        if hasattr(self, 'label'):
            self.canvas.delete(self.label)
            self.canvas.delete(self.label_rect)
        if new_label_text:
            self.label_text = new_label_text
        self.draw_text_label()

    def move_coordinates(self, xspd:float, yspd:float):
        """Moves boundary coordinates of ellipse."""
        self.x += xspd
        self.y += yspd
        self.x0 += xspd
        self.y0 += yspd
        self.x1 += xspd
        self.y1 += yspd

    def move_ellipse(self, xspd:float, yspd:float):
        """Moves the ellipse (and its text label)."""
        self.canvas.move(self.ellipse, xspd, yspd)
        self.move_coordinates(xspd, yspd)
        if hasattr(self, 'label'):
            self.canvas.move(self.label_rect, xspd, yspd)
            self.canvas.move(self.label, xspd, yspd)
    
    def reshape_ellipse(self, new_ecc:float=0, new_sma_axis:float=0):
        """Reshape and draws the ellipse (and its text label) on the canvas."""
        if new_ecc:
            self.ecc = new_ecc
        if new_sma_axis:
            self.a = new_sma_axis
        self.b = self.a * sqrt(1 - self.ecc**2)
        self.boundary_coordinates()
        self.canvas.delete(self.ellipse)
        self.draw_ellipse()
        self.update_text_label()