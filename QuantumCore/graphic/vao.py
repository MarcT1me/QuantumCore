# other
from loguru import logger

# engine elements imports
import QuantumCore.graphic
from QuantumCore.graphic.vbo import VBO
from QuantumCore.graphic.shaders.shader_program import ShaderProgram


class VAO:
    def __init__(self, shader_name: tuple[str, str]) -> None:
        self.ctx = QuantumCore.graphic.context

        # VAO dependencies
        self.vbo = VBO()
        self.program = ShaderProgram()
        self.program.add(shader_name[0], shader_name[1])

        # VAO array
        self.VAOs: dict[str, QuantumCore.graphic.context.vertex_array] = {
            'cube': self.__get_vao(
                program=self.program.programs[shader_name[1]],
                vbo=self.vbo.VBOs['cube']
            )
            # 'skybox': self.get_vao(
            #     program=self.program.programs['skybox'],
            #     vbo=self.vbo.VBOs['skybox']),
            # 'advanced_skybox': self.get_vao(
            #     program=self.program.programs['advanced_skybox'],
            #     vbo=self.vbo.VBOs['advanced_skybox'])
        }
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
        
        logger.debug('VAO - init\n\n')

    def __get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.formats, *vbo.attributes)], skip_errors=True)
        return vao

    def __destroy__(self) -> None:
        self.vbo.__destroy__()
        self.program.__destroy__()
