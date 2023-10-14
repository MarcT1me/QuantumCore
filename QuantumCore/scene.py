
# other
from copy import copy
import pickle
from datetime import datetime
import time

import QuantumCore.graphic
# engine elements imports
from QuantumCore.data import config


class Location:
    def __init__(self, app) -> None:
        """ Base location """
        self.app = app
        
        self.objects_list: dict[hash: object] = dict()
        self.lights_list: dict[hash: object] = copy(QuantumCore.graphic.light.lights_list)
        
        self.render_area = config.FAR*1.2
        
        self.builder = None
        self.ids: dict[str: hash] = dict()
        
        self.game_time = 0

    def __add_object(self, obj) -> int:
        """ add object in list """
        __id = id(obj)
        self.objects_list[__id] = obj
        return __id
    
    def __add_light(self, light) -> int:
        __id = id(light)
        self.lights_list[0][__id] = light
        return __id

    @staticmethod
    def build(app, obj, light) -> None:
        """ Write all the objects of the scene to this method """
        ...
    
    def unload(self):
        """ Unload scene """

        """ work with scene itself """
        self.objects_list.clear()
        """ clear all graphic lists """
        QuantumCore.graphic.vbo.CustomVBO_name.clear()
        QuantumCore.graphic.texture.CustomTexture_name.clear()
        QuantumCore.graphic.light.lights_list.clear()
        """ work with mash """
        QuantumCore.graphic.mash.mesh.__destroy__()

    def load(self) -> None:
        """  """
        app = self.app
        add_obj = self.__add_object
        add_light = self.__add_light
        
        self.build(app, add_obj, add_light)
    
    def __update__(self):
        QuantumCore.graphic.camera.camera.update()
        
    def __render__(self) -> None:
        QuantumCore.graphic.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        [entity.__render__() for entity in self.objects_list.values()]
    
    
scene: Location = None


class Builder:
    
    def __init__(self, target: str, *, scene=None) -> None:
        self.path: str = target
        self.scene: Location = scene
        
        self.root = lambda: ' '.join(self.path.split('/')[0:-1])
        self.name = lambda: self.path.split('/')[-1]
        self.time = datetime.fromtimestamp(time.time()).strftime("%d.%m.%y %H:%M:%S")
        
        self.save = None
    
    def format_sav(self):
        return {
            'file': {
                'root': self.root(),
                'name': self.name()
            },
            'time': {
                'system': self.time,
                'in game': self.scene.game_time
            },
            'scene': self.scene
        }
    
    def dump(self):
        if self.scene is not None:
            with open(self.path, 'wb') as file:
                pickle.dump(self.format_sav(), file)
    
    def load(self):
        with open(self.path, 'rb') as file:
            self.save = pickle.load(file)
            return self.save
