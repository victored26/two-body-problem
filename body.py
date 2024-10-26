from math import sqrt, pi, cos, sin, acos

from ellipse import Ellipse

class Body(Ellipse):
    """Represents a body which experiences gravity."""

    def __init__(self, app, desc:str, canvas, center_x:float, center_y:float, mini:bool=False):
        """Initializes the body as a circle"""
        self.root = app.win.root
        self.settings = app.settings
        self.description = desc
        self.mini = mini
        self.mass = self.settings.body_dict[self.description]['mass']
        if mini:
            self.radius = self.settings.body_dict[self.description]['radius_mini']
        else:
            self.radius = self.settings.body_dict[self.description]['radius']
        super().__init__(canvas, center_x, center_y, 0, self.radius)

    def elliptical_motion(self, pt_x:float, pt_y:float, ecc:float=0):
        """Sets up an animation of eliptical orbit."""
        self.set_body_runs()
        self.pt_x = pt_x
        self.pt_y = pt_y
        self.dist_pt = sqrt((self.x-pt_x)**2 + (self.y-pt_y)**2)
        theta = acos((self.x-pt_x)/self.dist_pt)
        if self.y > pt_y:
            theta = 2*pi - theta
        self.theta = theta
        self.birth_theta = self.theta

        # Draw the point of orbit
        self.pt_orbit = Ellipse(self.canvas, pt_x, pt_y, 0, 1)
        self.pt_orbit.draw_ellipse(fill='black')

        # Determine the semi-major and semi-minor axis
        if self.x-pt_x != 0:
            self.motion_a = (self.x-pt_x)/cos(self.theta)
            self.motion_b = self.motion_a*sqrt(1-ecc**2)
        else:
            self.motion_b = -(self.y-pt_y)/sin(self.theta)
            self.motion_a = self.motion_b/sqrt(1-ecc**2)

        # Draw the trajectory of orbit
        self.traj_orbit = Ellipse(self.canvas, pt_x, pt_y, ecc, self.motion_a)
        self.traj_orbit.draw_ellipse()
        self.canvas.itemconfig(self.traj_orbit.ellipse, dash=True)

        # Draw the body at its initial position
        self.draw_ellipse()

        # Start animation
        self.animate_ellip_motion()
    
    def animate_ellip_motion(self):
        """Animates the elliptical motion."""
        if self.theta >= 2*pi:
            self.theta %= 2*pi 
        theta = self.theta
        self.theta += 2*pi/self.orbit_runs

        # Calculate the movement displacement
        self.disp_x = (cos(self.theta)-cos(theta))*self.motion_a
        self.disp_y = -(sin(self.theta)-sin(theta))*self.motion_b

        # Move the body and its text label
        self.move_ellipse(self.disp_x, self.disp_y)

        # Start animating
        self.animation = self.root.after(
            self.settings.orbit_anm_ms, self.animate_ellip_motion)
    
    def restart_elliptical_motion(self, ecc:float=0):
        """Restarts the animation for elliptical motion with a diff ecc."""
        # Stop animation
        self.pause_elliptical_motion()

        # Delete previous canvas assets
        self.canvas.delete(self.pt_orbit.ellipse)
        self.canvas.delete(self.traj_orbit.ellipse)
        self.canvas.delete(self.ellipse)

        # Restore original coordinates
        self.x = self.birth_x
        self.y = self.birth_y
        self.theta = self.birth_theta
        self.boundary_coordinates()

        # Restart the animation from scratch
        self.elliptical_motion(self.pt_x, self.pt_y, ecc)
    
    def pause_elliptical_motion(self):
        """Pauses the animation for elliptical motion."""
        self.root.after_cancel(self.animation)
    
    def resume_elliptical_motion(self):
        """Resumes the animation for elliptical motion."""
        self.animate_ellip_motion()
    
    def delete_elliptical_motion(self):
        """Deletes all elliptical motion canvas assets."""
        self.canvas.delete(self.ellipse)
        if hasattr(self, 'label'):
            self.canvas.delete(self.label)
            self.canvas.delete(self.label_rect)
        if hasattr(self, 'pt_orbit') and hasattr(self.pt_orbit, 'ellipse'):
            self.canvas.delete(self.pt_orbit.ellipse)
        if hasattr(self, 'traj_orbit') and hasattr(self.traj_orbit, 'ellipse'):
            self.canvas.delete(self.traj_orbit.ellipse)
    
    def set_body_runs(self):
        """Fixes speed of orbit based on description."""
        self.orbit_runs = self.settings.orbit_runs_dict[self.description]