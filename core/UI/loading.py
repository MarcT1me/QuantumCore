
#noinspection PyUnresolvedReferences
class Head:
    def __init__(self):
        from QuantumCore.data.config import __APPLICATION_PATH__, SCREEN_size
        
        self.background = (
            pygame.transform.scale(pygame.image.load(
                    f'{__APPLICATION_PATH__}/core/textures/loading_image.jpg'
                ), SCREEN_size
            ), (0, 0)
        )
        self.loading_font = (
            pygame.font.SysFont('Unispace', 300).render('Loading', True, (50, 50, 50)),
            (50, 200)
        )
        
        self.percent_font = pygame.font.SysFont('Unispace', 50)
        self.stage_font = pygame.font.SysFont('Unispace', 60)
        
        self.get_line_rect = lambda value: pygame.Rect(20, SCREEN_size[1]-40, (SCREEN_size[0]-40)/100*value, 20)
        