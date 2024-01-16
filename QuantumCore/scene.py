import uuid
# other
import pickle
import os.path
from loguru import logger

import QuantumCore.graphic
from QuantumCore.model import QCModel
# engine elements imports
from QuantumCore.data import config


class QCScene:
    def __init__(self, *, locations=None, app=None):
        """ Game scene  """
        self.app = app
        self.locations: dict[QCLocation] = {} if locations is None else locations
        
        """ other """
        if QuantumCore.window.mash is not None:
            QuantumCore.window.mash.__destroy__()  # unset mesh
            
        self.time = {}
        self.progress_list = {}
        self.events_list = {}
    
    @staticmethod
    def unload() -> None:
        """ Unload scene """
        
        """ clear all graphic lists """
        QuantumCore.graphic.vbo.CustomVBO_name.clear()
        QuantumCore.graphic.texture.CustomTexture_name.clear()
        QuantumCore.widgets.Button.roster_relies()
    
    def set(self):
        """ Load game scene """
        
        QuantumCore.window.set_mesh()
        
        for location in self.locations.values():
            QuantumCore.model.ExtendedQCModel.process_location = location
            location.build()
        
        logger.debug('Scene load\n')
        return self
    
    def __update__(self):
        [location.__update__() for location in self.locations.values()]
            
    def __render__(self):
        QuantumCore.window.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        [location.__render__() for location in self.locations.values()]


class QCLocation:
    increment = 1
    
    def __init__(self) -> None:
        """ Base location """
        
        """ scene space """
        self.objects_list: dict[QCModel] = dict()
        self.lights_list = QuantumCore.graphic.light.LightArray()  # type: QuantumCore.graphic.light.LightArray
        print(self.lights_list)
        
        self.builder = None  # builder thad load scene from file
        self.render_area = config.FAR * 1.2
    
    def obj(self, obj: QCModel, abbr: str = None) -> str:
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
            if abbr in self.objects_list.keys():
                if config.SCENE_YSETB:
                    raise ValueError(f"Light with abbreviation '{abbr}' already exists")
                else:
                    abbr = f'{abbr}{self.increment}'
            self.lights_list[abbr] = light
            return abbr
        _id = uuid.uuid4()
        self.lights_list[_id] = light
        return _id
    
    @staticmethod
    def build() -> None:
        """ Write all the objects of the scene to this method """
        ...
    
    def __update__(self) -> None:
        QuantumCore.window.camera.update()
    
    def __render__(self) -> None:
        [entity.__render__() for entity in self.objects_list.values()]


class Builder:
    def __init__(self, target: str, *, scene_=None) -> None:
        """ Build in save.sav your scene """
        self.path: str = target
        self.location: QCLocation = scene_
        self.save: dict = None
        
        """ file info """
        self.root: str = os.path.dirname(self.path)
        self.name: str = os.path.basename(self.path)[:-4]
    
    @staticmethod
    def _format_sav_(bld) -> dict:
        """ format save for load in file, or get satisfaction format """
        
        return {
            'progress': bld.scene.progress_list,
            'time':     QuantumCore.time.list_,
            'data':     {
                'camera': QuantumCore.window.camera.data,
                'scene':  {
                    'objects': bld.location.objects_list,
                    'lights':  bld.scene.lights_list,
                    'time':    bld.scene.time
                }
            },
            'events':   bld.scene.events_list
        }
    
    def _dump(self, save) -> None:
        """ dump save in save.sav file """
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
                raise FileNotFoundError(f'there is no save with the name {self.name} in the directory {self.root}')
    
    def write(self, name=None) -> None:
        """ write save before format method """
        if name is not None:
            self.path = self.root+'/'+str(name)+'.sav'
        
        self._dump(self._format_sav_(self))
    
    def dell(self) -> bool:
        """ dell save.sav file """
        if os.path.isfile(path=self.path):
            os.remove(self.path)
            return True
        else:
            if config.SCENE_YSETB:
                raise FileNotFoundError(f'there is no save with the name {self.name} in the directory {self.root}')
            string = f'there is no save with the name {self.name} in the directory {self.root}'
            logger.warning(string)
            return False
    
    def load(self, objects_dictionary: dict[str: QCModel] = None, *,
             light_code='', object_code='', camera_code=''
             ) -> bool:
        """ easy constructing your scene """
        assert self.location is not None, ' `scene` reference is `None`'
        assert self.save is not None, " `save` variable should not be None"
        assert objects_dictionary is not None, "The `objects_dictionary` must be filled in"
        
        space = self.save['data']
        QuantumCore.time.list_ = self.save['time']
        
        for key, value in space['scene']['lights'].items():
            self.location.lights_list[key] = value
            exec(light_code)
        
        # scene objects
        for key, value in space['scene']['objects'].items():
            obj_class = objects_dictionary[value.object_id]
            if issubclass(obj_class, QCModel):
                self.location.objects_list[key] = obj_class(metadata=value, sav=True)
            exec(object_code)
        
        if space['camera'] is not None:
            QuantumCore.window.camera.data = space['camera']
        else:
            QuantumCore.graphic.camera.camera = QuantumCore.graphic.camera.Camera()
        exec(camera_code)
        
        return True
