from array import array

import pygame
from loguru import logger
from copy import copy

from pygame import Surface, image
import moderngl

import QuantumCore


class __Interface:
    def __init__(self):
        self.surface: pygame.Surface = Surface(QuantumCore.config.SCREEN_size)
        self.__ctx = copy(QuantumCore.window.context)
        
        with open(rf'{QuantumCore.config.__ENGINE_DATA__}/shaders/interface.vert') as shader_file:
            vert_shader = shader_file.read()
        with open(rf'{QuantumCore.config.__ENGINE_DATA__}/shaders/interface.frag') as shader_file:
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
    
    def nonscene_render(self):
        QuantumCore.window.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        self.__render__()
        pygame.display.flip()


class __AdvancedInterface:
    def __init__(self):
        self.surface = Surface(QuantumCore.data.config.SCREEN_size, pygame.SRCALPHA).convert_alpha()
        self.__ctx = copy(QuantumCore.window.context)
        
        with open(rf'{QuantumCore.config.__ENGINE_DATA__}/shaders/interface.vert') as shader_file:
            vert_shader = shader_file.read()
        with open(rf'{QuantumCore.config.__ENGINE_DATA__}/shaders/interface.frag') as shader_file:
            frag_shader = shader_file.read()
        self.__shaders = self.__ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)

        self.texture: moderngl.Texture = self.set_texture(self.surface, self.__ctx)
        
        self.__vbo = self.__ctx.buffer(data=array('f', [
            # position (x, y), uv cords (x, y)
            -1.0, -1.0, 0.0, 1.0,   # bottom left
            1.0,  -1.0, 1.0, 1.0,   # bottom right
            -1.0, 1.0,  0.0, 0.0,   # top left
            1.0,  1.0,  1.0, 0.0,   # top right
        ]))
        self.__vao = self.__ctx.vertex_array(self.__shaders, [(self.__vbo, '2f 2f', 'vert', 'texcoord')],
                                             skip_errors=True)
        logger.success('Interface - init\n')
    
    @staticmethod
    def set_texture(surf, ctx, *,
                    _s='RGBA', _f=(moderngl.NEAREST, moderngl.NEAREST), _a=32.0):
        tex = ctx.texture(surf.get_size(), 4)
        tex.filter, tex.swizzle = _f, _s
        tex.build_mipmaps()
        tex.anisotropy = _a
        return tex

    def set_uniform(self, u_key,  u_value: int): self.__shaders[u_key] = u_value
    
    @staticmethod
    def _surf_to_texture_(surf, tex, *, _s='RGBA') -> moderngl.Texture:
        image_data = pygame.image.tostring(surf, _s)
        tex.write(image_data)
        return tex
    
    def __render__(self):
        self._surf_to_texture_(self.surface, self.texture).use(1)
        self.__shaders['interfaceTexture'] = 1
    
        self.__vao.render(mode=moderngl.TRIANGLE_STRIP)
    
    def __destroy__(self):
        self.texture.release()
        self.__shaders.release()
        self.__vbo.release()
        self.__vao.release()
    
    def nonscene_render(self):
        QuantumCore.window.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        self.__render__()
        pygame.display.flip()
        