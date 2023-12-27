import pygame.transform


# noinspection PyUnresolvedReferences
class Head:
    fps_fonts_colors = ('red', 'orange', 'yellow', 'green', 'cyan')

    import QuantumCore
    qc_cfg = QuantumCore.config
    from pygame import draw
    draw = draw
    
    def __init__(self):
        from GameData.settings import  APPLICATION_VERSION
        
        self.application_version_font: pygame.font.SysFont = pygame.font.SysFont('Arial', 25, bold=True).render(
            f'{APPLICATION_VERSION}', False, 'white'
        ).convert_alpha()
        
        self.crosshair: pygame.image.load = pygame.image.load(
            rf'{self.qc_cfg.__APPLICATION_PATH__}/core/textures/crosshair.png'
        ).convert_alpha()
        
        self.crosshair = pygame.transform.scale_by(self.crosshair, 0.3)
        self.crosshair.set_colorkey('white')
        self.fps_font = pygame.font.SysFont('Arial', 25, bold=True)
