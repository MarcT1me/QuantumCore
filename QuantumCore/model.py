""" Engine standard model class.
That your code work correct inheritance on ExtendedBaseModel
 """

from copy import copy
import glm  # math
from dataclasses import dataclass, field
from uuid import uuid4

import QuantumCore.graphic
# engine config import
from QuantumCore.data.config import FAR, GAMMA


@dataclass
class MetaData:
    """ model data """
    pos: tuple[float, float, float] | glm.vec3
    rot: tuple[float, float, float] | glm.vec3
    scale: tuple[float, float, float] | glm.vec3
    
    object_id: str
    vao_id: str
    tex_id: str
    
    time_list: dict = field(init=True, default_factory=dict)
    ID: str = field(init=True, default_factory=uuid4)  # unique object id
    
    def __post_init__(self):
        self.pos = glm.vec3(self.pos)
        self.rot = glm.vec3([glm.radians(cord) for cord in self.rot])
        self.scale = glm.vec3(self.scale)


class BaseModel:
    # vectors, used in update, that calculate
    _vec_x = glm.vec3(1, 0, 0)
    _vec_y = glm.vec3(0, 1, 0)
    _vec_z = glm.vec3(0, 0, 1)
    
    def __init__(self, metadata: MetaData, *, render_area: int = FAR, sav=None) -> None:
        self.metadata = metadata
        
        self.m_model: glm.mat4 = self.__get_model_matrix__()
        self.camera = QuantumCore.graphic.camera.camera
        self.vao = QuantumCore.graphic.mash.mesh.vao.VAOs[metadata.vao_id]
        self.shader_program = self.vao.program
        
        self.texture = None
        self.render_area: int = render_area
    
    def __get_model_matrix__(self) -> glm.mat4:
        """ set and change model_matrix """
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.metadata.pos)
        # rotate
        m_model = glm.rotate(m_model, self.metadata.rot.x, self._vec_x)
        m_model = glm.rotate(m_model, self.metadata.rot.y, self._vec_y)
        m_model = glm.rotate(m_model, self.metadata.rot.z, self._vec_z)
        # scale
        m_model = glm.scale(m_model, self.metadata.scale)
        return m_model
    
    def update(self) -> None:
        self.m_model = self.__get_model_matrix__()
    
    def light_update(self) -> None: self.update()
    
    def __render__(self) -> None:
        """ render model """
        self.update() if self.can_render() else self.light_update()
        self.vao.render() if self.can_render() else None
    
    def can_render(self, *, render_area=None) -> bool:
        """ the method that decides which rendering method to use """
        render_area = self.render_area if render_area is None else render_area
        
        if all(
                (abs(self.metadata.pos[0] - self.camera.data.pos[0]) <= render_area*1.2,
                 abs(self.metadata.pos[1] - self.camera.data.pos[1]) <= render_area*1.2,
                 abs(self.metadata.pos[2] - self.camera.data.pos[2]) <= render_area*1.2)
        ):
            return True
        return False
    
    @classmethod
    def name(cls) -> str: return cls.__name__
    
    @staticmethod
    def combine_vector(vec1: tuple, vec2: tuple, *, sav: bool) -> glm.vec3:
        return glm.vec3(glm.vec3(vec1) + glm.vec3(vec2)) if not sav else vec1


class ExtendedBaseModel(BaseModel):
    """ Class - the basis for creating your own models.

      to use:
        1) inherit to this class
        2) use super in init and rewrite methods"""
    
    def __init__(self, metadata: MetaData, *, render_area: int = FAR, sav=None):
        """ init your model.

to do so:

class ModelName(ExtendedBaseModel):
    def __init__(self, app, vao_name='ModelName', tex_id='ModelName', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):

        super().__init__(app, vao_name, tex_id, pos, rot, scale)

* feel free to use combine_vector

ATTENTION!!! ModelName to be match in all place ATTENTION!!!"""
        
        # inheritance
        super().__init__(metadata, render_area=render_area)
        
        self.lights = copy(QuantumCore.graphic.light.lights_list)
        
        self.glas = lambda: min(len(self.lights[0]), 200)
        self._on_init_()
    
    # in development
    """def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        # resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)
        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)"""
    
    def _on_init_(self) -> None:
        """ init model """
        
        # light
        arr_size: int = self.glas()
        self.shader_program['lights_source_size'] = arr_size
        i = 0
        for light in self.lights[0].values():
            if i >= arr_size:
                break
            self.shader_program[f'lights_source[{i}].position'].write(light.position)
            self.shader_program[f'lights_source[{i}].Ia'].write(light.Ia)
            self.shader_program[f'lights_source[{i}].Id'].write(light.Id)
            self.shader_program[f'lights_source[{i}].Is'].write(light.Is)
            self.shader_program[f'lights_source[{i}].size'] = light.size
            i += 1
        
        # gamma
        self.shader_program['gamma'] = GAMMA
        
        # texture
        self.texture = QuantumCore.graphic.mash.mesh.texture.textures[self.metadata.tex_id]
        self.shader_program['u_texture_0'] = 0
        self.texture.use(0)
        
        # mvp
        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
    
    def update(self) -> None:
        super().update()
        # light
        self.__update_light__() if self.can_render(render_area=self.render_area/3) else None
        # texture
        self.texture.use(0)
        
        # rewrite GLSL variable
        self.shader_program['camPos'].write(self.camera.data.pos)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
    
    def __update_light__(self) -> None:
        """ update light position """
        i = 0
        for light in self.lights[0].values():
            self.shader_program[f'lights_source[{i}].position'].write(light.position)
            i += 1
    
    # in development
    """def update_shadow(self) -> None:
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self) -> None:
        self.update_shadow()
        self.shadow_vao.render()"""


class Cube(ExtendedBaseModel):
    def __init__(self, metadata: MetaData = None, *,
                 tex_id='empty', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=None
                 ):
        super().__init__(
            metadata if metadata is not None else MetaData(
                pos=pos,
                rot=rot,
                scale=scale,
                object_id=self.name(),
                vao_id='Cube',
                tex_id=tex_id
            ),
            render_area=render_area,
            sav=sav
        )


"""
 In development
"""


class SkyBox(BaseModel):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(
            MetaData(
                pos=pos, rot=rot, scale=scale,
                object_id=self.name(), vao_id='skybox', tex_id='skybox'
            )
        )
        self.on_init()
    
    def update(self):
        self.shader_program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))
    
    def on_init(self):
        # texture
        self.texture = QuantumCore.graphic.mash.mesh.texture.textures[self.metadata.tex_id]
        self.shader_program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(
            MetaData(
                pos=pos, rot=rot, scale=scale,
                object_id=self.name(), vao_id='advanced_skybox', tex_id='skybox'
            )
        )
        self.on_init()
    
    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.shader_program['m_invProjView'].write(glm.inverse(self.camera.m_proj*m_view))
    
    def on_init(self):
        # texture
        self.texture = QuantumCore.graphic.mash.mesh.texture.textures[self.metadata.tex_id]
        self.shader_program['u_texture_skybox'] = 11
        self.texture.use(location=11)
