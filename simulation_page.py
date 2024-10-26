import tkinter as tk
from math import sqrt

from ellipse import Ellipse
from body import Body

class Simulation_Page:
    """Represents the simulation page."""
    
    def __init__(self, app):
        """Initializes the page"""
        self.app = app
        self.root = self.app.win.root
        self.settings = self.app.settings
    
        self._draw_canvas()
        self._draw_title()
        self._create_go_back_button()
        self._create_exit_button()
        
    def load_page(self):
        """Loads the page"""
        self.canvas.pack(expand=True)
        self.begin_simulation()

    def _hide_page(self):
        """Hides the canvas and all its widgets."""
        self.canvas.pack_forget()

    def _go_back_page(self):
        """Sends the user to the menu page."""
        self._stop_simulation()
        self._hide_page()  
        self.app.menu_page.load_page()
        self.app.menu_page.resume_animations()

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
            outline=self.settings.label_dict[label_key]['outline'],
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
        """Draws the page's canvas"""
        self.canvas = tk.Canvas(
            self.app.bg_canvas, 
            bg=self.settings.canvas_bg,
            highlightthickness=self.settings.canvas_outline_thickness,
            highlightbackground=self.settings.canvas_outline,
            highlightcolor=self.settings.canvas_outline,
            width=self.settings.canvas_width,
            height=self.settings.canvas_height
            )
    
    def _draw_title(self):
        """Draws the title"""
        self.title_bbox = self._draw_text_label('title')
        self.title_bbox_dims = self._bbox_dims(self.title_bbox)

    def _create_go_back_button(self):
        """Creates the go back button"""
        self.back_button = tk.Button(
            self.canvas,
            bg=self.settings.label_dict['back']['bg'],
            activebackground=self.settings.label_dict['back']['act_bg'],
            fg=self.settings.label_dict['back']['fg'], 
            activeforeground=self.settings.label_dict['back']['act_fg'],
            text=self.settings.label_dict['back']['text'],
            font=self.settings.label_dict['back']['font'],
            highlightthickness=4,
            highlightbackground='black',
            cursor=self.settings.label_dict['back']['cursor'],
            command=self._go_back_page,
            )
        self.canvas.create_window(
            self.settings.label_dict['back']['x'], 
            self.settings.label_dict['back']['y'], 
            window=self.back_button, 
            width=self.title_bbox_dims[0]*0.5, 
            height=self.title_bbox_dims[1]*0.5)
    
    def _create_exit_button(self):
        """Creates the exit button"""
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

    def begin_simulation(self):
        """Sets up simulation."""
        # Determine center of mass coordinates
        self.x0 = self.settings.simulation_x0[self.app.ecc]['cm']
        self.y0 = (self.settings.canvas_height + self.title_bbox[3])/2

        # Determine the initial coordinates for first body
        self.one_x = self.settings.simulation_x0[self.app.ecc]['body']
        self.one_y = self.y0

        # Fix eccentricity of trajectories
        self.ecc = float(self.app.ecc)

        # Determine the semi-major axis for the first trajectory
        self.one_dist_center = sqrt((self.one_x-self.x0)**2+(self.one_y-self.y0)**2)
        self.one_sma_axis = self.one_dist_center/(1-self.ecc)

        # Draw the center of mass
        self.center_mass = Ellipse(self.canvas, self.x0, self.y0, 0, 2)
        self.center_mass.draw_ellipse(
            fill='black', 
            label_text='Center of Mass'
            )

        # Assign first body and second body labels based on mass
        self._body_coordinates()
        
        # Create the bodies and start animating
        self.create_bodies()

    def create_bodies(self):
        """Creates the bodies for the simulations."""
        self.one_body = Body(
            self.app, 
            self.app.one_desc, 
            self.canvas, 
            self.one_x, 
            self.one_y)
        self.one_body.elliptical_motion(
            self.x0+self.one_sma_axis*self.ecc, 
            self.one_y, 
            ecc=self.ecc)
        self.canvas.itemconfig(
            self.one_body.traj_orbit.ellipse, 
            outline=self.settings.body_dict[self.one_body.description]['color']
            )
        self.one_body.update_color(
            self.settings.body_dict[self.one_body.description]['color']
            )
        self.one_body.update_text_label(self.app.one_name)
        self.canvas.delete(self.one_body.pt_orbit.ellipse)

        # Determine mass ratio.
        self.mass_ratio_12 = self.one_body.mass
        self.mass_ratio_12 /= self.settings.body_dict[self.app.two_desc]['mass'] 

        # Determine the initial coordinates for the second body
        self.two_x = self.x0 + self.mass_ratio_12*self.one_sma_axis*(1-self.ecc)
        self.two_y = self.one_y

        self.two_body = Body(
            self.app, 
            self.app.two_desc, 
            self.canvas, 
            self.two_x, 
            self.two_y
            )

        # Determine the semi-major axis for the second trajectory
        self.two_dist_center = sqrt((self.two_x-self.x0)**2+(self.two_y-self.y0)**2)
        self.two_sma_axis = self.two_dist_center/(1-self.ecc)

        # Animate the trajectory
        self.two_body.elliptical_motion(
            self.x0-self.two_sma_axis*self.ecc, 
            self.two_y, 
            ecc=self.ecc
            )
        self.canvas.itemconfig(
            self.two_body.traj_orbit.ellipse, 
            outline=self.settings.body_dict[self.two_body.description]['color']
            )
        self.canvas.delete(self.two_body.pt_orbit.ellipse)
        self._animate_second_body()
        self.two_body.update_color(
            self.settings.body_dict[self.two_body.description]['color']
            )
        self.two_body.update_text_label(self.app.two_name)

    def _body_coordinates(self):
        """Determines the coordinates of the bodies based on their mass."""
        descr_one = self.app.one_desc
        name_one = self.app.one_name
        descr_two = self.app.two_desc
        name_two = self.app.two_name
        mass_one = self.settings.body_dict[descr_one]['mass']
        mass_two = self.settings.body_dict[descr_two]['mass']

        if mass_one > mass_two:
            self.app.one_desc = descr_two
            self.app.one_name = name_two
            self.app.two_desc = descr_one
            self.app.two_name = name_one

    def _animate_second_body(self):
        """Animate second body with respect to the first."""
        self.two_body.pause_elliptical_motion()
        disp_x = self.one_body.disp_x
        disp_y = self.one_body.disp_y

        # Move the body and its text label
        self.two_body.move_ellipse(
            -self.mass_ratio_12*disp_x, 
            -self.mass_ratio_12*disp_y
            )

        # Start animating
        self.two_body.animation = self.root.after(
            self.settings.orbit_anm_ms, 
            self._animate_second_body
            )

    def _stop_simulation(self):
        """Stops all animations on menu_page."""
        # Stop the animations
        self.one_body.pause_elliptical_motion()
        self.two_body.pause_elliptical_motion()

        # Delete canvas items
        self.one_body.delete_elliptical_motion()
        self.two_body.delete_elliptical_motion()