
#noinspection PyUnresolvedReferences
class Head:
    from QuantumCore.data.config import __APPLICATION_PATH__, SCREEN_size
    import time
    app_path = __APPLICATION_PATH__
    sc_size = SCREEN_size
    sleep = time.sleep
    
    def __init__(self):
        self.background = (
            pygame.transform.scale(pygame.image.load(
                    f'{self.app_path}/core/textures/loading_image.jpg'
                ), self.sc_size
            ), (0, 0)
        )
        self.loading_font = (
            pygame.font.SysFont('Unispace', 300).render('Loading', True, (50, 50, 50)),
            (50, 200)
        )
        
        self.percent_font = pygame.font.SysFont('Unispace', 50)
        self.stage_text = ''
        self.stage_font = pygame.font.SysFont('Unispace', 60)
        self.status_font = pygame.font.SysFont('Unispace', 35)
        
        self.get_line_rect = lambda value: pygame.Rect(20, self.sc_size[1]-40, (self.sc_size[0]-40)/100*value, 20)
        