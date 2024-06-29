# other
from loguru import logger

from QuantumCore.data.config import __APPLICATION_PATH__
# engine elements import
from QuantumCore.scene import Location, Builder
import QuantumCore.graphic.light
from QuantumCore.graphic.light import Light
from QuantumCore.graphic.vbo import CustomVBO_name
from QuantumCore.graphic.texture import CustomTexture_name

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
            '2f 3f 3f', ['in_texcoord_0', 'in_normal', 'in_position'],
            f'{__APPLICATION_PATH__}/{settings.MODEL_path}/WoodenWatchTower', 'obj', 'jpg'
        )
        CustomVBO_name['Cat'] = (
            '2f 3f 3f', ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{settings.MODEL_path}/cat', 'obj', 'jpg'
        )
        CustomVBO_name['Earth'] = (
            '2f 3f 3f', ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{__APPLICATION_PATH__}/{settings.MODEL_path}/earth', 'obj', 'png'
        )
        CustomTexture_name['alpha'] = f'{__APPLICATION_PATH__}\\core\\textures\\image.png'
        self.app.loading.itrf.step(45, status='Game Canvas')
        return self
    
    def build(self) -> None:
        if self.builder.read() is not None and False:
            """ if scene.sav load successful """
            
            self.builder.load(
                {
                    'Earth':            Earth,
                    'Cat':              Cat,
                    'Cube':             Cube,
                    'MovingCube':       MovingCube,
                    'WoodenWatchTower': WoodenWatchTower
                },
                light_code="""
self.scene.app.loading.itrf.step(45, stage='Load game scene', status='sav - lighting')
            """,
                object_code="""
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
            self.light(Light(pos=(25, 25, 25), ambient=.2, diffuse=1.5, specular=.5))  # default light
            self.light(Light(size=15), 'lighter')  # camera light

            self.obj(Cube(pos=(40, 0, 40), scale=(40, 1, 40), tex_id='wall1'))  # wall
            self.obj(MovingCube(pos=(15, 10, 15), scale=(5, 10**-10, 5), tex_id='test1'))  # moving cube 1
            self.obj(WoodenWatchTower(pos=(60, -1, 30), scale=(3, 3, 3)))  # tower - custom model
            self.obj(Earth(pos=(30, 10, 60), scale=(2, 2, 2)))  # earth - custom model with no-event updating
            self.obj(MovingCube(pos=(44, 10, 44), scale=(5, 5, 5), tex_id='empty'))  # moving cube 2
            self.obj(Cat(pos=(7.0, 0.0, 44.0), rot=(0, 0, 125)))  # cat - custom model with handling events
            self.obj(Cube(pos=(30, 5, 30), tex_id='alpha'))  # alpha texture
            
            QuantumCore.graphic.camera.camera.data = QuantumCore.graphic.camera.Camera.Snap(
                pos=(-7, 7, -7), yaw=45, pitch=-15
            )
            
            self.builder.write()  # saving in file
            
            logger.warning('TestScene - build\n\n')
    
    def __update__(self) -> None:
        super().__update__()
        
        self.lights_list[0]['lighter'].position = QuantumCore.graphic.camera.camera.data.pos  # change camera light pos
