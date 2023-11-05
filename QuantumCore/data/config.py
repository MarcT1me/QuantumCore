""" Engine configuration
 """
from pygame.display import init as display_init, get_desktop_sizes
from inspect import stack; from os.path import dirname, abspath

""" Application settings """
# path variable
__APPLICATION_FOLDER__: str = dirname(abspath(stack()[1].filename)).removesuffix('\\PyInstaller\\loader')  # dynamic
__ENGINE_FOLDER__: str = dirname(abspath(__file__)).removesuffix('\\PyInstaller\\loader')[0:-5]  # dynamic
SHADER_path: str = r'graphic/shaders'  # constant
TEXTURE_path: str = r'data/textures'   # constant

APPLICATION_ICO_path, APPLICATION_ICO_name = r'QuantumCore/data', 'standard.png'  # dynamic

PRE_INIT: bool    # constant  # .CONFIG
IS_RELEASE: bool  # constant  # .CONFIG

""" Screen settings """
fps: int = 0              # easy
full_screen: bool = True  # easy
DISPLAY_num: int = 0      # heavy
_, SCREEN_size = display_init(), get_desktop_sizes()[DISPLAY_num]  # dynamic

""" Render settings """
SHADER_NAME: tuple = 'default', 'default'  # heavy  # .CONFIG
__CONTEXT_SIZE__: tuple = SCREEN_size      # heavy
VSYNC: bool = False                        # heavy

""" Mouse & KeyBord settings """
sensitivity: float = 0.05  # heavy

""" Shaders settings """
FOV: float = 60     # heavy
FAR: int = 1000     # heavy
GAMMA: float = 2.2  # heavy

NEAR: float   # constant  # .CONFIG
AA_TYPE: int  # constant  # .CONFIG


with open(rf'{__ENGINE_FOLDER__}/data/settings.config', 'r') as config:
    exec(config.read())

with open(rf'{__ENGINE_FOLDER__}/data/graphic.config', 'r') as config:
    exec(config.read())
    