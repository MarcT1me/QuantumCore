import pygame
import glm

# import Engine
try:
    import QuantumCore
except Exception as err:
    import traceback; traceback.print_exception(err)
    input()

pygame.init()

if __name__ == '__main__':
    img = pygame.image.load(f'{QuantumCore.config.__ENGINE_DATA__}/textures/test_texture.jpg')
    
    surf = pygame.Surface(img.get_size())
    surf.blit(img, (0, 0))
    
    # Окно игры: размер, позиция
    win = pygame.display.set_mode((200, 200))
    cwin = []
    def add():
        cwin.append(
            QuantumCore.widgets.ConfirmWin(
                size=surf.get_size()*glm.vec2(0.5),
                opacity=0.5,
                pos=(-surf.get_width()*0.5//2, 1080//2-100)
            ).set(
                surf
            )
        )
        cwin[-1].win.resizable = True
    
    clock = pygame.time.Clock()
    
    f1 = pygame.font.SysFont('Arial', 15)
    
    k1 = [0, 0]
    k = [0, 0, 0, 0]
    
    QuantumCore.widgets.Button(
        on_press= add,
        pos=(0, 50),
        size=(200, 150)
    )
    
    add()
    event_window = cwin[0]
    
    running = True
    while running:
        """ event """
        for event in pygame.event.get():
            event_window = QuantumCore.widgets.event_window(event)
            
            if event_window is None:
                if event.type == pygame.WINDOWCLOSE:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        for i in cwin:
                            i.win.show()
                QuantumCore.widgets.Button.roster_event(event)
            if event_window in [cw.win for cw in cwin]:
                if event.type == pygame.WINDOWCLOSE:
                    event_window.destroy()
                    k1 = [0, 0]
                    k = [0, 0, 0, 0]
                
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP:
                        k1[0] = 1
                    elif event.key == pygame.K_DOWN:
                        k1[1] = 1
                        
                    elif event.key == pygame.K_w:
                        k[0] = 1
                    elif event.key == pygame.K_a:
                        k[1] = 1
                    elif event.key == pygame.K_s:
                        k[2] = 1
                    elif event.key == pygame.K_d:
                        k[3] = 1
                        
                    elif event.key == pygame.K_RETURN:
                        event_window.hide()
                
                elif event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_UP:
                        k1[0] = 0
                    elif event.key == pygame.K_DOWN:
                        k1[1] = 0
                    
                    if event.key == pygame.K_w:
                        k[0] = 0
                    elif event.key == pygame.K_a:
                        k[1] = 0
                    elif event.key == pygame.K_s:
                        k[2] = 0
                    elif event.key == pygame.K_d:
                        k[3] = 0
        
        """ update """
        try:
            if k1[0]:
                event_window.opacity += .01
            if k1[1]:
                event_window.opacity -= .01
                
            if k[0]:
                event_window.position = event_window.position[0], event_window.position[1] - 5
            if k[1]:
                event_window.position = event_window.position[0] - 5, event_window.position[1]
            if k[2]:
                event_window.position = event_window.position[0], event_window.position[1] + 5
            if k[3]:
                event_window.position = event_window.position[0] + 5, event_window.position[1]
        except:
            pass
        
        """ render """
        win.fill('sea green')
        try:
            win.blit(f1.render(f'opacity = {round(event_window.opacity, 2)}, position = {event_window.position}', True, 'white'), (0, 0))
        except:
            pass
        QuantumCore.widgets.Button.roster_render(win)
        
        pygame.display.flip()
        clock.tick(120)
