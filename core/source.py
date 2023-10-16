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
from QuantumCore.graphic.texture import CustomTexture_name
from QuantumCore.graphic.vbo import CustomVBO_name
from QuantumCore.data import config
from GameData.settings import MODEL_path


class Source:
    def __init__(self) -> None:
        """ THE CORE OF THE GAME """
        pygame.init(), pygame.font.init(), settings.rewrite_config()  # Initializing game dependencies

        CustomVBO_name['WoodenWatchTower'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            f'{config.__APPLICATION_FOLDER__}/{MODEL_path}/WoodenWatchTower', 'obj', 'jpg')
        CustomVBO_name['Cat'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{config.__APPLICATION_FOLDER__}/{MODEL_path}/cat', 'obj', 'jpg')
        CustomVBO_name['Earth'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{config.__APPLICATION_FOLDER__}/{MODEL_path}/earth', 'obj', 'png')

        CustomTexture_name['box1'] = rf'{config.__APPLICATION_FOLDER__}/QuantumCore/data/textures/box1.jpg'
        CustomTexture_name['wall1'] = rf'{config.__APPLICATION_FOLDER__}/QuantumCore/data/textures/wall1.jpg'
        
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
        
        # time variables
        self.time_list: dict = {
            'cube animation': 0,
            'earth animation': 0,
            'get Cam&cube pos': time.time()
        }
        
        """ set locations, and main render scene """
        self.test_scene: Location = TestScene(self)
        QuantumCore.scene.scene = self.test_scene
        QuantumCore.scene.scene.load()

        """ Additional variable """
        self.mods = Mods()
        self.mods.search(), self.mods.load()
        
        self.spec_keys: dict = {
            'L-Ctrl': False
        }
        
        # pygame fonts (not work/use)
        """
        self.some_font = pygame.font.SysFont('Arial', 125, bold=True).render(f'Hello World!', True, (200, 250, 0))
        self.application_version_font = pygame.font.SysFont('Arial', 15).render(
            f'{settings.APPLICATION_VERSION}', True, 'white'
        )"""
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
                    QuantumCore.graphic.context.front_face = 'cw'
                if self.spec_keys['L-Ctrl'] and event.key == pygame.K_2:
                    QuantumCore.graphic.front_face = 'ccw'
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_g:
                    logger.debug('GAME - TEST RISE\n\n')
                    raise Exception("TEST RISE - USE 'raise - Exception' and call traceback")
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_r:
                    settings.rewrite_config()
                    QuantumCore.graphic.resset()
                
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

    def get_time(self) -> None:
        """ updating game time """
        self.time_list['cube animation'] = pygame.time.get_ticks() * 0.001
        self.time_list['earth animation'] = pygame.time.get_ticks() * 0.0001

    def update_app(self) -> None:
        """ updating the application itself (CPU) """
        
        # update animation time
        self.get_time()
        
        """ main update """
        QuantumCore.scene.scene.__update__()

    def update_window(self) -> None:
        """ Rendering the application itself (GPU) """

        """ Main render 3D engine - updating OpenGL context """
        self.render()

        pygame.display.flip()
