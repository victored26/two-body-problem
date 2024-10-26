import tkinter as tk

from body import Body
from name_entry import NameEntry
from dropdown import Dropdown

class Menu_Page:
    """Represents the menu page."""
    
    def __init__(self, app):
        """Initializes the page"""
        self.app = app
        self.root = app.root
        self.settings = app.settings
    
        self._draw_canvas()
        self._draw_title()
        self._draw_body_one_section()
        self._draw_ecc_section()
        self._draw_body_two_section()
        self._create_continue_button()
        self._create_exit_button()
        
    def load_page(self):
        """Loads the page"""
        self.canvas.pack(expand=True)

    def _hide_page(self):
        """Hides the canvas and all its widgets."""
        self.canvas.pack_forget()

    def _save_data(self):
        """Saves the data from the menu page."""
        self.app.one_name = self.one_name_entry.text_var.get()
        self.app.one_desc = self.one_desc_drop.clicked.get()
        self.app.two_name = self.two_name_entry.text_var.get()
        self.app.two_desc = self.two_desc_drop.clicked.get()
        self.app.ecc = self.ecc_drop.clicked.get()

    def _go_next_page(self):
        """Sends the user to the simulation page."""
        self._save_data()
        self._stops_animations()
        self._hide_page()
        self.app.simulation_page.load_page()

    def _stops_animations(self):
        """Stops all animations on page."""
        self.one_body.pause_elliptical_motion()
        self.ecc_body.pause_elliptical_motion()
        self.two_body.pause_elliptical_motion()
    
    def resume_animations(self):
        """Stops all animations on page."""
        self.one_body.resume_elliptical_motion()
        self.ecc_body.resume_elliptical_motion()
        self.two_body.resume_elliptical_motion()
        
    def _draw_text_label(self, label_key:str):
        """Draws a text rectangle and returns its bbox"""
        text_box = self.canvas.create_text(
            self.settings.label_dict[label_key]['x'], 
            self.settings.label_dict[label_key]['y'], 
            text=self.settings.label_dict[label_key]['text'],
            font=self.settings.label_dict[label_key]['font'],
            fill=self.settings.label_dict[label_key]['fg']
        )
        text_rectangle = self.canvas.create_rectangle(
            self._bbox_padding(text_box), 
            fill=self.settings.label_dict[label_key]['bg'],
            outline = self.settings.label_dict[label_key]['outline'],
            width=3
            )
        self.canvas.lower(text_rectangle, text_box)
        return self.canvas.bbox(text_rectangle)
    
    def _bbox_padding(self, box, padx:float=10, pady:float=10):
        """Returns a new bbox with padding."""
        bbox = self.canvas.bbox(box)
        new_bbox = (bbox[0]-padx, bbox[1]-pady, bbox[2]+padx, bbox[3]+pady)
        return new_bbox
    
    def _bbox_dims(self, bbox):
        """Returns a bbox's width and height."""
        return bbox[2]-bbox[0], bbox[3]-bbox[1]

    def _draw_canvas(self):
        """Draw the page's canvas, and displays it."""
        self.canvas = tk.Canvas(
                self.app.bg_canvas,
                bg=self.settings.canvas_bg,
                highlightthickness=self.settings.canvas_outline_thickness,
                highlightbackground=self.settings.canvas_outline,
                highlightcolor=self.settings.canvas_outline,
                width=self.settings.canvas_width,
                height=self.settings.canvas_height,
            )
        self.load_page()

    def _draw_title(self):
        """Draws the title"""
        self.title_bbox = self._draw_text_label('title')
        self.title_bbox_dims = self._bbox_dims(self.title_bbox)

    def _draw_body_one_section(self):
        """Draws the figure, labels and entries for the first body."""
        # Draw the name label
        self.one_name_bbox = self._draw_text_label('one_name')
        self.one_name_bbox_dims = self._bbox_dims(self.one_name_bbox)

        # Draw the figure
        self.canvas.create_rectangle(
            self.one_name_bbox[0],
            (self.one_name_bbox[1]-20)-3*self.one_name_bbox_dims[1],
            self.one_name_bbox[2],
            self.one_name_bbox[1]-20
        )

        self.one_body = Body(
            self.app, 
            "Light", 
            self.canvas,
            (self.one_name_bbox[0])+self.one_name_bbox_dims[0]/6,
            (self.one_name_bbox[1]-20)-3*self.one_name_bbox_dims[1]/2,
            True
        )
        self.one_body.elliptical_motion(
            (self.one_name_bbox[0])+self.one_name_bbox_dims[0]/2,
            (self.one_name_bbox[1]-20)-3*self.one_name_bbox_dims[1]/2
        )
        self.one_body.update_color('yellow')
        self.one_body.update_text_label('One')

        # Create name entry object
        self.one_name_entry = NameEntry(self.app, self.canvas, self.one_body, '1')
        self.one_name_entry.create_window(
            (self.one_name_bbox[0])+self.one_name_bbox_dims[0]/2, 
            self.one_name_bbox[3]+1.5*20, 
            self.one_name_bbox_dims[0]*0.8, 
            self.one_name_bbox_dims[1]*0.8
        )
        
        # Description Label
        self.one_desc_bbox = self._draw_text_label('one_description')

        # Description dropdown
        self.one_desc_drop = Dropdown(self.app, self.canvas, self.one_body, 'desc')
        self.one_desc_drop.create_window(
            (self.one_name_bbox[0])+self.one_name_bbox_dims[0]/2,
            self.one_desc_bbox[3] + 1.5*20,
            self.one_name_bbox_dims[0]*0.8, 
            self.one_name_bbox_dims[1]*0.8
        )

    def _draw_ecc_section(self):
        """Draws the figure, label and dropdown for eccentricity."""
        # Draw eccentricity label
        self.ecc_bbox = self._draw_text_label('eccentricity')
        self.ecc_bbox_dims = self._bbox_dims(self.ecc_bbox)

        # Draw the figure
        self.canvas.create_rectangle(
            self.ecc_bbox[0],
            (self.ecc_bbox[1]-20)-3*self.ecc_bbox_dims[1],
            self.ecc_bbox[2],
            self.ecc_bbox[1]-20
            )

        self.ecc_body = Body(
            self.app, 
            "Light", 
            self.canvas,
            (self.ecc_bbox[0])+self.ecc_bbox_dims[0]/2,
            (self.ecc_bbox[1]-20)-3*self.ecc_bbox_dims[1]*0.80,
            True 
            )
        self.ecc_body.elliptical_motion(
            (self.ecc_bbox[0])+self.ecc_bbox_dims[0]/2,
            (self.ecc_bbox[1]-20)-3*self.ecc_bbox_dims[1]/2,
            )
        self.ecc_body.update_color('red')

        # Description dropdown
        self.ecc_drop = Dropdown(self.app, self.canvas, self.ecc_body, 'ecc')
        self.ecc_drop.create_window(
            (self.ecc_bbox[0])+self.ecc_bbox_dims[0]/2,
            self.ecc_bbox[3] + 1.5*20,
            self.ecc_bbox_dims[0]*0.8, 
            self.ecc_bbox_dims[1]*0.8
            )
    
    def _draw_body_two_section(self):
        """Draws the figure, labels and entries for the second body"""
        # Draw the name label
        self.two_name_bbox = self._draw_text_label('two_name')
        self.two_name_bbox_dims = self._bbox_dims(self.two_name_bbox)

        # Draw the figure
        self.canvas.create_rectangle(
            self.two_name_bbox[0],
            (self.two_name_bbox[1]-20)-3*self.two_name_bbox_dims[1],
            self.two_name_bbox[2],
            self.two_name_bbox[1]-20
            )

        self.two_body = Body(
            self.app, 
            "Light", 
            self.canvas,
            (self.two_name_bbox[0])+self.two_name_bbox_dims[0]*5/6,
            (self.two_name_bbox[1]-20)-3*self.two_name_bbox_dims[1]/2,
            True
            )
        self.two_body.elliptical_motion(
            (self.two_name_bbox[0])+self.two_name_bbox_dims[0]/2,
            (self.two_name_bbox[1]-20)-3*self.two_name_bbox_dims[1]/2
            )
        self.two_body.update_color('blue')
        self.two_body.update_text_label('Two')

        # Create name entry object
        self.two_name_entry = NameEntry(self.app, self.canvas, self.two_body, '2')
        self.two_name_entry.create_window(
            (self.two_name_bbox[0])+self.two_name_bbox_dims[0]/2, 
            self.two_name_bbox[3]+1.5*20, 
            self.two_name_bbox_dims[0]*0.8, 
            self.two_name_bbox_dims[1]*0.8
            )

        # Description Label
        self.two_desc_bbox = self._draw_text_label('two_description')

        # Description dropdown
        self.two_desc_drop = Dropdown(self.app, self.canvas, self.two_body, 'desc')
        self.two_desc_drop.create_window(
            (self.two_name_bbox[0])+self.two_name_bbox_dims[0]/2,
            self.two_desc_bbox[3] + 1.5*20,
            self.two_name_bbox_dims[0]*0.8, 
            self.two_name_bbox_dims[1]*0.8
            )
    
    def _create_continue_button(self):
        """Creates the continue button."""
        self.continue_button = tk.Button(
            self.canvas,
            border=4,
            bg=self.settings.label_dict['continue']['bg'],
            activebackground=self.settings.label_dict['continue']['act_bg'],
            fg=self.settings.label_dict['continue']['fg'],
            activeforeground=self.settings.label_dict['continue']['act_fg'], 
            text=self.settings.label_dict['continue']['text'],
            font=self.settings.label_dict['continue']['font'],
            highlightthickness=4,
            highlightbackground='black',
            cursor=self.settings.label_dict['continue']['cursor'],
            command=self._go_next_page,
            )
        self.canvas.create_window(
            self.settings.label_dict['continue']['x'], 
            self.settings.label_dict['continue']['y'], 
            window=self.continue_button, 
            width=self.ecc_bbox_dims[0]*1.3, 
            height=self.ecc_bbox_dims[1]*1.3
            )
    
    def _create_exit_button(self):
        """Creates the exit button."""
        self.exit_button = tk.Button(
            self.canvas,
            bg=self.settings.label_dict['exit']['bg'],
            activebackground=self.settings.label_dict['exit']['act_bg'],
            fg=self.settings.label_dict['exit']['fg'], 
            activeforeground=self.settings.label_dict['exit']['act_fg'],
            text=self.settings.label_dict['exit']['text'],
            font=self.settings.label_dict['exit']['font'],
            highlightthickness=4,
            highlightbackground='black',
            cursor=self.settings.label_dict['exit']['cursor'],
            command=self.app.quit,
            )
        self.canvas.create_window(
            self.settings.label_dict['exit']['x'], 
            self.settings.label_dict['exit']['y'], 
            window=self.exit_button, 
            width=self.title_bbox_dims[0]*0.3, 
            height=self.title_bbox_dims[1]*0.3
        )
    