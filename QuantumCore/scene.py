import uuid
# other
from copy import copy
import pickle
import os.path
from loguru import logger

import QuantumCore.graphic
from QuantumCore.model import BaseModel
# engine elements imports
from QuantumCore.data import config


class Location:
    increment = 1
    
    def __init__(self, app) -> None:
        """ Base location """
        self.app = app
        
        """ scene space """
        self.objects_list: dict[str: object] = dict()
        self.lights_list: dict[str: object] = copy(QuantumCore.graphic.light.lights_list)
        
        """ other """
        if QuantumCore.graphic.mash.mesh is not None:
            QuantumCore.graphic.mash.mesh.__destroy__()  # unset mesh
        
        self.builder = None  # builder thad load scene from file
        
        self.render_area = config.FAR*1.2
        self.time = {}
        self.progress_list = {}
        self.events_list = {}

    def obj(self, obj: BaseModel, abbr: str = None) -> str:
        if abbr is not None:
            if abbr in self.objects_list.keys():
                if config.SCENE_YSETB:
                    raise ValueError(f"Object with abbreviation '{abbr}' already exists")
                else:
                    abbr = f'{abbr}{self.increment}'
            self.objects_list[abbr] = obj
            return abbr
        self.objects_list[obj.metadata.ID] = obj
        return obj.metadata.ID
    
    def light(self, light, abbr: str = None) -> str:
        if abbr is not None:
            if abbr in self.objects_list.keys() and config.SCENE_YSETB:
                if config.SCENE_YSETB:
                    raise ValueError(f"Light with abbreviation '{abbr}' already exists")
                else:
                    abbr = f'{abbr}{self.increment}'
            self.lights_list[0][abbr] = light
            return abbr
        _id = uuid.uuid4()
        self.lights_list[0][_id] = light
        return _id

    @staticmethod
    def build() -> None:
        """ Write all the objects of the scene to this method """
        ...
    
    def unload(self) -> None:
        """ Unload scene """

        """ clear all graphic lists """
        QuantumCore.graphic.vbo.CustomVBO_name.clear()
        QuantumCore.graphic.texture.CustomTexture_name.clear()
        QuantumCore.widgets.Button.roster_relies()
        self.lights_list[0].clear()

    def load(self):
        """ Load game scene """

        QuantumCore.window.set_mesh()
        
        self.build()
        
        logger.debug('Scene load\n')
        return self
        
    def __update__(self) -> None:
        QuantumCore.graphic.camera.camera.update()
        
    def __render__(self) -> None:
        QuantumCore.window.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        [entity.__render__() for entity in self.objects_list.values()]
    
    
scene: Location = None
loading: int = True


class Builder:
    def __init__(self, target: str, *, scene_=None) -> None:
        """ Build in save.sav your scene """
        self.path: str = target
        self.scene: Location = scene_
        self.save: dict = None
        
        """ file info """
        self.root: str = lambda: os.path.dirname(self.path)
        self.name: str = lambda: os.path.basename(self.path)[:-4]
        self.exc: str = lambda: os.path.basename(self.path)[:-4]
        self.size: bin = lambda: os.path.getsize(self.path) if os.path.isfile(path=self.path) else None
    
    @staticmethod
    def _format_sav_(bld) -> dict:
        """ format save for load in file, or get satisfaction format """
        objects_data = {}
        for _, value in bld.scene.objects_list.items():
            objects_data[value.metadata.ID] = value.metadata
            
        return {
            'progress': bld.scene.progress_list,
            'time': QuantumCore.time.list_,
            'data': {
                'camera': QuantumCore.graphic.camera.camera.data,
                'scene': {
                    'objects': objects_data,
                    'lights': bld.scene.lights_list[0],
                    'time': bld.scene.time
                }
            },
            'events': bld.scene.events_list
        }
    
    def _dump(self, save) -> None:
        """ dump save in save.sav file """
        if self.scene is not None:
            with open(self.path, 'wb') as file:
                pickle.dump(save, file)
    
    def read(self) -> _format_sav_:
        """ load data from save.sav file """
        if os.path.isfile(path=self.path):
            with open(self.path, 'rb') as file:
                self.save = pickle.load(file)
                return self.save
        else:
            if config.SCENE_YSETB:
                raise FileNotFoundError(f'there is no save with the name {self.name()} in the directory {self.root()}')
    
    def write(self, name=None) -> None:
        """ write save before format method """
        if name is not None:
            self.path = self.root()+'/'+str(name)+'.sav'
        
        self._dump(self._format_sav_(self))
    
    def dell(self) -> bool:
        """ dell save.sav file """
        if os.path.isfile(path=self.path):
            os.remove(self.path)
            return True
        else:
            if config.SCENE_YSETB:
                raise FileNotFoundError(f'there is no save with the name {self.name()} in the directory {self.root()}')
            string = f'there is no save with the name {self.name()} in the directory {self.root()}'
            logger.warning(string)
            return False
    
    def load(self, objects_dictionary: dict[str: BaseModel] = None, *,
             light_code='', object_code='', camera_code='') -> bool:
        """ easy constructing your scene """
        assert self.scene is not None, ' `scene` reference is `None`'
        assert self.save is not None, " `save` variable should not be None"
        assert objects_dictionary is not None, "The `objects_dictionary` must be filled in"
        
        space = self.save['data']
        QuantumCore.time.list_ = self.save['time']

        for key, value in space['scene']['lights'].items():
            self.scene.lights_list[0][key] = value
            exec(light_code)
        
        # scene objects
        for key, value in space['scene']['objects'].items():
            obj_class = objects_dictionary[value.object_id]
            if issubclass(obj_class, BaseModel):
                self.scene.objects_list[key] = obj_class(metadata=value, sav=True)
            exec(object_code)
        
        if space['camera'] is not None:
            QuantumCore.graphic.camera.camera.data = space['camera']
        else:
            QuantumCore.graphic.camera.camera = QuantumCore.graphic.camera.Camera()
        exec(camera_code)
        
        return True
    