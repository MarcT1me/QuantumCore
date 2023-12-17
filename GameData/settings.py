""" Game settings.
 """
from QuantumCore.data import config
import json  # for rewrite engine configs

""" Application settings """
APPLICATION_NAME: str = 'QuantumGame'
APPLICATION_VERSION: str = '0.4.4'

""" Path settings """
MODEL_path: str = r'core/models'
TEXTURE_path: str = r'core/textures'
MODS_path: str = r'GameData/mods'
SAVES_path: str = r'GameData/saves'


""" Settings functional """
datafile = None


def _read_datafile_():
    """ Read CONFIG files """
    with open(rf"{config.__APPLICATION_PATH__}/GameData/config.json", mode='r') as file:
        return json.load(file)

<<<<<<< HEAD
=======
def change_datafile(changes):
    """ Change data in datafile variable """
    for field, data in changes.items():
        for key, value in data.items():
            datafile[field][key] = value

def write_datafile(changes: dict[str: dict] =None):
    """ Write CONFIG files """
    change_datafile(changes) if changes is not None else Ellipsis
    
    with open(rf"{config.__APPLICATION_PATH__}/GameData/config.json", mode='w') as file:
        json.dump(datafile, file, indent=2)

>>>>>>> 60d7484 (0.5.2:r2)

def rewrite_config():
    """ Rewrite CONFIG data """
    global datafile
    datafile = _read_datafile_()
    
    for key, value in datafile['engine'].items():
        exec(f"""config.{key} = {value}""")
