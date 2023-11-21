"""" Main file
 """
import QuantumCore
from core.source import Source
from QuantumCore.app import App, mainloop


class QuantumGame(App):
    def __init__(self) -> None: self.__source__: Source = Source()
    def events(self): self.__source__.events()
    def update_app(self): self.__source__.update_app()
    def update_window(self): self.__source__.update_window()


if __name__ == '__main__':
    """ Entry point """
    mainloop(QuantumGame)
    