""" Engine time counter
Total time management file for all engine functions
uses the time module

DESCRIPTION OF VARIABLES
delta - Время между 2-мя итерациями цикла App
start - Временная отметка с запуска программы (import)

list_ - Список счётчиков
dict_ - Список секундомеров
 """
from time import time

delta: float = 0
start: float = time()

list_: dict = {
    'cube animation':  0,
    'earth animation': 0
}
dict_: dict = {
    ...
}
