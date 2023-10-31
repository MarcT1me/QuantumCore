"""
print('Hello world!')
"""
# graphics
from pygame import OPENGL, DOUBLEBUF, HWSURFACE, quit
from moderngl import DEPTH_TEST, BLEND  # CULL_FACE

# other
from loguru import logger
from pprint import pformat
import sys

# engine elements imports
import QuantumCore.graphic
import QuantumCore.time
import QuantumCore.scene
from QuantumCore.graphic.shaders.interface import __Interface
window: QuantumCore.graphic.__GRAPHIC = None

__version = '0.10.3'
name, short_name = 'QuantumCore', 'PyQC'

__authors: dict = {
    'programmers': {
        'CoreTech programmers': 'Timur Shestakov',
        'DevOps engineer': ('Nikita Usachyov', 'Emil Akhmetov'),
    },
    'Tester and QA engineers': 'Emil Akhmetov',
    '3d artists': None
}

logger.info(f'\n\n{name}: {__version=}\n')
logger.info(f'\n\n{pformat(__authors)}\n')
logger.warning('This is LEARN project writen just student')


def init(*,
         flags=None) -> None:
    global window
    """ Init Engine """
    if flags is None:
        flags = {'pygame': OPENGL | DOUBLEBUF | HWSURFACE,
                 'glsl': DEPTH_TEST | BLEND}  # CULL_FACE
    window = QuantumCore.graphic.__GRAPHIC(flags)
    QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh()
    window.interface = __Interface()
    QuantumCore.time.delta_time = 0
    logger.success('ENGINE ready\n\n')


def __quit__() -> None:
    """ Correct engine QUIT """
    logger.success('Engine - QUIT')
    quit()
    QuantumCore.graphic.mash.mesh.__destroy__()
    QuantumCore.window.context.release()
    sys.exit('success game exit')
