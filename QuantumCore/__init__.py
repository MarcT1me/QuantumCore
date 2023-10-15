"""
print('Hello world!')
"""
import pygame  # graphics

# other
from loguru import logger
from pprint import pformat
import sys

# engine elements imports
import QuantumCore.graphic
import QuantumCore.time
import QuantumCore.scene

__version = '0.9.4:1'
name, short_name = 'QuantumCore', 'PyQC'

__authors: dict = {
    'programmers': {
        'CoreTech programmers': 'Timur Shestakov',
        'Gameplay programmers': ('Timur Shestakov', 'Dmitry Shcherbinin'),
        'DevOps engineer': ('Nikita Usachyov', 'Emil Akhmetov', 'Dmitry Shcherbinin'),
        'Web programmer ': ('Timur Shestakov', 'Dmitry Shcherbinin'),
    },
    'Tester and QA engineers': 'Emil Akhmetov',
    '3d artists': None,
    'composers': 'Dmitry Shcherbinin'
}

logger.info(f'\n\n{name}: {__version=}\n')
logger.info(f'\n\n{pformat(__authors)}\n')


def init() -> None:
    """ Init Engine """
    QuantumCore.graphic._init_()
    QuantumCore.time.delta_time = 0
    logger.debug('ENGINE ready\n\n')


def __quit__() -> None:
    """ Correct engine QUIT """
    logger.debug('GAME - QUIT')
    QuantumCore.graphic.mash.mesh.__destroy__()
    pygame.quit()
    sys.exit()
