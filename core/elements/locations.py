
# other
from loguru import logger

from QuantumCore.data.config import __APPLICATION_FOLDER__
# engine elements import
from QuantumCore.scene import Location, Builder
import QuantumCore.graphic.light
from QuantumCore.graphic.light import Light

from GameData.settings import SAVES_path
from core.elements.entities import Cat, Cube, MovingCube, WoodenWatchTower, Earth
# core elements


class TestScene(Location):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.builder = Builder(rf'{__APPLICATION_FOLDER__}/{SAVES_path}/data.sav', scene_=self)

    def build(self, app, obj, light) -> None:

        self.lights_list[0].clear()
        load_scene = self.builder.load()
        
        if load_scene is not None:
            """ if scene.sav load successful """
            
            self.builder.read(
                self, "from core.elements.entities import Cat, Cube, MovingCube, WoodenWatchTower, Earth; "
                      "from QuantumCore.graphic.light import Light"
            )  # use builder, that easy constructing scene
                        
            logger.debug('TestScene - construct .sav\n\n')

        else:
            """ in other a build scene in code """
            light(Light(pos=(25, 25, 25), ambient=.2, diffuse=1.5, specular=.5))
            self.ids['фонарик'] = light(Light(size=15))
            
            for x in range(40):
                for z in range(40):
                    obj(Cube(app, pos=(x*2, 0, z*2), tex_id='wall1'))

            obj(MovingCube(app, pos=(15, 10, 15), tex_id='test1', scale=(5, 5, 5)))
            obj(WoodenWatchTower(app, scale=[3, 3, 3], pos=[60, 0, 30]))
            obj(Earth(app, scale=[2, 2, 2], pos=[30, 10, 60]))
            obj(Cat(app, pos=(7, 0, 44), rot=(0, 0, 125)))
            obj(MovingCube(app, pos=(44, 10, 44), tex_id='empty', scale=(5, 5, 5)))
            
            logger.debug('TestScene - build\n\n')
            
            self.builder.write()
    
    def __update__(self):
        super().__update__()
        
        if len(self.lights_list[0]) >= 2:
            self.lights_list[0][self.ids['фонарик']].position = QuantumCore.graphic.camera.camera.position
        