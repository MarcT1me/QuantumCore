
# other
from loguru import logger

import QuantumCore.graphic
# engine config imports
from QuantumCore.data.config import __APPLICATION_FOLDER__
from QuantumCore.data.config import SHADER_path


class ShaderProgram:
    def __init__(self) -> None:
        self.ctx = QuantumCore.graphic.context

        # program array
        self.programs = {
            'default': self.__get_shader_program__(shader_name='default', shader_path_name='default'),
            # 'skybox': self.get_shader_program('skybox'),
            # 'advanced_skybox': self.get_shader_program('advanced_skybox'),
            # 'shadow_map': self.get_shader_program('shadow_map')
        }

        logger.debug('Default shaders init/load - finished')

    def add(self, path_name, name, *, path=SHADER_path) -> None:
        """ Add shaders in list """
        self.programs[name] = self.__get_shader_program__(shader_name=name,
                                                          shader_path_name=path_name, shader_path=path)
        logger.debug(f'third-party shader load - finished\n')

    def __get_shader_program__(self, *, shader_name, shader_path_name, shader_path=SHADER_path):
        """ set shader program (use GLSL files) """
        with open(rf'{__APPLICATION_FOLDER__}/{shader_path}/{shader_path_name}/{shader_name}.vert') as shader_file:
            vertex_shader = shader_file.read()

        with open(rf'{__APPLICATION_FOLDER__}/{shader_path}/{shader_path_name}/{shader_name}.frag') as shader_file:
            fragment_shader = shader_file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        logger.info(f'shader with name: {shader_name} - load')
        return program

    def __destroy__(self) -> None: [program.release() for program in self.programs.values()]
