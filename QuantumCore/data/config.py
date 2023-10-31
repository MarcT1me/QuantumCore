""" Engine configuration
 """
from pygame.display import init as display_init, get_desktop_sizes  # screen size variable
from inspect import stack; from os.path import dirname, abspath  # path

""" Application settings """
__APPLICATION_FOLDER__: str = dirname(abspath(stack()[1].filename)).removesuffix('\\PyInstaller\\loader')
SHADER_path: str = r'QuantumCore/graphic/shaders'
TEXTURE_path: str = r'QuantumCore/data/textures'

APPLICATION_ICO_path, APPLICATION_ICO_name = r'QuantumCore/data', 'standard.png'

""" Screen settings """
fps: int = 0
full_screen: bool = True
DISPLAY_num: int = 0
_, SCREEN_size = display_init(), get_desktop_sizes()[DISPLAY_num]

""" Render settings """
shader_name: tuple = 'default', 'default'
__CONTEXT_SIZE__: tuple = SCREEN_size
vsync: bool = False

""" Mouse & KeyBord settings """
sensitivity: float = 0.05

""" Shaders settings """
FOV: float = 60
NEAR: float = 0.05
FAR: int = 1000
GAMMA: float = 2.2
