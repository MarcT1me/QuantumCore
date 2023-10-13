
import QuantumCore.graphic
# engine elements imports
from QuantumCore.data import config


# NOT WORK  in development
"""class Builder:
    def __init__(self, target: str) -> None:
        self.path: str = target
        self.root: ETree.Element = None
        self.import_list: list = None
        
        with open(self.path, 'r') as file:
            xml_data = file.read()
        self.root = ETree.fromstringlist(xml_data)
    
    def read_tpt(self):
        # read TPT teg - load. imports/data/camera
        tpt_tag = self.root.find('TPT')  # Top PrioriTy core load (<!-- sav requirements -->)
        
        include: ETree.Element = tpt_tag.find('Include')
        if include is not None:
            
            # sav IMPORTS
            imports = include.find('Imports')
            if imports is not None:
                
                for element in imports:
                    exec(f"{element.text}")
                    
            list_ = include.find("list")
            self.import_list = [] if list_ is None else list_
            
            # sav CUSTOM data loading
            loads = include.find('Loads')
            if loads is not None:
                
                vbos = loads.find('vbos')
                if vbos is not None:
                    for element in vbos:
                        exec(f"QuantumCore.graphic.vbo.{element.text}")  # vbo`s
                
                textures = loads.find('textures')
                if textures is not None:
                    for element in textures:
                        exec(f"QuantumCore.graphic.texture.{element.text}")  # texture`s
            
        # sav CAMERA
        camera: ETree.Element = tpt_tag.find('Camera')
        if camera is not None:
            for element in camera:
                exec(f"QuantumCore.graphic.camera.camera.{element.tag} = {element.text}")
    
    def read_sav(self, app, add):
        # init Map
        save = self.root.find('Save')
        
        objects = save.find('Objects')
        for object in objects.iter():
            exec(object.text)
            
        objects = save.find('Lights')
        for light in objects.iter():
            exec(f"QuantumCore.graphic.light.lights_list.append({light.text})")
        
        code = save.find('code')
        for element in code:
            exec(element.text)
    
    def read_custom_tags(self, app, add, use_tags: tuple = None):
        # Read custom tags. Use_tag arg, that loader know, why load you save
        for tag in use_tags:
            element_tag = tag.find(tag)
            self.use_tag(element_tag, app=app, add=add)
    
    @staticmethod
    def use_tag(tag, *, first_text='', second_text='', app=None, add=None):
        if tag is not None:
            for element in tag:
                exec(f"{first_text}{element.text}{second_text"")
    
    def unimport(self) -> None:
        for include in self.import_list:
            exec(f"del {include}")"""


class Location:
    def __init__(self, app) -> None:
        """ Base location """
        self.app = app
        self.objects_list = dict()
        self.render_area = config.FAR*1.2
        self.builder = None

    def __add_object__(self, id: str, obj) -> None:
        """ add object in list """
        self.objects_list[id] = obj

    @staticmethod
    def build(app, add) -> None:
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
        add = self.__add_object__

        self.build(app, add)
        
    def __render__(self) -> None:
        QuantumCore.graphic.context.clear(color=(0.08, 0.16, 0.18, 1.0))
        [entity.__render__() for entity in self.objects_list]
    
    
scene: Location = None
