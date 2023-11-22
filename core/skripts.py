""" Addicted game core
 """
from os import walk

# engine config import
from QuantumCore.data.config import __APPLICATION_PATH__

# core element
from GameData.settings import MODS_path


class Mods:
    
    PATH = rf'{__APPLICATION_PATH__}/{MODS_path}'
    root, mods_list = None, None

    def __init__(self) -> None: ...
    
    def search(self):
        for root, mod_list, _ in walk(self.PATH):
            self.root, self.mods_list = root, mod_list
            break  # rewrite mods list
        return self
        
    def load(self) -> None:
        for mod in self.mods_list:
            with open(rf'{self.root}/{mod}/__init__.py') as file:
                code = file.read()
                if not code.count(' os' or ' socket' or 'remove'):
                    exec(code)
