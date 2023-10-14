"""" Main file
 """
import pygame
from threading import Thread
# app imports
from core.source import Source
from QuantumCore.err_screen.err_screen import err_screen
import QuantumCore.time
from QuantumCore.data import config


class MyApp:
    def __init__(self) -> None:
        self.__source__: Source = Source()
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while True:
            Thread(target=self.__source__.events()).run()
            Thread(target=self.__source__.update_app()).run()
            Thread(target=self.__source__.update_window()).run()
            QuantumCore.time.delta_time = self.clock.tick(config.fps)


if __name__ == '__main__':
    """ Entry point """
    running: bool = True
    while running:
        app: MyApp = None
        try:
            app = MyApp()
            app.run()
        except Exception as err:
            try:
                QuantumCore.graphic.mash.mesh.__destroy__()
                pygame.quit()
            except Exception as exc:
                print(f'\n\n{exc}\n\n')
            running = QuantumCore.err_screen.err_screen.err_screen(err)
