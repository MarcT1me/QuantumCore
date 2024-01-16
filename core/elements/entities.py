# graphic
import pygame

# math
import glm
import numpy as np

# engine elements imports
from QuantumCore.data.config import FAR
from QuantumCore.model import ExtendedQCModel, Cube, MetaData
import QuantumCore.time


class MovingCube(Cube):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def update(self) -> None:

        m_model = glm.rotate(self._get_model_matrix_(),
                             np.sin(QuantumCore.time.list_['cube animation'] * 0.5), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model,
                             np.cos(QuantumCore.time.list_['cube animation'] * 0.5), glm.vec3(0, -1, 0))
        self._m_model_ = glm.rotate(m_model,
                                  np.sin(QuantumCore.time.list_['cube animation'] * 0.5), glm.vec3(0, 0, 1))

        super().update()

    def light_update(self) -> None: super().update()


class Cat(ExtendedQCModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='Cat', tex_id='Cat',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:
        
        super().__init__(metadata if metadata is not None else\
                             MetaData(
                                 pos=self.combine_vector(pos, (0, 1, 0), sav=sav),
                                  rot=self.combine_vector(rot, (-90, 0, 0), sav=sav),
                                  scale=scale,
                                  object_id=self.name(),
                                  vao_id=vao_id,
                                  tex_id=tex_id
                             ),
                         render_area=render_area)
        
        self.speed: float = .05

    def update(self) -> None:

        velocity = self.speed * QuantumCore.time.delta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP8]:
            self.metadata.pos += velocity * self._vec_x
        if keys[pygame.K_KP5]:
            self.metadata.pos -= velocity * self._vec_x
        if keys[pygame.K_KP6]:
            self.metadata.pos += velocity * self._vec_z
        if keys[pygame.K_KP_4]:
            self.metadata.pos -= velocity * self._vec_z
        if keys[pygame.K_KP_PLUS]:
            self.metadata.pos += velocity * self._vec_y
        if keys[pygame.K_KP_MINUS]:
            self.metadata.pos -= velocity * self._vec_y

        velocity /= 5
        if keys[pygame.K_KP7]:
            self.metadata.rot -= velocity * self._vec_z
        if keys[pygame.K_KP9]:
            self.metadata.rot += velocity * self._vec_z

        if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01

        self._m_model_ = self._get_model_matrix_()
        super().update()

    def light_update(self) -> None: super().update()


class WoodenWatchTower(ExtendedQCModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='WoodenWatchTower', tex_id='WoodenWatchTower',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:
        
        super().__init__(metadata if metadata is not None else\
                             MetaData(
                                 pos=self.combine_vector(pos, (0, -1, 0), sav=sav),
                                  rot=rot,
                                  scale=scale,
                                  object_id=self.name(),
                                  vao_id=vao_id,
                                  tex_id=tex_id
                             ),
                         render_area=render_area)


class Earth(ExtendedQCModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='Earth', tex_id='Earth',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:
        
        super().__init__(metadata if metadata is not None else\
                             MetaData(
                                 pos=pos,
                                  rot=rot,
                                  scale=scale,
                                  object_id=self.name(),
                                  vao_id=vao_id,
                                  tex_id=tex_id
                             ),
                         render_area=render_area)

    def update(self) -> None:

        self._m_model_ = glm.rotate(self._get_model_matrix_(),
                                  QuantumCore.time.list_['earth animation'] * 0.5, glm.vec3(0, 1, 0))
        
        super().update()

    def light_update(self) -> None: super().update()
