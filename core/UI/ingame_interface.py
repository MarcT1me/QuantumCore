
# noinspection PyUnresolvedReferences
class Head:
    import pygame
    import QuantumCore
    
    def __init__(self):
        from GameData import settings
        
        self.application_version_font = pygame.font.SysFont('Arial', 25, bold=True).render(
            f'{settings.APPLICATION_VERSION}', False, 'white'
        )
        self.fps_font = pygame.font.SysFont('Arial', 25, bold=True)
