""" Engine graphic core
 """
import moderngl
import pygame  # graphics

# other
from loguru import logger

# engine elements imports
import QuantumCore.graphic.camera
import QuantumCore.graphic.light
import QuantumCore.graphic.mash
import QuantumCore.graphic.texture
import QuantumCore.graphic.vbo
# engine config import
from QuantumCore.data import config


class __GRAPHIC:
    # set opengl attribute
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    
    interface = None  # type: QuantumCore.__AdvancedInterface
    context = None  # type: moderngl.Context
    
    def __init__(self, flags):
        """ Init engine graphic
         """
        self.flags = flags
        
        """ INIT PyGamse Window """
        if config.full_screen:
            config.SCREEN_SIZE = pygame.display.get_desktop_sizes()[config.DISPLAY_num]
        self.screen = \
            pygame.display.set_mode(
                config.SCREEN_size,
                display=config.DISPLAY_num, vsync=config.VSYNC,
                flags=self.flags['pygame']
            )  # flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE
        if (config.full_screen and not pygame.display.is_fullscreen()) and config.full_screen:
            pygame.display.toggle_fullscreen()
        pygame.display.flip()
        
        w_size = pygame.display.get_window_size()
        config.SCREEN_size[0] = w_size[0]
        config.SCREEN_size[1] = w_size[1]
        # rend surf
        config.RENDER_size[0] = w_size[0]*config.RESOLUTION_SCALING
        config.RENDER_size[1] = w_size[1]*config.RESOLUTION_SCALING
        
        """ INIT GLSL context """
        self.context = moderngl.create_context()
        self.context.enable(flags=self.flags['glsl'])  # flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND
        self.context.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.context.viewport = (0, 0, *config.SCREEN_size)
        
        """ init render surface """
        # Создание текстуры для рендера
        # render_texture = self.context.texture(config.RENDER_size, 4)
        # render_texture.build_mipmaps()
        
        # Создание фреймбуфера
        # self._render_fbo = self.context.framebuffer(color_attachments=[render_texture])
    
    def set_mesh(self):
        """ INIT Engine core """
        QuantumCore.graphic.camera.camera = QuantumCore.graphic.camera.Camera()
        QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh()
        
        logger.info(
            f"Engine graphic - init\n"
            f"screen: size = {config.SCREEN_size},"
            f" is full screen - {pygame.display.is_fullscreen()},"
            f" VSync - {config.VSYNC}\n"
            f"context: size = {self.context.screen.size},"
            f" GPU = {self.context.info['GL_RENDERER']}\n"
            f"mesh: "
            f"shaders_list = {QuantumCore.graphic.mash.mesh.vao.program.programs.keys()},\n"
            f"      VAOs_list = {QuantumCore.graphic.mash.mesh.vao.VAOs.keys()},\n"
            f"      textures_list = {QuantumCore.graphic.mash.mesh.texture.textures.keys()}\n"
        )
    
    def resset(self) -> None:
        """ Resset graphic, requires initialization of classes camera and scene """
        self.__init__(self.flags)
        logger.info(f'screen size = {config.SCREEN_size},  context size= {self.context.screen.size}')
        
        """ REWRITE Engine variables """
        if QuantumCore.graphic.camera.camera is not None:
            QuantumCore.graphic.camera.camera._aspect_ratio = config.SCREEN_size[0]/config.SCREEN_size[1]
            QuantumCore.graphic.camera.camera.m_proj = QuantumCore.graphic.camera.camera._get_projection_matrix_
        
        logger.debug(f'graphics - restart\n\n')
    
    def close(self):
        self.context.release()
        self.interface.__destroy__()
