from array import array
from loguru import logger
from copy import copy

from pygame import Surface, image
import moderngl

import QuantumCore.data.config
from QuantumCore.data.config import __ENGINE_DATA__


class __Interface:
    def __init__(self):
        self.surface = Surface(QuantumCore.data.config.SCREEN_size)
        self.__ctx = copy(QuantumCore.window.context)
        
        with open(rf'{__ENGINE_DATA__}/shaders/interface.vert') as shader_file:
            vert_shader = shader_file.read()
        with open(rf'{__ENGINE_DATA__}/shaders/interface.frag') as shader_file:
            frag_shader = shader_file.read()
        self.__shaders = self.__ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        
        self.surface.fill((0, 0, 0))
        self.set_color_key((0, 0, 0))
        self.frame_tex = self._surf_to_texture_()
        
        self.__vbo = self.__ctx.buffer(data=array('f', [
            # position (x, y), uv cords (x, y)
            -1.0, 1.0,  0.0, 0.0,   # top left
            1.0,  1.0,  1.0, 0.0,   # top right
            -1.0, -1.0, 0.0, 1.0,   # bottom left
            1.0,  -1.0, 1.0, 1.0,   # bottom right
        ]))
        self.__vao = self.__ctx.vertex_array(self.__shaders, [(self.__vbo, '2f 2f', 'vert', 'texcoord')],
                                             skip_errors=True)
        logger.success('Interface - init\n')

    def set_color_key(self, key: tuple[float, float, float]) -> None:
        self.__shaders['colorkey'] = key

    def _surf_to_texture_(self, *, _s='BGRA', _f=(moderngl.NEAREST, moderngl.NEAREST)):
        tex = self.__ctx.texture(self.surface.get_size(), 4, image.tostring(self.surface, _s))
        tex.filter, tex.swizzle = _f, _s
        return tex
    
    def __render__(self):
        self.frame_tex = self._surf_to_texture_()
        self.frame_tex.use(1)
        self.__shaders['interface_texture'] = 1
        self.__vao.render(mode=moderngl.TRIANGLE_STRIP)
        self.frame_tex.release()
    
    def __destroy__(self):
        self.__shaders.release()
        self.frame_tex.release()
        self.__vbo.release()
        self.__vao.release()


from QuantumCore.model import BaseModel


class __AdvancedInterface(BaseModel):
    def __init__(self):
        super().__init__(None, 'interface', None, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        self.surface = Surface(QuantumCore.data.config.SCREEN_size)
        self.__ctx = copy(QuantumCore.window.context)
        self.frame_tex = None
        self.set_color_key((0, 0, 0))
        logger.success('Interface - init\n')
    
    def set_color_key(self, key: tuple[float, float, float]) -> None:
        self.shader_program['colorkey'] = key
    
    def _surf_to_texture_(self, *, _s='BGRA', _f=(moderngl.NEAREST, moderngl.NEAREST)):
        tex = self.__ctx.texture(self.surface.get_size(), 4, image.tostring(self.surface, _s))
        tex.filter, tex.swizzle = _f, _s
        return tex
    
    def __render__(self):
        self.frame_tex = self._surf_to_texture_()
        self.frame_tex.use(1)
        self.shader_program['interface_texture'] = 1
        self.vao.render()
        self.frame_tex.release()