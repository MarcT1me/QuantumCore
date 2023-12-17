# other
from copy import copy
import pickle
import os.path
import glm

import QuantumCore.graphic
# engine elements imports
from QuantumCore.data import config


class Location:
    def __init__(self, app) -> None:
        """ Base location """
        self.app = app
        
        self.objects_list: dict[hash: object] = dict()
        self.lights_list: dict[hash: object] = copy(QuantumCore.graphic.light.lights_list)
        
        self.unload()
        if QuantumCore.graphic.mash.mesh is not None:
            QuantumCore.graphic.mash.mesh.__destroy__()
        
        self.render_area = config.FAR*1.2
        
        self.builder = None
        self.ids: dict[str: hash] = dict()
        
        self.time = 0

    def add_vbos(self): ...
    
    def on_init(self):
        self.add_vbos()
        return self

    def _add_object(self, obj) -> int:
        """ add object in list """
        __id = id(obj)
        self.objects_list[__id] = obj
        return __id
    
    def _add_light(self, light) -> int:
        __id = id(light)
        self.lights_list[0][__id] = light
        return __id

    @staticmethod
    def build(app, obj, light) -> None:
        """ Write all the objects of the scene to this method """
        ...
    
    def unload(self) -> None:
        """ Unload scene """

        """ work with scene itself """
        self.objects_list.clear()
        """ clear all graphic lists """
        QuantumCore.graphic.vbo.CustomVBO_name.clear()
        QuantumCore.graphic.texture.CustomTexture_name.clear()
        self.lights_list[0].clear()

    def load(self):
        """ Load game scene """
        app = self.app
        
        add_obj = self._add_object
        add_light = self._add_light

        QuantumCore.window.set_mesh()
        self.build(app, add_obj, add_light)
        return self
        
    def __update__(self) -> None:
        QuantumCore.graphic.camera.camera.update()
        
    def __render__(self) -> None:
        QuantumCore.window.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        [entity.__render__() for entity in self.objects_list.values()]
    
    
scene: Location = None
loading = None


class Builder:
    
    def __init__(self, target: str, *, scene_=None) -> None:
        """ Build in save.sav your scene """
        self.path: str = target
        self.scene: Location = scene_
        
        """ file info """
        self.root: str = lambda: os.path.dirname(self.path)
        self.name: str = lambda: os.path.basename(self.path)[:-4]
        self.size: bin = lambda: os.path.getsize(self.path) if os.path.isfile(path=self.path) else None
        
        """ builder variable """
        self.save = self._format_sav_(self)
        self.new_id = None  # from changing id
    
    @staticmethod
    def _format_sav_(sav) -> dict[str: Location]:
        """ format save for load in file, or get satisfaction format """
        root: str = sav.root()
        name: str = sav.name()
        objects_data = [{'id': id_,
                         'name': obj.name(),
                         'pos': tuple(obj.pos),
                         'rot': [glm.degrees(cord) for cord in obj.rot],
                         'r_area': obj.render_area,
                         'scale': tuple(obj.scale),
                         'tex_id': obj.tex_id,
                         'vao': obj.vao_name}
                        for id_, obj in sav.scene.objects_list.items()]
        light_data = [{'id': id_,
                       'color': tuple(light.color),
                       'pos': tuple(light.position),
                       'Ia': tuple(light.Ia),
                       'Id': tuple(light.Id),
                       'Is': tuple(light.Is),
                       'size': light.size}
                      for id_, light in sav.scene.lights_list[0].items()]
        camera = QuantumCore.graphic.camera.camera
        camera_data = None
        if camera is not None:
            camera_data = {
                'pos': tuple(camera.position),
                'yaw': camera.yaw,
                'pitch': camera.pitch,
                'speed': camera.speed
            }
        return {
            'file': {
                'root': root,
                'name': name,
            },
            'time': QuantumCore.time.list_,
            'scene': {
                'objects': objects_data,
                'lights': light_data,
                'ids': sav.scene.ids,
                'camera': camera_data
            }
        }
    
    def _dump_(self, save) -> None:
        """ dump save in fail.sav """
        if self.scene is not None:
            with open(self.path, 'wb') as file:
                pickle.dump(save, file)
    
    def load(self) -> dict[str: Location]:
        """ load save.sav """
        if os.path.isfile(path=self.path):
            with open(self.path, 'rb') as file:
                print(self.path)
                self.save = pickle.load(file)
                return self.save
        else:
            print('not found file')
    
    def write(self, name=None) -> None:
        """ write save before format method """
        if name is not None:
            self.path = self.root()+'/'+str(name)+'.sav'
        
        self._dump_(self._format_sav_(self))
    
    def dell(self) -> bool:
        """ dell file.sav """
        if os.path.isfile(path=self.path):
            os.remove(self.path)
            return True
        else:
            print('not found file')
            return False
    
    def read(self, scene_, import_code_,
             light_iteration_code='', object_iteration_code='', camera_body_code='',
             **kwargs) -> bool:
        """ easy constructing your scene """
        if self.scene is None:
            print('I can`t read save')
            return False
        
        exec(import_code_)
        
        sav = self.save['scene']
        scene_.ids = sav['ids']
        QuantumCore.time.list_ = self.save['time']
        
        def change_id() -> None:
            for key, old_id in scene_.ids.items():
                if old_id == i['id']:
                    scene_.ids[key] = self.new_id
                    break
        
        # lights sources
        for i in sav['lights']:
            exec(f"""
self.new_id = scene_._add_light(
    Light(
        color={i['color']},
        pos={i['pos']},
        ambient={i['Ia']},
        diffuse={i['Id']},
        specular={i['Is']},
        size={i['size']}
    )
)"""); change_id()  # light sources initialisation
            exec(light_iteration_code)
        
        # scene objects
        for i in sav['objects']:
            exec(f"""
self.new_id = scene_._add_object(
    {kwargs[i['name']] if len(kwargs) is not 0 else i['name']}(
        scene_.app,
        pos={i['pos']},
        rot={i['rot']},
        render_area={i['r_area']},
        scale={i['scale']},
        tex_id="{i['tex_id']}",
        vao_name="{i['vao']}",
        sav=True
    )
)"""); change_id()  # objects initialisation
            exec(object_iteration_code)
        
        if sav['camera'] is not None:
            QuantumCore.graphic.camera.camera.position = glm.vec3(sav['camera']['pos'])
            QuantumCore.graphic.camera.camera.yaw = sav['camera']['yaw']
            QuantumCore.graphic.camera.camera.pitch = sav['camera']['pitch']
            QuantumCore.graphic.camera.camera.speed = sav['camera']['speed']
            exec(camera_body_code)
        
        return True
    