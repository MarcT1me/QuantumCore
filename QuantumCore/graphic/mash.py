
# engine elements
import QuantumCore.graphic
from QuantumCore.graphic.vao import VAO
from QuantumCore.graphic.texture import Texture


class Mesh:
    def __init__(self) -> None:
        """ Engine graphics heart """
        self.vao = VAO()
        self.texture = Texture()

    def __destroy__(self) -> None:
        """ delete data from GRAM """
        self.vao.__destroy__()
        self.texture.__destroy__()
        QuantumCore.window.interface.frame_tex.release()


mesh: Mesh = None
