"""" Main file
 """

import concurrent.futures
# import multiprocessing
from QuantumCore.messages import err_screen
# app imports
from core.source import Source
import QuantumCore.graphic.mash


class QuantumGame:
    def __init__(self) -> None:
        self.__source__: Source = Source()

    def run(self) -> None:
        while True:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.__source__.events())
                executor.submit(self.__source__.update_app())
                executor.submit(self.__source__.update_window())


if __name__ == '__main__':
    """ Entry point """
    # multiprocessing.freeze_support()
    running: bool = True
    while running:
        try:
            QuantumGame().run()
        except Exception as err:
            try: QuantumCore.graphic.mash.mesh.__destroy__()
            except Exception as exc: print(f'\n\n{exc}\n\n')
            running = err_screen.showWindow(err)
