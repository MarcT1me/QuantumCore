
# engine elements
from QuantumCore.graphic.vao import VAO
from QuantumCore.graphic.texture import Texture


class Mesh:
    def __init__(self, shader_name) -> None:
        """ Engine graphics heart """

        # dependencies
        self.vao = VAO(shader_name)
        self.texture = Texture()

    def __destroy__(self) -> None:
        """ stop rendering """
        self.vao.__destroy__()
        self.texture.__destroy__()


mesh: Mesh = None
