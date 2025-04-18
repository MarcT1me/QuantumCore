import importlib

import pygame
import QuantumCore
from typing import Callable

_creator: Callable = None


def interface_creator(file_path, file_name, *,
                      init_args=(), init_kwargs=None, go_args=(), go_kwargs=None, frames=10
                      ) -> None:
    if init_kwargs is None: init_kwargs = {}
    if go_kwargs is None: go_kwargs = {}
    
    pygame.init()
    QuantumCore.init()
    
    module = importlib.import_module(f'{".".join(file_path)}.{file_name}')
    last_code = ''
    
    err_font = pygame.font.SysFont('Arial', 60)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuantumCore.close()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    QuantumCore.close()
                    exit()
        
        try:
            with open(
                    rf'{QuantumCore.config.__APPLICATION_PATH__}/{"/".join(file_path)}/{file_name}.itrf', 'r'
            ) as file:
                interface_code = file.read().replace('# Callable: ', '')
                
                if interface_code.count('#uif') or last_code == '':
                    with open(module.__file__, 'r') as file:
                        head_code = file.read().replace('# Callable: ', '')
                        exec(head_code)
                
                exec(interface_code)
                last_code = head_code
                _creator.surface = QuantumCore.window.interface.surface
                _creator(*init_args, **init_kwargs).go(*go_args, **go_kwargs)
        
        except Exception as err:
            try:
                exec(last_code)
            except Exception as err:
                pass
            
            QuantumCore.window.interface.surface.blit(err_font.render(str(err.args[0]), True, 'red'), (0, 0))
        
        # main pygame updating
        clock.tick(frames)
        if interface_code.count('# init'):
            QuantumCore.widgets.Button.roster_relies()


class InterfaceUI:
    def __init__(self, file_path: str, file_name: str, *,
                 init_args=(), init_kwargs: dict = None, go_args=(), go_kwargs: dict = None
                 ) -> None:
        """ Class - reader. from your InTeRface Files """
        if init_kwargs is None: init_kwargs = {}
        if go_kwargs is None: go_kwargs = {}
        
        self.module = importlib.import_module(f'{".".join(file_path)}.{file_name}')
        
        with open(self.module.__file__, 'r') as file:
            head_code = file.read().replace('#Callable: ', '')
            exec(head_code)
        
        with open(rf'{QuantumCore.config.__APPLICATION_PATH__}/{"/".join(file_path)}/{file_name}.itrf', 'r') as file:
            interface_code = file.read().replace('#Callable: ', '')
            exec(interface_code)
        
        _creator.itr = QuantumCore.window.interface
        self.itrf = _creator(*init_args, **init_kwargs)
        self.go = lambda: self.itrf.go(*go_args, **go_kwargs)
    
    @staticmethod
    def set_default_files(path):
        """ Create default interface files (Head and Itrf) """
        
        with open(rf'{path}.py', 'w') as file:
            file.write(
                """#noinspection PyUnresolvedReferences
class Head:
    # Your file imports
    # be sure to create an abbreviation for the import
    
    def __init__(self):
        #Callable: print('creator code')  # real comment
        ...
    ...
"""
            )
        
        with open(rf'{path}.itrf', 'w') as file:
            file.write(
                """#noinspection PyUnresolvedReferences
class Itrf(Head):  #type: core.UI.loading.Head
    
    def go(*args, **kwargs):     # Your methods
        #Callable: print('creator code')  # real comment
        ...
    ...


#noinspection PyUnresolvedReferences
QuantumCore.UI._creator = Itrf
"""
            )
