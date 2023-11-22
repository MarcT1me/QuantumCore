
# noinspection PyUnresolvedReferences
class Head:
    fps_fonts_colors = ('red', 'orange', 'yellow', 'green', 'cyan')
    
    def __init__(self):
        from GameData.settings import  APPLICATION_VERSION
        
        self.application_version_font = pygame.font.SysFont('Arial', 25, bold=True).render(
            f'{APPLICATION_VERSION}', False, 'white'
        )
        self.fps_font = pygame.font.SysFont('Arial', 25, bold=True)
