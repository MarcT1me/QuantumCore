"""" This file have been CHANGE
rewrite mainloop and hem arguments
"""

import concurrent.futures
# import multiprocessing
from QuantumCore.messages import err_screen
# app imports
import QuantumCore.graphic.mash


class App:
    def events(self): ...
    def update_app(self): ...
    def update_window(self): ...
    
    def run(self) -> None:
        while True:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.events())
                executor.submit(self.update_app())
                executor.submit(self.update_window())


def mainloop(QuantumGame):
    running: bool = True
    while running and (running is not None):
        try:
            QuantumGame().run()
        except Exception as err:
            try: QuantumCore.graphic.mash.mesh.__destroy__()
            except Exception as exc: print(f'\n\n{exc}\n\n')
            running = err_screen.showWindow(err) if QuantumCore.config.IS_RELEASE \
                else err_screen.showTraceback(err)
