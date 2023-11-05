import time

import pygame
from pygame._sdl2 import Window, Renderer, Texture


class ConfirmWin:
    def __init__(self, *, caption=None, size=(300, 200), opacity=0.75) -> None:
        """ init confirm window class """
        self.win: Window = Window(str(caption), size=size)
        self.win.opacity = opacity
        self.rend: Renderer = Renderer(self.win)
        self.surf: pygame.Surface = pygame.Surface(size=size)
        self.__rend_surf: Texture = None
    
    def on_init(self) -> None:
        self.update()
        self.render()
        
    def event(self, event: pygame.event.Event) -> None:
        if getattr(event, 'window', None) == self.win:
            if event.type == pygame.WINDOWCLOSE:
                self.win.destroy()
    
    def update(self) -> None:
        self.__rend_surf = Texture.from_surface(self.rend, self.surf)
    
    def render(self) -> None:
        self.rend.clear()
        self.__rend_surf.draw()
        self.rend.present()


class Button:
    roster = list()
    
    def __init__(self, *,
                 # WINDOW
                 size: tuple[int, int] = (100, 100),
                 pos: tuple[int, int] = (0, 0),
                 source: str = None,
                 image_pos: tuple = (0, 0),
                 # TEXT
                 text: str = '',
                 text_size: int = 20,
                 text_pos: tuple = (0, 0),
                 text_center: bool = False,
                 text_clor: tuple[int, int, int] = (220, 220, 220),
                 text_bold: bool = True,
                 # COLORS
                 font: str = 'Arial',
                 bgcolor_on_press: tuple[int, int, int] = (100, 150, 250),
                 bgcolor_not_press: tuple[int, int, int] = (120, 120, 120),
                 # FUNCTIONAL
                 on_press=lambda: None,
                 on_release=lambda: None,
                 release_long: float = 1
                 ) -> None:
        """ Init Button class """
        
        """ RECT """
        self.pos: tuple = pos
        self.size: tuple = size
        
        """ IMAGE """
        self.image = pygame.transform.scale(pygame.image.load(source), size) if source is not None else None
        self.image_pos = image_pos
        
        """ TEXT """
        self.text: str = text
        self.text_size: tuple = text_size
        self.text_clor: tuple = text_clor
        self.font = pygame.font.SysFont(font, self.text_size, bold=text_bold).render(self.text, True, self.text_clor)
        self.font_size: tuple = self.font.get_size()
        self.text_pos: tuple = (
            text_pos[0]-self.font.get_width()//2, text_pos[1]-self.font.get_height()//2
        ) if text_center else text_pos
        
        """ SURFACE """
        self.surf = pygame.Surface(size)
        self.bgcolor_on_press: tuple = bgcolor_on_press
        self.bgcolor_not_press: tuple = bgcolor_not_press
        self.surf_color: tuple = bgcolor_not_press
        self.surf.set_colorkey(self.surf_color) if self.image is not None else Ellipsis
        
        """ FUNCTION """
        self.release_start = None
        self.release_long = release_long
        
        self.on_press = on_press
        self.on_release = on_release
        self.roster.append(self)
        
    def event(self, event: pygame.event.Event) -> None:
        """ События кнопки, нажатие (короткое/долгое) и реализация функционала """
        if self.release_start is not None:
            if self.release_start + self.release_long <= time.time():
                """ Долгое удержание """
                self.on_release()  # долгое нажатие
                
                self.release_start = None  # сброс значений нажатия
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            """ Нажатие """
            if pygame.rect.Rect(*self.pos, *self.size).collidepoint(pygame.mouse.get_pos()):
                # изменение цвета на активное
                self.surf_color = self.bgcolor_not_press if self.image is not None else self.bgcolor_on_press
                
                if self.release_start is None:  # ставлю значение нажатия
                    self.release_start = time.time()
                    
            else:
                self.surf_color = self.bgcolor_not_press
                
        elif event.type == pygame.MOUSEBUTTONUP:
            """ Отжатие """
            self.surf_color = self.bgcolor_not_press    # изменение цвета на не активное
            
            if self.release_start is not None:
                if self.release_start + self.release_long >= time.time():
                    """ Недолгое удержание """
                    self.on_press()  # недолгое нажатие
                
                self.release_start = None  # сброс значений нажатия
    
    def render(self, win) -> None:
        """ Render button.   всегда один подход   """
        self.surf.fill(self.surf_color)
        
        self.surf.blit(self.image, self.image_pos) if self.image is not None else Ellipsis
        self.surf.blit(self.font, self.text_pos)  # отображение текста и изображения кнопки
        
        win.blit(self.surf, self.pos)
    
    def relies(self):
        self.roster.remove(self)
    
    @staticmethod
    def roster_event(event):
        for btn in Button.roster:
            btn.event(event)

    @staticmethod
    def roster_render(win):
        for btn in Button.roster:
            btn.render(win)
        
    @staticmethod
    def roster_relies():
        for btn in Button.roster:
            btn.relies()


"""class Main:
    pygame.mixer.init()
    pygame.mixer_music.load('123.mp3')
    img = pygame.transform.scale(pygame.image.load('img.png'), (100, 100))
    
    FPS = 60
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((600, 400))
        
        self.conf_win = ConfirmWin()
        self.conf_win.surf.blit(
            pygame.font.SysFont('Arial', 15).render('вы уверены?', True, 'red'),
            (0, 0)
        )
        self.conf_win.on_init()
        
        self.btn = Button(pos=(150, 100), size=(100, 100),
                          release_long=0.0, on_release=self.release,
                          source='fg3.png')
        self.exit_btn = Button(pos=(0, 350), size=(600, 50),
                               release_long=0.0, on_release=sys.exit,
                               text_pos=(300, 25), text_center=True, text='Exit', text_size=30,
                               bgcolor_not_press=(250, 100, 100), bgcolor_on_press=(250, 200, 200))
        
        self.event_list = None
    
    def release(self):
        self.img = pygame.transform.rotate(self.img, 90)
        pygame.mixer.music.play()

    @staticmethod
    def press():
        pygame.mixer.music.play()
    
    def run(self):
        while True:
            
            self.events()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def events(self):
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                sys.exit()
            # self.conf_win.event(event)
            self.btn.event(event)
            self.exit_btn.event(event)
    
    def update(self):
        pygame.display.set_caption(str(self.clock.get_fps()))
    
    def render(self):
        self.window.fill((90, 90, 90))
        self.window.blit(self.img, (300, 0))
        self.btn.render(self.window)
        self.exit_btn.render(self.window)


if __name__ == '__main__':
    Main().run()"""
        