""" ErrorMessage for user
 """
# graphic
import pygame

# other
import time
import sys
from loguru import logger
import traceback

# Engine elements
from QuantumCore.data.config import __ENGINE_DATA__
from QuantumCore.data.config import APPLICATION_ICO_path, APPLICATION_ICO_name
import QuantumCore.widgets
import QuantumCore.time


def showTraceback(err, *, flags=pygame.NOFRAME) -> bool:
    """ processing error """
    pygame.quit()
    pygame.init()
    QuantumCore.time.loading = False
    
    # error texts
    caption, format_exc = f'ERROR: {err}', traceback.format_exc()
    logger.exception(f'ERROR: {err}') if "TEST RISE" not in str(err) else Ellipsis

    # background surface
    background = pygame.image.load(rf'{__ENGINE_DATA__}/messages/debug_err.png')
    background_size = .9
    background = pygame.transform.scale_by(background, background_size)
    # text surface
    text_surface = pygame.Surface(background.get_size())
    text_surface.set_colorkey((0, 0, 0))
    clock = pygame.time.Clock()

    """animation"""
    animation_time: float = 1
    background.set_alpha(1)

    """set pygame screen"""
    screen = pygame.display.set_mode(background.get_size(),
                                     flags=flags)
    pygame.display.set_caption(caption)
    pygame.display.set_icon(
        pygame.image.load(rf'{__ENGINE_DATA__}/{APPLICATION_ICO_path}/{APPLICATION_ICO_name}')
    )

    """traceback text variable"""
    default_col = 5
    col: int = default_col
    color_1: int = 1
    color: tuple = (220, 60, 60)
    max_text_lines = screen.get_height()/18

    """ Buttons """
    # first button
    first_font = pygame.font.SysFont('Calibri', 20, bold=True).render(
        f'  In progress been get Exception. to close press:'
        f'esc, quit or  on font  ', True, 'white')
    first_font_pos = (20, 10)
    first_font_rect = pygame.rect.Rect(*first_font_pos, *first_font.get_size())
    # second button
    second_font1 = pygame.font.SysFont('Arial', 18).render(
        f'We have`t check your logs, but you cen believe that we already working on it bug',
        True, (150, 220, 220))
    second_font1_pos = (10, (max_text_lines + 2) * 15 - 5)

    second_font2 = pygame.font.SysFont('Arial', 15).render(
        f'  that restart press R or on font  ', True, (220, 220, 150))
    second_font2_pos = (10, (max_text_lines + 3) * 15)
    second_font2_rect = pygame.rect.Rect(*second_font2_pos, *second_font2.get_size())

    """ Error text """
    def add_text(*, nl=False):
        text_lines.append({
            'text': '',
            'pos_variable': [col, line],
            'color': color,
            'count': nl,
        })
        
    line: int = 3
    text_lines = list()
    add_text()
    
    # text processing
    for symbol in format_exc:
        if symbol == f'\n':
            col = default_col
            line += 1
            add_text(nl=True)
        else:
            if line <= max_text_lines:
                col += 1
                if symbol == '"' and symbol != '\n':
                    color_1 *= -1
                    color = (255, 60, 60) if color_1 == 1 else (250, 250, 250)
                    add_text()
            
                text_lines[-1]['text'] += str(symbol)
                text_lines[-1]['pos_variable'] = [min(col, text_lines[-1]['pos_variable'][0]), line]
                text_lines[-1]['color'] = color
    
    # render surface
    pust_font_width = 0
    for text_line in text_lines:
        current_pos = text_line['pos_variable']
        text_font = pygame.font.SysFont('Calibri', 15, bold=True).render(
            f'{text_line["text"]}' if col <= 87 else '.', True, text_line['color'])
    
        text_surface.blit(
            text_font, (current_pos[0] + pust_font_width if not text_line['count'] else 0,
                        current_pos[1] * 15 - text_font.get_height() // 2)
        )
        pust_font_width = text_font.get_width()

    start_time: float = time.time()
    while True:
        """events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    pygame.quit()
                    return True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and second_font2_rect.collidepoint(*pygame.mouse.get_pos()):
                    pygame.quit()
                    return True
                elif event.button == 1 and first_font_rect.collidepoint(*pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        """Update window"""
        screen.fill((0, 0, 0))

        t = time.time() - start_time
        background.set_alpha(int(t/animation_time*100) if t <= animation_time else 100)
        screen.blit(background, (0, -20 / (.75/background_size)))
        
        # error text
        screen.blit(text_surface, (0, 0))
        
        # buttons
        pygame.draw.rect(screen, 'gray', first_font_rect, 1), pygame.draw.rect(screen, 'gray', second_font2_rect, 1)
        pygame.draw.line(screen, (150, 150, 150),
                         (0, (max_text_lines+1)*15+5),
                         (screen.get_width(), (max_text_lines+1)*15+5), 4)
        
        screen.blit(first_font, first_font_pos)
        screen.blit(second_font1, second_font1_pos), screen.blit(second_font2, second_font2_pos)
        
        # default pygame methods
        pygame.display.flip(), clock.tick(30)
        

blit_list = [1, 1, 1, 1, 1, 1]


def showWindow(err, *, caption='Error Message', custom_surf=None, flags=pygame.NOFRAME) -> bool:
    """ processing error """
    pygame.quit()
    pygame.init()
    QuantumCore.time.loading = False
    logger.exception(f'ERROR: {err}') if "TEST RISE" not in str(err) else Ellipsis
    
    custom_surf, custom_surf_arg = pygame.Surface((270, 110)), custom_surf
    custom_surf.fill((0, 255, 0))
    if custom_surf_arg == 'base':
        custom_surf.blit(
            pygame.font.SysFont('Verdana', 40, bold=True).render(
                'Quantum', False, 'black'
            ),
            (7, 0)
        )
        custom_surf.blit(
            pygame.font.SysFont('Verdana', 40, bold=True).render(
                'Game', False, 'black'
            ),
            (112, 51)
        )
    if custom_surf_arg != 'fill':
        custom_surf.set_colorkey((0, 255, 0)) if custom_surf is not None else Ellipsis

    """ Working with pygame """
    clock = pygame.time.Clock()
    # process background
    background = pygame.image.load(rf'{__ENGINE_DATA__}/messages/err_background.png')
    background = pygame.transform.scale_by(background, .75)
    # screen
    screen_size = background.get_size()
    screen = pygame.display.set_mode(screen_size, flags=flags)
    white_surf = pygame.Surface(screen_size); white_surf.fill('white')
    pygame.display.set_icon(pygame.image.load(rf'{__ENGINE_DATA__}/{APPLICATION_ICO_path}/{APPLICATION_ICO_name}'))
    # caption
    pygame.display.set_caption(str(caption))
    
    def exit_func(res):
        nonlocal result, running
        result, running = res, False
    
    """ fonts and other graphic """
    def restart_btn(): exit_func(True)
    def exit_btn(): exit_func(False)
    btn1 = QuantumCore.widgets.Button(size=(302, 40), pos=(10, screen_size[1]-50),
                                      text='Restart', font='Unispace', text_size=45, text_bold=False,
                                      bgcolor_on_press=(150, 150, 150),
                                      text_pos=(151, 20), text_center=True,
                                      on_press=restart_btn)
    QuantumCore.widgets.Button(size=(302, 40), pos=(btn1.size[0]+30, btn1.pos[1]),
                               text='Exit', font='Unispace', text_size=45, text_bold=False,
                               bgcolor_not_press=(255, 50, 50), bgcolor_on_press=(255, 120, 120),
                               text_center=True, text_pos=(151, 20),
                               on_press=exit_btn)
    font_color = (50, 50, 50)
    err_text_font = pygame.font.SysFont('Unispace', 30).render(
        str(err), True, font_color
    )
    err_type_font = pygame.font.SysFont('Unispace', 30).render(
        f'type: {str(type(err))[8:-2]}', True, font_color
    )
    err_message_font = pygame.font.SysFont('Unispace', 30).render(
        'message - in dev', True, font_color
    )
    err_description_font = pygame.font.SysFont('Unispace', 30).render(
        'description - in dev', True, font_color
    )
    help_font = pygame.font.SysFont('Unispace', 30).render(
        "press on 'BUTTON' or 'R' to restart and 'BUTTON', 'Esc' or 'QUIT'", True, (20, 20, 20)
    )
    
    result: bool = False
    running: bool = True
    while running:
        """err while"""
        
        """ events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_func(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_func(False)
                elif event.key == pygame.K_r:
                    exit_func(True)
            QuantumCore.widgets.Button.roster_event(event)
        
        """ render """
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(err_text_font, (screen_size[0]-err_text_font.get_width()-30, 20)) if blit_list[0] else Ellipsis
        screen.blit(err_type_font, (130, 300)) if blit_list[1] else Ellipsis
        screen.blit(err_message_font, (20, 345))  if blit_list[2] else Ellipsis
        screen.blit(err_description_font, (20, 375))  if blit_list[3] else Ellipsis
        screen.blit(custom_surf, (780, 345)) if custom_surf is not None and blit_list[4] else Ellipsis
        screen.blit(help_font, (12, 420)) if custom_surf is not None and blit_list[5] else Ellipsis
        QuantumCore.widgets.Button.roster_render(screen)
        
        """ __PyGame__ """
        pygame.display.flip(), clock.tick(60)
    pygame.quit()
    QuantumCore.widgets.Button.roster_relies()
    return result


if __name__ == '__main__':
    try:
        try: raise UnicodeDecodeError('UTF-8', b'\\', 0, 0, 'err')
        except Exception as exc: print(showWindow(exc, custom_surf='base'))
    except Exception as err:
        import traceback; traceback.print_exception(err)
        input()
        
