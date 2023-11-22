""" Game core
 """
import pygame  # graphics

# dependencies
from loguru import logger

import QuantumCore
from QuantumCore.app import App, mainloop
from GameData import settings  # there is a rewrite

# core elements
from core.elements.locations import TestScene, Location  # load game scenes

# engine elements imports
import QuantumCore.time
from QuantumCore import config


class TestGame(App):
    fps_fonts_colors = ('red', 'orange', 'yellow', 'green', 'cyan')
    
    def __init__(self) -> None:
        """ THE CORE OF THE GAME """
        pygame.init(), pygame.font.init(), settings.rewrite_config()  # Initializing game dependencies
        
        """ init Engine (create context, window, camera, mesh and default scene) """
        QuantumCore.init()
        
        self.loading = QuantumCore.UI.InterfaceUI(['core', 'UI'], 'loading')
        self.ingame_interface = QuantumCore.UI.InterfaceUI(['core', 'UI'], 'ingame_interface')
        
        self.loading.itrf.step(8, 'Init Engine', 'Game Window')

        """ working with pygame """
        config.APPLICATION_ICO_name = 'QuantumCore.png'
        pygame.display.set_caption(f"{settings.APPLICATION_NAME}    v{settings.APPLICATION_VERSION}"
                                   f"      powered by {QuantumCore.name}({QuantumCore.short_name})")  # for IDE
        pygame.display.set_icon(pygame.image.load(  # for IDE
                rf'{config.__ENGINE_DATA__}/{config.APPLICATION_ICO_path}/{config.APPLICATION_ICO_name}'
            )
        )
        pygame.event.set_grab(True), pygame.mouse.set_visible(False)  # mouse
        
        """ Init additional variable """
        self.clock = pygame.time.Clock()
        self.test_scene: Location = TestScene(self).on_init()
        
        """ Load additional variable """
        QuantumCore.scene.scene = self.test_scene.load()
        # QuantumCore.graphic.camera.camera.attach_object = QuantumCore.scene.scene.objects_list[
        #     QuantumCore.scene.scene.ids['котик']
        # ] # comment this out to untie the camera from the object

        self.loading.itrf.step(98, stage='Init Game', status='additional variables and game font')
        self.spec_keys: dict = {
            'L-Ctrl': False
        }
        logger.debug('GAME ready\n\n')

    def events(self) -> None:
        """ Event handling """
        for event in pygame.event.get():

            """ Exit of App to button "close" """
            if event.type == pygame.QUIT:
                QuantumCore.close()
                exit()

            elif event.type == pygame.KEYDOWN:
                """ Detect KEY DOWN """
                if event.key == pygame.K_LCTRL:
                    self.spec_keys['L-Ctrl'] = True

                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_1:
                    QuantumCore.window.context.front_face = 'cw'
                if self.spec_keys['L-Ctrl'] and event.key == pygame.K_2:
                    QuantumCore.graphic.front_face = 'ccw'
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_g:
                    logger.warning('GAME - TEST RISE\n\n')
                    raise Exception("TEST RISE - USE 'raise - Exception' and call traceback")
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_r:
                    settings.rewrite_config()
                    QuantumCore.window.resset()
                
                elif self.spec_keys['L-Ctrl'] and event.key == pygame.K_q:
                    QuantumCore.close()
                    exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.spec_keys['L-Ctrl'] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                """ Detect MOUSE BUTTON DOWN """
    
    @staticmethod
    def get_time() -> None:
        """ updating game time """
        QuantumCore.time.list_['cube animation'] = pygame.time.get_ticks() * 0.001
        QuantumCore.time.list_['earth animation'] = pygame.time.get_ticks() * 0.0001

    def update_app(self) -> None:
        """ updating the application itself (CPU) """
        self.get_time()
        
        """ main update """
        QuantumCore.scene.scene.__update__()

    def update_window(self) -> None:
        """ Rendering the application itself (GPU) """
        
        QuantumCore.scene.scene.__render__()
        
        self.ingame_interface.go(int(self.clock.get_fps()))

        # main pygame updating
        pygame.display.flip()
        QuantumCore.time.delta = self.clock.tick(config.fps)


if __name__ == '__main__':
    mainloop(TestGame)