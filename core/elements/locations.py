
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
from GameData.settings import SAVES_path, MODEL_path
from core.elements.entities import Cat, Cube, MovingCube, WoodenWatchTower, Earth


class TestScene(Location):
    def __init__(self, app) -> None:
        super().__init__(app)
        app.loading.itrf.step(15, stage='Init game Scene', status='builder')
<<<<<<< HEAD
        self.builder = Builder(rf'{__APPLICATION_PATH__}/{SAVES_path}/Abobacraft.sav', scene_=self)
=======
        self.builder = Builder(rf'{__APPLICATION_PATH__}/{settings.SAVES_path}/{settings.save_name}.sav', scene_=self)
        print(self.builder.path)
>>>>>>> 60d7484 (0.5.2:r2)

    def add_vbos(self):
        self.app.loading.itrf.step(16, status='models path')
        CustomVBO_name['WoodenWatchTower'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            f'{__APPLICATION_PATH__}/{MODEL_path}/WoodenWatchTower', 'obj', 'jpg')
        CustomVBO_name['Cat'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{MODEL_path}/cat', 'obj', 'jpg')
        CustomVBO_name['Earth'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{MODEL_path}/earth', 'obj', 'png')
        self.app.loading.itrf.step(45, status='Game Canvas')
        return self

    def build(self, app, obj, light) -> None:
        
        if self.builder.load() is not None:
            """ if scene.sav load successful """
            
            self.builder.read(
                self, "from core.elements.entities import Cat, Cube, MovingCube, WoodenWatchTower, Earth; "
                      "from QuantumCore.graphic.light import Light",
                light_iteration_code="""
p = 65 + (87-66) * sav['lights'].index(i) / (len(sav['lights']) - 1)
scene_.app.loading.itrf.step(p, stage='Load game scene', status='sav - lighting')
""",
                object_iteration_code="""
p = 87 + (96-87) * sav['objects'].index(i) / (len(sav['objects']) - 1)
scene_.app.loading.itrf.step(p, stage='Load game scene', status='sav - objects')
""",
                camera_body_code="""
scene_.app.loading.itrf.step(97, stage='Load game scene', status='sav - camera')
"""
            )  # use builder, that easy constructing scene
                        
            logger.success('TestScene - construct .sav\n\n')
        else:
            self.app.loading.itrf.step(65, stage='Load game scene', status='Scene - build')
            
            """ in other a build scene in code """
            light(Light(pos=(25, 25, 25), ambient=.2, diffuse=1.5, specular=.5))
            self.ids['фонарик'] = light(Light(size=15))
            
            # for x in range(40):
            #     for z in range(40):
            obj(Cube(app, pos=(40, 0, 40), scale=(40, 1, 40), tex_id='wall1'))

            obj(MovingCube(app, pos=(15, 10, 15), tex_id='test1', scale=(5, 5, 5)))
            obj(WoodenWatchTower(app, scale=[3, 3, 3], pos=[60, 0, 30]))
            obj(Earth(app, scale=[2, 2, 2], pos=[30, 10, 60]))
            self.ids['котик'] = obj(Cat(app, pos=(7, 0, 44), rot=(0, 0, 125)))
            obj(MovingCube(app, pos=(44, 10, 44), tex_id='empty', scale=(5, 5, 5)))
            
            QuantumCore.graphic.camera.camera.position = glm.vec3((-7, 7, -7))
            QuantumCore.graphic.camera.camera.yaw = 45
            QuantumCore.graphic.camera.camera.pitch = -15
            QuantumCore.graphic.camera.camera.speed = 0.01
            
            logger.warning('TestScene - build\n\n')
    
    def __update__(self) -> None:
        super().__update__()
        
        self.lights_list[0][self.ids['фонарик']].position = QuantumCore.graphic.camera.camera.position
        