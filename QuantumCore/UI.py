import importlib

import pygame
import QuantumCore
from typing import Callable

_creator: Callable = None


def interface_creator(file_path, file_name, *, init_args=(), init_kwargs={}, go_args=(), go_kwargs={}, frames=10):
    pygame.init()
    QuantumCore.init()
    
    module = importlib.import_module(f'{".".join(file_path)}.{file_name}')
    last_code = ''
    
    err_font = pygame.font.SysFont('Arial', 60)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                QuantumCore.close()
                exit()
        
        try:
            with open(rf'{QuantumCore.config.__APPLICATION_PATH__}/{"/".join(file_path)}/{file_name}.itrf', 'r') as file:
                interface_code = file.read()
        
                if interface_code.count('# init') or last_code == '':
                    with open(module.__file__, 'r') as file:
                        head_code = file.read()
                        exec(head_code)
                
                exec(interface_code)
                last_code = head_code
                    
                _creator(*init_args, **init_kwargs).go(*go_args, **go_kwargs)
                
        except Exception as err:
            try:
                exec(last_code)
            except Exception as err:
                pass
            QuantumCore.window.interface.surface.blit(err_font.render(str(err.args[0]), True, 'red'), (0, 0))
        
        # main pygame updating
        QuantumCore.window.interface.nonscene_render()
        clock.tick(frames)
        if interface_code.count('# init'):
            QuantumCore.widgets.Button.roster_relies()
