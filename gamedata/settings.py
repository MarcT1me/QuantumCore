""" Game settings.
 """
from QuantumCore.data import config
import json  # for rewrite engine configs

""" Application settings """
APPLICATION_NAME: str = 'QuantumGame'
APPLICATION_VERSION: str = '0.4.3'

""" Path settings """
MODEL_path: str = r'core/models'
TEXTURE_path: str = r'core/textures'
MODS_path: str = r'gamedata/mods'
SAVES_path: str = r'gamedata/saves'


""" Settings functional """
datafile = None


def _read_datafile_():
    """ Read CONFIG files """
    with open(rf"{config.__APPLICATION_FOLDER__}/gamedata/config.json") as file:
        return json.load(file)


def rewrite_config():
    """ Rewrite CONFIG data """
    global datafile
    datafile = _read_datafile_()
    
    for key, value in datafile['engine'].items():
        exec(f"""config.{key} = {value}""")
