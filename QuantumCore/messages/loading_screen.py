# graphic
import pygame

# other
import sys
from loguru import logger

# Engine elements
from QuantumCore.data.config import __ENGINE_DATA__, DISPLAY_num
from QuantumCore.data.config import APPLICATION_ICO_path, APPLICATION_ICO_name


def showWindow(*, bg_img_path=r'messages/default_loading_background.png',
               bg_size=(800, 400), caption='QuantumGame - loading', flags=pygame.NOFRAME
               ):
    """ show that game loading in progress """
    pygame.init()
    
    screen_size = bg_size if bg_size[0] >= 200 and bg_size[1] >= 150 else (400, 300)
    """ background surface """
    background = pygame.transform.scale(
        pygame.image.load(rf'{__ENGINE_DATA__}/{bg_img_path}'),
        screen_size
    )
    
    """ set pygame screen """
    window = pygame.display.set_mode(screen_size, display=DISPLAY_num, flags=flags)
    pygame.display.set_caption(caption)
    pygame.display.set_icon(
        pygame.image.load(rf'{__ENGINE_DATA__}/{APPLICATION_ICO_path}/{APPLICATION_ICO_name}')
    )
    
    """ fonts """
    powered_by_font = pygame.font.SysFont('Verdana', 20).render('powered by', True, 'darkgray')
    PyQC_font = pygame.font.SysFont('Unispace', 45).render('PyQC', True, 'darkgray')
    powered_by_font_pos = (
        screen_size[0]-(PyQC_font.get_width()+powered_by_font.get_width()+20),
        screen_size[1]-(PyQC_font.get_height()+10)
    )
    PyQC_font_pos = (
        screen_size[0]-(PyQC_font.get_width()+10),
        screen_size[1]-(PyQC_font.get_height()+10)
    )
    
    logger.debug('Loading - start')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.blit(background, (0, 0))
        window.blit(powered_by_font, powered_by_font_pos)
        window.blit(PyQC_font, PyQC_font_pos)
        pygame.display.flip()


if __name__ == '__main__':
    try:
        showWindow(flags=0)
    except Exception as err:
        import traceback
        
        traceback.print_exception(err)
        input()
