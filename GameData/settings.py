""" Game settings.
 """
from QuantumCore.data import config
import toml  # for rewrite engine configs

""" Application settings """
APPLICATION_NAME: str = 'QuantumGame'
APPLICATION_VERSION: str = '0.5.2'

""" Path settings """
MODEL_path: str = r'core/models'
TEXTURE_path: str = r'core/textures'
MODS_path: str = r'GameData/mods'
SAVES_path: str = r'GameData/saves'
# data in file
datafile: dict

""" other """
save_name: str
autosave: bool = False



def read_datafile_():
    """ Read CONFIG files """
    with open(rf"{config.__APPLICATION_PATH__}/GameData/config.toml", mode='r') as file:
        return toml.load(file)
    
def change_datafile(changes):
    """ Change data in datafile variable """
    for field, data in changes.items():
        for key, value in data.items():
            datafile[field][key] = value

def write_datafile(changes: dict[str: dict] =None):
    """ Write CONFIG files """
    change_datafile(changes) if changes is not None else Ellipsis
    
    with open(rf"{config.__APPLICATION_PATH__}/GameData/config.toml", mode='w') as file:
        toml.dump(datafile, file)


def rewrite_config():
    """ Rewrite CONFIG data """
    global datafile
    datafile = read_datafile_()
    
    for key, value in datafile['engine'].items():
        exec(f"""config.{key} = {value}""")
    
    for key, value in datafile['game'].items():
        globals()[key] = value
