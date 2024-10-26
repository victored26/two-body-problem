class Settings:
    """Stores all the settings of the app."""
    
    def __init__(self):
        """Initialize the app's settings."""

        # Window Settings
        self.window_title = "Two Body Problem"
        self.window_width = 840
        self.window_height = 840
        
        # Canvas Settings
        self.canvas_width = 720
        self.canvas_height = 720
        self.canvas_bg = 'dim grey'
        self.canvas_outline_thickness = 4
        self.canvas_outline = 'dark blue'

        # Font 
        self.font = "Arial"

        # Text Label Settings
        self.label_dict = {
            'title': {
                'x': self.canvas_width*0.5,
                'y': 70,
                'bg': 'white',
                'fg': 'black',
                'text': "Two Body Problem", 
                'font': f"{self.font} 26 bold",
                'outline': 'yellow'
                },

            'n_entry': {
                'font': f"{self.font} 10 italic",
                'bg': 'light blue'
                },

            'one_name': {
                'x': self.canvas_width*0.167,
                'y': self.canvas_height*0.45,
                'bg': 'white',
                'fg': 'black',
                'text': "Body's Name", 
                'font': f"{self.font} 15 bold",
                'outline': 'yellow'
                },

            'two_name': {
                'x': self.canvas_width*(1-0.167),
                'y': self.canvas_height*0.45,
                'bg': 'white',
                'fg': 'black',
                'text': "Body's Name", 
                'font': f"{self.font} 15 bold",
                'outline': 'yellow'
                },
                
            'drop': {
                'font': "Arial 10 italic",
                'bg': 'blue'
                },

            'one_description': {
                'x': self.canvas_width*0.167,
                'y': self.canvas_height*0.65,
                'bg': 'white',
                'fg': 'black',
                'text': "Body's Description", 
                'font': f"{self.font} 15 bold",
                'outline': 'yellow'
                },

            'two_description': {
                'x': self.canvas_width*(1-0.167),
                'y': self.canvas_height*0.65,
                'bg': 'white',
                'fg': 'black',
                'text': "Body's Description", 
                'font': f"{self.font} 15 bold",
                'outline': 'yellow'
                },

            'eccentricity': {
                'x': self.canvas_width*0.5,
                'y': self.canvas_height*0.52,
                'bg': 'white',
                'fg': 'black',
                'text':"Eccentricity of Trajectory", 
                'font': f"{self.font} 15 bold",
                'outline': 'yellow'
                },

            'continue': {
                'x': self.canvas_width*0.5,
                'y': self.canvas_height*0.85,
                'bg': 'yellow',
                'act_bg': 'yellow3',
                'fg': 'blue',
                'act_fg': 'blue3',
                'text':"Continue To Simulation", 
                'font': f"{self.font} 18 bold",
                'cursor': 'hand2',
                },

            'back': {
                'x': self.canvas_width*5/6,
                'y': self.canvas_height-30,
                'bg': 'yellow',
                'act_bg': 'yellow3',
                'fg': 'blue',
                'act_fg': 'blue3',
                'text':"Return to Menu", 
                'font': f"{self.font} 12 bold",
                'cursor': 'hand2',
                },

            'exit': {
                'x': self.canvas_width*0.93,
                'y': 17,
                'bg': 'blue',
                'act_bg': 'blue3',
                'fg': 'yellow',
                'act_fg': 'yellow3',
                'text':"Exit", 
                'font': f"{self.font} 11 bold",
                'cursor': 'hand2',
                },
        }

        # Text Entry Settings
        self.entry_char_lmt = 8

        # Body Settings
        self.default_name = {'1': "One", '2': "Two"}
        self.body_dict = {
            'Light': {
                'mass': 1,
                'radius': 5,
                'radius_mini': 5,
                'color': 'yellow'
            },
            'Medium': {
                'mass': 5,
                'radius': 10,
                'radius_mini': 7,
                'color': 'cyan'
            },
            'Massive': {
                'mass': 25,
                'radius': 15,
                'radius_mini': 15,
                'color': 'lawn green'
            },
        }

        # Simulation Settings
        self.simulation_x0 = {
            '0.0': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width/6
                },
            '0.1': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.30
                },
            '0.2': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.30
                },
            '0.3': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.32
                },
            '0.4': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.33
                },
            '0.5': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.35
                },
            '0.6': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.38
                },
            '0.7': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.42
                },
            '0.8': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.45
                },
            '0.9': {
                'cm': self.canvas_width/2,
                'body': self.canvas_width*0.48
                },
        }
        # Elliptical Motion Settings
        self.orbit_anm_ms = 10
        self.orbit_runs_dict = {
            'Light': 3_000/self.orbit_anm_ms,
            'Medium': 7_000/self.orbit_anm_ms,
            'Massive': 10_000/self.orbit_anm_ms
        }

        # Eccentricity options
        self.eccentricities = [ str(x/10) for x in range(0, 10) ]
        
