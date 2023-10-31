
import QuantumCore.graphic

from QuantumCore.data import config
from GameData import settings

from core.elements.entities import Earth

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
texture = QuantumCore.graphic.context.texture(size=texture.get_size(), components=4,
                                              data=pygame.image.tostring(texture, 'RGBA'))  # get GLSL texture array
# use GLSL methods
texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
texture.build_mipmaps()
# AF
texture.anisotropy = 32.0

QuantumCore.graphic.mash.mesh = QuantumCore.graphic.mash.Mesh(shader_name=('automaton', 'unilight'))
QuantumCore.graphic.mash.mesh.texture.textures['Earth'] = texture
QuantumCore.scene.scene.objects_list[1] = Earth(QuantumCore.scene.scene.app, pos=(-10, 10, -10), scale=(2, 2, 2))
        