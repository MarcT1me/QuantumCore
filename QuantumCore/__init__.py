"""
print('Hello world!')
"""
# graphics
from pygame import OPENGL, DOUBLEBUF, HWSURFACE, quit
from moderngl import DEPTH_TEST, BLEND, CULL_FACE

# other
from loguru import logger

# engine elements imports
import QuantumCore.graphic
import QuantumCore.time
import QuantumCore.scene
from QuantumCore.data import config
import QuantumCore.widgets
from QuantumCore.graphic.interface import __AdvancedInterface
import QuantumCore.UI

window = None  # type: QuantumCore.graphic.__GRAPHIC

__version = '0.11'
name, short_name = 'QuantumCore', 'PyQC'

logger.info(f'\n\n{name}: {__version=}\n')
logger.warning('This is an LEARN project written by an ordinary student')


def init(*,
         flags=None
         ) -> None:
    global window
    """ Init Engine """
    if flags is None:
        flags = {
            'pygame': OPENGL|DOUBLEBUF|HWSURFACE,
            'glsl':   DEPTH_TEST|BLEND|CULL_FACE
        }
    window = QuantumCore.graphic.__GRAPHIC(flags)
    if QuantumCore.data.config.PRE_INIT:
        QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh()
    window.interface = __AdvancedInterface()
    QuantumCore.time.delta_time = 0
    logger.success('ENGINE ready\n\n')


def close() -> None:
    """ Correct engine QUIT """
    quit()
    try:
        window.close()
        QuantumCore.graphic.mash.mesh.__destroy__()
    except Exception as exc:
        print(f'\n\n{exc}\n\n')
    
    logger.success('Engine - QUIT')
