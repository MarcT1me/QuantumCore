
import QuantumCore.graphic

from QuantumCore.data import config
from GameData import settings

from core.elements.locations import TestScene
from core.elements.entities import Earth
from QuantumCore.graphic.light import Light

import moderngl
import pygame

texture = pygame.image.load(
    rf'{config.__APPLICATION_FOLDER__}/{settings.MODEL_path}/earth/Diffuse_2K.png'
)
clouds = pygame.image.load(
    rf'{config.__APPLICATION_FOLDER__}/{settings.MODEL_path}/earth/Textures/Clouds_2K.png'
)
clouds.set_colorkey((0, 0, 0))
clouds.set_alpha(75)
texture.blit(
    clouds, (0, 0)
)

texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)  # debug
# texture.fill((255, 0, 0))  # debug
texture = QuantumCore.graphic.context.texture(size=texture.get_size(), components=3,
                                              data=pygame.image.tostring(texture, 'RGBA'))  # get GLSL texture array
# use GLSL methods
texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
texture.build_mipmaps()
# AF
texture.anisotropy = 32.0


class MyScene(TestScene):
    def __init__(self, app) -> None:
        super().__init__(app)
    
    def build(self, app, add) -> None:
        QuantumCore.graphic.vbo.CustomVBO_name['earth'] = (
            '2f 3f 3f',
            ['in_texcoord_0', 'in_normal', 'in_position'],
            rf'{config.__APPLICATION_FOLDER__}/{settings.MODEL_path}/earth', 'obj', 'png'
        )
        QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh(shader_name=('automaton', 'unilight'))
        QuantumCore.graphic.mash.mesh.texture.textures['earth'] = texture
        QuantumCore.graphic.light.lights_list = [Light(), Light()]
        add(Earth(app, pos=(-10, 10, -10), scale=(2, 2, 2)))
        
        super().build(app, add)


QuantumCore.scene.scene.unload()
QuantumCore.scene.scene = MyScene(QuantumCore.scene.scene.app)
QuantumCore.scene.scene.load()
        