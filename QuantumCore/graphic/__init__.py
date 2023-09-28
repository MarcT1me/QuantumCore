""" Engine graphic core
 """
import moderngl
import pygame  # graphics

# other
from loguru import logger
from ctypes import c_int

# engine elements imports
import QuantumCore.graphic.camera
import QuantumCore.graphic.light
import QuantumCore.graphic.mash
import QuantumCore.graphic.texture
import QuantumCore.graphic.vbo
# engine config import
from QuantumCore.data import config
window, context = None, None  # main graphics variables

# set opengl attribute
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)


def _init_() -> None:
    """ Init engine graphics variable """
    global window, context

    """ INIT PyGamse Window """
    if config.full_screen:
        config.SCREEN_SIZE = pygame.display.get_desktop_sizes()[config.DISPLAY_num]
    window = \
        pygame.display.set_mode(
            config.SCREEN_size,
            display=config.DISPLAY_num, vsync=config.vsync,
            flags=pygame.OPENGL | pygame.DOUBLEBUF
        )
    if (config.full_screen and not pygame.display.is_fullscreen()) and config.full_screen:
        pygame.display.toggle_fullscreen()
    config.SCREEN_size = pygame.display.get_window_size()

    """ INIT GLSL context """
    context = moderngl.create_context()
    context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)
    context.viewport = (0, 0, config.SCREEN_size[0], config.SCREEN_size[1])
    if 'GLX_EXT_swap_control' in context.extensions:  # проверка поддержки VSync
        print(int(config.vsync), c_int(config.vsync))
        context.extensions.GLX_EXT_swap_control.glXSwapIntervalEXT(c_int(config.vsync))
    
    """ INIT Engine core """
    QuantumCore.graphic.camera.camera = QuantumCore.graphic.camera.Camera()
    QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh(shader_name=config.shader_name)

    logger.info(f"Engine graphic - init\n"
                f"screen: size = {config.SCREEN_size},"
                f" is full screen - {pygame.display.is_fullscreen()},"
                f" VSync - {config.vsync}\n"
                f"context: size = {context.screen.size},"
                f" GPU = {context.info['GL_RENDERER']}\n"
                f"mesh: "
                f"shaders_list = {QuantumCore.graphic.mash.mesh.vao.program.programs.keys()},\n"
                f"      VAOs_list = {QuantumCore.graphic.mash.mesh.vao.VAOs.keys()},\n"
                f"      textures_list = {QuantumCore.graphic.mash.mesh.texture.textures.keys()}\n")


def resset() -> None:
    """ Resset graphic, requires initialization of classes camera and scene """
    global window, context
    
    """ REWRITE PyGamse Window """
    if config.full_screen:
        config.SCREEN_SIZE = pygame.display.get_desktop_sizes()[config.DISPLAY_num]
    window = \
        pygame.display.set_mode(
            config.SCREEN_size,
            display=config.DISPLAY_num, vsync=config.vsync,
            flags=pygame.OPENGL | pygame.DOUBLEBUF
        )
    if (config.full_screen and not pygame.display.is_fullscreen()) and config.full_screen:
        pygame.display.toggle_fullscreen()
    config.SCREEN_size = pygame.display.get_window_size()
        
    """ REWRITE GLSL context """
    del context
    context = moderngl.create_context()
    context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)
    context.viewport = (0, 0, config.SCREEN_size[0], config.SCREEN_size[1])
    if 'GLX_EXT_swap_control' in context.extensions:  # проверка поддержки VSync
        print(int(config.vsync), c_int(config.vsync))
        context.extensions.GLX_EXT_swap_control.glXSwapIntervalEXT(c_int(config.vsync))
    
    logger.info(f'screen size = {config.SCREEN_size},  context size= {context.screen.size}')
    
    """ REWRITE Engine variables """
    QuantumCore.graphic.camera.camera.aspect_ratio = config.SCREEN_size[0] / config.SCREEN_size[1]
    QuantumCore.graphic.camera.camera.m_proj = QuantumCore.graphic.camera.camera.__get_projection_matrix__

    logger.debug(f'graphics - restart\n\n')
    