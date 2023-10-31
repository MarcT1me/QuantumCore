
# engine elements
from QuantumCore.graphic.vao import VAO
from QuantumCore.graphic.texture import Texture
from QuantumCore.data.config import shader_name
import QuantumCore.graphic


class Mesh:
    def __init__(self, *, shader_name=shader_name) -> None:
        """ Engine graphics heart """
        self.vao = VAO(shader_name)
        self.texture = Texture()

    def __destroy__(self) -> None:
        """ delete data from GRAM """
        self.vao.__destroy__()
        self.texture.__destroy__()
        QuantumCore.window.interface.frame_tex.release()


mesh: Mesh = None
