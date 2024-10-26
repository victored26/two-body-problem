from settings import Settings
from window import Window
from menu_page import Menu_Page
from simulation_page import Simulation_Page

class Two_Body_Problem:
    """Represents app."""

    def __init__(self):
        """Initializes the app."""
        self.settings = Settings()

        # Create app window and store app root
        self.win = Window(self)
        self.root = self.win.root
        self.bg_canvas = self.win.bg_canvas

        # Create menu page
        self.menu_page = Menu_Page(self)

        # Create simulation page
        self.simulation_page = Simulation_Page(self)

    def quit(self):
        """Closes the app."""
        self.root.destroy()

if __name__ == '__main__':
    two_body = Two_Body_Problem()
    two_body.root.mainloop()
