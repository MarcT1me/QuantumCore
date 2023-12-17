"""" This file have been CHANGE
rewrite mainloop and hem arguments
"""
# App import
from QuantumCore.messages import err_screen
import QuantumCore.graphic.mash


class App:
    running: bool = True
    
    def events(self): ...
    def update_app(self): ...
    def update_window(self): ...
    
    def run(self) -> None:
        """ Run game """
        while App.running:
            self.events()
            self.update_app()
            self.update_window()


def mainloop(QuantumGame):
    while App.running and (App.running is not None):
        try:
            QuantumGame().run()
        except Exception as err:
            App.running = err_screen.showWindow(err) if QuantumCore.config.IS_RELEASE \
                else err_screen.showTraceback(err)
        finally:
            QuantumCore.close()
