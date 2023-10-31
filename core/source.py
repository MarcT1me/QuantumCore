""" Game core
 """
import pygame  # graphics

# dependencies
import time
from loguru import logger

import QuantumCore
from GameData import settings  # there is a rewrite

# core elements
from core.elements.locations import TestScene, Location  # load game scenes
from core.skripts import Mods

# engine elements imports
import QuantumCore.time
from QuantumCore.data import config


class Source:
    def __init__(self) -> None:
        """ THE CORE OF THE GAME """
        pygame.init(), pygame.font.init(), settings.rewrite_config()  # Initializing game dependencies
        
        """ Init additional variable """
        self.time_list: dict = {
            'cube animation': 0,
            'earth animation': 0,
            'get Cam&cube pos': time.time()
        }

        self.mods = Mods().search()
        self.test_scene: Location = TestScene(self).on_init()
        self.clock = pygame.time.Clock()
        
        """ init Engine (create context, window, camera, mesh and default scene) """
        QuantumCore.init()

        """ working with pygame """
        config.APPLICATION_ICO_name = 'QuantumCore.ico'
        pygame.display.set_caption(f"{settings.APPLICATION_NAME}    v{settings.APPLICATION_VERSION}"
                                   f"      powered by {QuantumCore.name}({QuantumCore.short_name})")  # for IDE
        pygame.display.set_icon(pygame.image.load(  # for IDE
                rf'{config.__APPLICATION_FOLDER__}/{config.APPLICATION_ICO_path}/{config.APPLICATION_ICO_name}'
            )
        )
        pygame.event.set_grab(True), pygame.mouse.set_visible(False)  # mouse
        
        """ Load additional variable """
        QuantumCore.scene.scene = self.test_scene.load()
        self.mods.load()
        # QuantumCore.graphic.camera.camera.attach_object = QuantumCore.scene.scene.objects_list[
        #     QuantumCore.scene.scene.ids['котик']
        # ] # comment this out to untie the camera from the object
        
        self.spec_keys: dict = {
            'L-Ctrl': False
        }
        
        """ pygame fonts (not work/use) """
        self.application_version_font = pygame.font.SysFont('Arial', 15, bold=True).render(
            f'{settings.APPLICATION_VERSION}', False, 'cyan'
        )
        self.fps_font = pygame.font.SysFont('Arial', 15, bold=True)
        logger.debug('GAME ready\n\n')

    def events(self) -> None:
        """ Event handling """
        for event in pygame.event.get():

            """ Exit of App to button "close" """
            if event.type == pygame.QUIT:
                QuantumCore.__quit__()

            elif event.type == pygame.KEYDOWN:
                """ Detect KEY DOWN """
                if event.key == pygame.K_LCTRL:
                    self.spec_keys['L-Ctrl'] = True

                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_1:
                    QuantumCore.window.context.front_face = 'cw'
                if self.spec_keys['L-Ctrl'] and event.key == pygame.K_2:
                    QuantumCore.graphic.front_face = 'ccw'
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_g:
                    logger.debug('GAME - TEST RISE\n\n')
                    raise Exception("TEST RISE - USE 'raise - Exception' and call traceback")
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_r:
                    settings.rewrite_config()
                    QuantumCore.window.resset()
                
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_q:
                    QuantumCore.__quit__()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.spec_keys['L-Ctrl'] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                """ Detect MOUSE BUTTON DOWN """
    
    @staticmethod
    def render() -> None:
        """ render OpenGL context """
        QuantumCore.scene.scene.__render__()  # render scene
        QuantumCore.window.interface.__render__()

    def get_time(self) -> None:
        """ updating game time """
        self.time_list['cube animation'] = pygame.time.get_ticks() * 0.001
        self.time_list['earth animation'] = pygame.time.get_ticks() * 0.0001

    def update_app(self) -> None:
        """ updating the application itself (CPU) """
        self.get_time()
        
        """ main update """
        QuantumCore.scene.scene.__update__()

    def update_window(self) -> None:
        """ Rendering the application itself (GPU) """
        
        """ Interface render """
        QuantumCore.window.interface.surface.fill((0, 0, 0))
        QuantumCore.window.interface.surface.blit(self.application_version_font,
                               (0, config.SCREEN_size[1]-self.application_version_font.get_height()))
        QuantumCore.window.interface.surface.blit(self.fps_font.render(str(self.clock.get_fps()), False, 'cyan'),
                               (0, 0))

        """ Main render 3D engine - updating OpenGL context """
        self.render()
        pygame.display.flip()
        QuantumCore.window.interface.frame_tex.release()
        QuantumCore.time.delta_time = self.clock.tick(config.fps)
