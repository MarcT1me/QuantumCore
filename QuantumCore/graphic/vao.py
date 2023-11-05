# other
from loguru import logger
from copy import copy

# engine elements imports
import QuantumCore.graphic
from QuantumCore.graphic.vbo import VBO
from QuantumCore.graphic.shader_program import ShaderProgram
from QuantumCore.data import config


class VAO:
    def __init__(self, *, shader_name: tuple[str, str] = config.SHADER_NAME) -> None:
        self.ctx = copy(QuantumCore.window.context)

        # VAO dependencies
        self.vbo = VBO()
        self.program = ShaderProgram()

        # VAO array
        self.VAOs = dict()
        self._load_vaos(shader_name)
    
    def _load_vaos(self, shader_name) -> None:
        # load custom VAO`s
        for name in self.vbo.VBOs.keys():
            self.VAOs[name] = self.__get_vao(
                program=self.program.programs[shader_name[1]],
                vbo=self.vbo.VBOs[name]
            )  # initialize VAO models
            
            # in development
            """
            self.VAOs[f'shadow_{name}'] = self.get_vao(
                program=self.program.programs['shadow_map'],
                vbo=self.vbo.VBOs[name]
                )  # initialize the shadow of the VAO model
            """
        
        for name in self.vbo.service_VBOs.keys():
            self.VAOs[name] = self.__get_vao(
                program=self.program.programs[name],
                vbo=self.vbo.service_VBOs[name]
            )
        logger.debug('VAO - init\n\n')

    def __get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.formats, *vbo.attributes)], skip_errors=True)
        return vao

    def __destroy__(self) -> None:
        self.vbo.__destroy__()
        self.program.__destroy__()
