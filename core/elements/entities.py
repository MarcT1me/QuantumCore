# graphic
import pygame

# math
import glm
import numpy as np

# engine elements imports
from QuantumCore.data.config import FAR
from QuantumCore.model import ExtendedBaseModel, Cube
import QuantumCore.time


class MovingCube(Cube):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def update(self) -> None:

        m_model = glm.rotate(self.__get_model_matrix__(),
                             np.sin(self.app.time_list['cube animation'] * 0.5), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model,
                             np.cos(self.app.time_list['cube animation'] * 0.5), glm.vec3(0, -1, 0))
        self.m_model = glm.rotate(m_model,
                                  np.sin(self.app.time_list['cube animation'] * 0.5), glm.vec3(0, 0, 1))

        super().update()

    def light_update(self) -> None: super().update()


class Cat(ExtendedBaseModel):
    def __init__(self, app, vao_name='Cat', tex_id='Cat', *,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:

        super().__init__(app, vao_name, tex_id,
                         self.combine_vector(pos, (0, 1, 0), sav=sav),
                         self.combine_vector(rot, (-90, 0, 0), sav=sav),
                         scale, render_area)
        
        self.speed: float = .05

    def update(self) -> None:

        velocity = self.speed * QuantumCore.time.delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP8]:
            self.pos += velocity * self._vec_x
        if keys[pygame.K_KP5]:
            self.pos -= velocity * self._vec_x
        if keys[pygame.K_KP6]:
            self.pos += velocity * self._vec_z
        if keys[pygame.K_KP_4]:
            self.pos -= velocity * self._vec_z
        if keys[pygame.K_KP_PLUS]:
            self.pos += velocity * self._vec_y
        if keys[pygame.K_KP_MINUS]:
            self.pos -= velocity * self._vec_y

        velocity /= 5
        if keys[pygame.K_KP7]:
            self.rot -= velocity * self._vec_z
        if keys[pygame.K_KP9]:
            self.rot += velocity * self._vec_z

        if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01
        
        if keys[pygame.K_TAB]:
            print(self.pos, self.rot)

        self.m_model = self.__get_model_matrix__()
        super().update()

    def light_update(self) -> None: super().update()


class WoodenWatchTower(ExtendedBaseModel):
    def __init__(self, app, vao_name='WoodenWatchTower', tex_id='WoodenWatchTower', *,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:

        super().__init__(app, vao_name, tex_id,
                         self.combine_vector(pos, (0, -1, 0), sav=sav),
                         rot, scale, render_area)


class Earth(ExtendedBaseModel):
    def __init__(self, app, vao_name='Earth', tex_id='Earth', *,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False) -> None:

        super().__init__(app, vao_name, tex_id, pos, rot, scale, render_area)

    def update(self) -> None:

        self.m_model = glm.rotate(self.__get_model_matrix__(),
                                  self.app.time_list['earth animation'] * 0.5, glm.vec3(0, 1, 0))

        super().update()

    def light_update(self) -> None: super().update()
