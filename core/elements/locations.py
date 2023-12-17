
# other
from loguru import logger
import glm

from QuantumCore.data.config import __APPLICATION_PATH__
# engine elements import
from QuantumCore.scene import Location, Builder
import QuantumCore.graphic.light
from QuantumCore.graphic.light import Light
from QuantumCore.graphic.vbo import CustomVBO_name

# core elements
from GameData import settings
from core.elements.entities import Cat, Cube, MovingCube, WoodenWatchTower, Earth


class TestScene(Location):
    def __init__(self, app) -> None:
        super().__init__(app)
        app.loading.itrf.step(15, stage='Init game Scene', status='builder')
        self.builder = Builder(rf'{__APPLICATION_PATH__}/{settings.SAVES_path}/{settings.save_name}.sav', scene_=self)

    def on_init(self):
        self.app.loading.itrf.step(16, status='models path')
        CustomVBO_name['WoodenWatchTower'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            f'{__APPLICATION_PATH__}/{settings.MODEL_path}/WoodenWatchTower', 'obj', 'jpg')
        CustomVBO_name['Cat'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{settings.MODEL_path}/cat', 'obj', 'jpg')
        CustomVBO_name['Earth'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{settings.MODEL_path}/earth', 'obj', 'png')
        self.app.loading.itrf.step(45, status='Game Canvas')
        return self

    def build(self, app, obj, light) -> None:
        
        if self.builder.read() is not None:
            """ if scene.sav load successful """

            self.builder.load(
                {
                    'Earth': Earth,
                    'Cat': Cat,
                    'Cube':Cube,
                    'MovingCube': MovingCube,
                    'WoodenWatchTower': WoodenWatchTower
                },
                light_code="""
self.scene.app.loading.itrf.step(45, stage='Load game scene', status='sav - lighting')
            """,
                object_iter_code="""
lp = 0
if lp:
    self.scene.app.loading.itrf.step(67, stage='Load game scene', status='sav - objects')
    lp = 1
            """,
                camera_code="""
self.scene.app.loading.itrf.step(93, stage='Load game scene', status='sav - camera')
            """
            )  # use builder, that easy constructing scene
                        
            logger.success('TestScene - construct .sav\n\n')
        else:
            self.app.loading.itrf.step(65, stage='Load game scene', status='Scene - build')
            
            """ in other a build scene in code """
            light(Light(pos=(25, 25, 25), ambient=.2, diffuse=1.5, specular=.5))
            light(Light(size=15))
            
            for x in range(-5, 5):
                for y in range(-5, 5):
                    for z in range(-5, 5):
                        obj(Earth(pos=(10*x, 10*y, 10*z)))
            
            QuantumCore.graphic.camera.camera.data.position = glm.vec3((-7, 7, -7))
            QuantumCore.graphic.camera.camera.data.yaw = 45
            QuantumCore.graphic.camera.camera.data.pitch = -15
            QuantumCore.graphic.camera.camera.data.speed = 0.01
            
            # self.builder.write()
            
            logger.warning('TestScene - build\n\n')
    
    def __update__(self) -> None:
        super().__update__()
        
        # self.lights_list[0][self.ids['фонарик']].position = QuantumCore.graphic.camera.camera.position
        